/**
 * Phomemo M02 - Node.js Driver & CLI
 * Resolução: 203 DPI (384 pixels / 48 bytes por linha)
 */

const { SerialPort } = require('serialport');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const WIDTH_DOTS = 384;
const BYTES_PER_LINE = WIDTH_DOTS / 8; // 48
const DEFAULT_PORT = 'COM6';

/**
 * Detecta a porta COM da Phomemo M02
 */
async function detectPort() {
  const ports = await SerialPort.list();
  for (const p of ports) {
    const hwid = (p.pnpId || p.hardwareId || '').toUpperCase();
    const desc = (p.friendlyName || '').toLowerCase();
    if (hwid.includes('CBF5E7D8337E') || desc.includes('m02') || desc.includes('phomemo')) {
      return p.path;
    }
  }
  return DEFAULT_PORT;
}

class PhomemoM02 {
  constructor(options = {}) {
    this.portName = options.port || null;
    this.baudRate = options.baudRate || 115200;
    this.port = null;
  }

  async connect(retries = 3) {
    if (this.port && this.port.isOpen) return this;

    const targetPort = this.portName || (await detectPort());
    let lastError = null;

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        await new Promise((resolve, reject) => {
          const sp = new SerialPort(
            {
              path: targetPort,
              baudRate: this.baudRate,
              autoOpen: true
            },
            (err) => {
              if (err) return reject(err);
              this.port = sp;
              resolve();
            }
          );
        });
        return this;
      } catch (err) {
        lastError = err;
        if (attempt < retries) {
          await new Promise((r) => setTimeout(r, 1000));
        }
      }
    }
    throw lastError;
  }

  async close() {
    if (this.port && this.port.isOpen) {
      await new Promise((resolve) => this.port.close(resolve));
      this.port = null;
    }
  }

  /**
   * Converte uma imagem (caminho ou buffer) em comando ESC/POS raster com Floyd-Steinberg dithering
   */
  async printImage(imageInput) {
    await this.connect();

    const image = sharp(imageInput);
    const metadata = await image.metadata();
    const targetHeight = Math.round((metadata.height * WIDTH_DOTS) / metadata.width);
    const { data: rawPixels } = await image
      .resize(WIDTH_DOTS, targetHeight)
      .toColourspace('b-w')
      .raw()
      .toBuffer({ resolveWithObject: true });

    const width = WIDTH_DOTS;
    const height = targetHeight;

    // Floyd-Steinberg
    const dither = new Float32Array(rawPixels);
    const binary = new Uint8Array(width * height);

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const idx = y * width + x;
        const oldVal = dither[idx];
        const newVal = oldVal < 128 ? 0 : 255;
        binary[idx] = newVal === 0 ? 1 : 0;
        const error = oldVal - newVal;
        if (x + 1 < width) dither[idx + 1] += error * (7 / 16);
        if (x - 1 >= 0 && y + 1 < height) dither[(y + 1) * width + (x - 1)] += error * (3 / 16);
        if (y + 1 < height) dither[(y + 1) * width + x] += error * (5 / 16);
        if (x + 1 < width && y + 1 < height) dither[(y + 1) * width + (x + 1)] += error * (1 / 16);
      }
    }

    // Inicialização
    await this._writeChunk(Buffer.from([0x1b, 0x40, 0x1f, 0x11, 0x02, 0x04]));
    await new Promise((r) => setTimeout(r, 50));

    // Envio em blocos de 32 linhas para respeitar o buffer de RAM da Phomemo
    const CHUNK_ROWS = 32;
    for (let startY = 0; startY < height; startY += CHUNK_ROWS) {
      const blockHeight = Math.min(CHUNK_ROWS, height - startY);
      const blockData = [];

      blockData.push(0x1d, 0x76, 0x30, 0x00);
      blockData.push(BYTES_PER_LINE & 0xff);
      blockData.push((BYTES_PER_LINE >> 8) & 0xff);
      blockData.push(blockHeight & 0xff);
      blockData.push((blockHeight >> 8) & 0xff);

      for (let y = startY; y < startY + blockHeight; y++) {
        for (let byteIdx = 0; byteIdx < BYTES_PER_LINE; byteIdx++) {
          let byteVal = 0;
          for (let bitIdx = 0; bitIdx < 8; bitIdx++) {
            const x = byteIdx * 8 + bitIdx;
            if (x < width && binary[y * width + x] === 1) {
              byteVal |= 1 << (7 - bitIdx);
            }
          }
          blockData.push(byteVal);
        }
      }

      await this._writeChunk(Buffer.from(blockData));
      await new Promise((r) => setTimeout(r, 220));
    }

    // Feed de avanço
    await this._writeChunk(Buffer.from([0x1b, 0x64, 0x06, 0x1f, 0x11, 0x08, 0x0a, 0x0a, 0x0a]));
    await new Promise((r) => setTimeout(r, 3500));
  }

  async _writeChunk(buf) {
    return new Promise((resolve, reject) => {
      this.port.write(buf, (err) => {
        if (err) return reject(err);
        this.port.drain(resolve);
      });
    });
  }

  async printText(text, options = {}) {
    const title = options.title ? options.title.toUpperCase() : null;
    const fontSize = options.fontSize || 20;

    // Divide em linhas para caber em 384px
    const maxChars = Math.floor((WIDTH_DOTS - 30) / (fontSize * 0.55));
    const lines = [];

    if (title) {
      lines.push(`=== ${title} ===`, '');
    }

    text.split('\n').forEach((para) => {
      const words = para.trim().split(/\s+/);
      let cur = '';
      for (const w of words) {
        if ((cur + ' ' + w).trim().length > maxChars) {
          if (cur) lines.push(cur);
          cur = w;
        } else {
          cur = cur ? `${cur} ${w}` : w;
        }
      }
      if (cur) lines.push(cur);
    });

    const lineHeight = Math.round(fontSize * 1.4);
    const totalHeight = 40 + lines.length * lineHeight;

    const textElements = lines
      .map((l, i) => {
        const escaped = l.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return `<text x="20" y="${30 + i * lineHeight}" font-size="${fontSize}" font-family="Arial, sans-serif" fill="#000">${escaped}</text>`;
      })
      .join('\n');

    const svg = `
      <svg width="${WIDTH_DOTS}" height="${totalHeight}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#fff" />
        ${textElements}
      </svg>
    `;

    const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
    await this.printImage(pngBuffer);
  }
}

// CLI Runner
async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === '--help' || cmd === '-h') {
    console.log(`
Uso do Driver Phomemo M02 (Node.js):
  node phomemo.js text "Seu texto aqui" [--title "Titulo"]
  node phomemo.js image caminho/para/foto.png
    `);
    process.exit(0);
  }

  const printer = new PhomemoM02();

  try {
    if (cmd === 'text') {
      const text = args[1];
      const titleIndex = args.indexOf('--title');
      const title = titleIndex !== -1 ? args[titleIndex + 1] : null;
      console.log('Conectando à Phomemo M02...');
      await printer.connect();
      console.log(`Imprimindo texto na ${printer.port.path}...`);
      await printer.printText(text, { title });
      console.log('Impressão via Node.js concluída com sucesso!');
    } else if (cmd === 'image') {
      const imgPath = args[1];
      if (!imgPath || !fs.existsSync(imgPath)) {
        console.error('Arquivo de imagem não encontrado:', imgPath);
        process.exit(1);
      }
      console.log('Conectando à Phomemo M02...');
      await printer.connect();
      console.log(`Imprimindo imagem '${imgPath}' na ${printer.port.path}...`);
      await printer.printImage(imgPath);
      console.log('Impressão via Node.js concluída com sucesso!');
    }
  } catch (err) {
    console.error('Erro na impressão:', err.message);
  } finally {
    await printer.close();
  }
}

if (require.main === module) {
  main();
}

module.exports = { PhomemoM02, detectPort };
