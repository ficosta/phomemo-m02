"""
Driver e utilitário CLI para Phomemo M02 (Windows - Bluetooth Serial / RFCOMM)
Largura do cabeçote: 384 dots (203 DPI) - 48 bytes por linha.
"""

import sys
import time
import argparse
import textwrap
from pathlib import Path
from typing import Optional
import serial
import serial.tools.list_ports
from PIL import Image, ImageDraw

WIDTH_DOTS = 384
BYTES_PER_LINE = WIDTH_DOTS // 8
DEFAULT_PORT = "COM6"

def detect_phomemo_port() -> str:
    """Tenta detectar a porta COM correspondente à Phomemo M02."""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        hwid = (p.hwid or "").upper()
        desc = (p.description or "").lower()
        if "CBF5E7D8337E" in hwid or "m02" in desc:
            return p.device
    return DEFAULT_PORT

class PhomemoM02:
    def __init__(self, port: Optional[str] = None, baudrate: int = 115200):
        self.port = port or detect_phomemo_port()
        self.baudrate = baudrate
        self.ser: Optional[serial.Serial] = None

    def connect(self, retries: int = 3):
        if not self.ser or not self.ser.is_open:
            last_err = None
            for attempt in range(1, retries + 1):
                try:
                    self.ser = serial.Serial(self.port, self.baudrate, timeout=3.0, write_timeout=5.0)
                    return self
                except Exception as e:
                    last_err = e
                    if attempt < retries:
                        time.sleep(1.0)
            raise last_err
        return self

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.ser = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _convert_to_raster(self, img: Image.Image) -> bytes:
        # Redimensiona mantendo a proporção para 384 pixels
        if img.width != WIDTH_DOTS:
            new_height = int(img.height * (WIDTH_DOTS / img.width))
            img = img.resize((WIDTH_DOTS, new_height), Image.Resampling.LANCZOS)
        
        # Converte para preto e branco com dithering Floyd-Steinberg
        bw = img.convert('L').convert('1', dither=Image.Dither.FLOYDSTEINBERG)
        width, height = bw.size
        pixels = bw.load()
        
        payload = bytearray()
        payload.extend(b'\x1b\x40')        # ESC @ (Reset)
        payload.extend(b'\x1f\x11\x02\x04') # Densidade Phomemo
        
        CHUNK_ROWS = 128
        for start_y in range(0, height, CHUNK_ROWS):
            block_height = min(CHUNK_ROWS, height - start_y)
            payload.extend(b'\x1d\x76\x30\x00')
            payload.append(BYTES_PER_LINE & 0xFF)
            payload.append((BYTES_PER_LINE >> 8) & 0xFF)
            payload.append(block_height & 0xFF)
            payload.append((block_height >> 8) & 0xFF)
            
            for y in range(start_y, start_y + block_height):
                for byte_idx in range(BYTES_PER_LINE):
                    byte_val = 0
                    for bit_idx in range(8):
                        x = byte_idx * 8 + bit_idx
                        if x < width and pixels[x, y] == 0:
                            byte_val |= (1 << (7 - bit_idx))
                    payload.append(byte_val)
                    
        # Feed de avanço
        payload.extend(b'\x1b\x64\x06')
        payload.extend(b'\x1f\x11\x08')
        payload.extend(b'\n\n\n')
        return bytes(payload)

    def _send_payload(self, data: bytes):
        if not self.ser or not self.ser.is_open:
            self.connect()
        chunk_size = 256
        for i in range(0, len(data), chunk_size):
            self.ser.write(data[i:i + chunk_size])
            time.sleep(0.015)
        self.ser.flush()
        time.sleep(2.0)

    def print_image(self, image_or_path):
        """Imprime uma imagem (caminho de arquivo ou PIL Image)."""
        if isinstance(image_or_path, (str, Path)):
            img = Image.open(image_or_path)
        else:
            img = image_or_path
        data = self._convert_to_raster(img)
        self._send_payload(data)

    def print_text(self, text: str, font_size: int = 22, title: Optional[str] = None):
        """Formata e imprime um texto com quebra automática de linha."""
        margin = 15
        max_chars_per_line = int((WIDTH_DOTS - 2 * margin) / (font_size * 0.55))
        
        lines = []
        if title:
            lines.append(f"=== {title.upper()} ===")
            lines.append("")
            
        for paragraph in text.split("\n"):
            if not paragraph.strip():
                lines.append("")
                continue
            wrapped = textwrap.wrap(paragraph, width=max_chars_per_line)
            lines.extend(wrapped)
            
        line_height = int(font_size * 1.4)
        total_height = margin * 2 + len(lines) * line_height + 20
        
        img = Image.new('RGB', (WIDTH_DOTS, max(total_height, 60)), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        y = margin
        for line in lines:
            draw.text((margin, y), line, fill=(0, 0, 0), font_size=font_size)
            y += line_height
            
        self.print_image(img)

    def print_qr(self, data_str: str, caption: Optional[str] = None):
        """Gera e imprime um QR Code centralizado."""
        try:
            import qrcode
        except ImportError:
            raise ImportError("Instale o módulo qrcode para usar esta função: pip install qrcode")

        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(data_str)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Centralizar na fita de 384px
        caption_height = 40 if caption else 10
        total_h = qr_img.height + caption_height + 20
        canvas = Image.new('RGB', (WIDTH_DOTS, total_h), color=(255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        offset_x = (WIDTH_DOTS - qr_img.width) // 2
        canvas.paste(qr_img, (max(0, offset_x), 10))
        
        if caption:
            draw.text((WIDTH_DOTS // 2, qr_img.height + 20), caption, fill=(0, 0, 0), anchor="mm", font_size=16)
            
        self.print_image(canvas)

def main():
    parser = argparse.ArgumentParser(description="Driver CLI para Phomemo M02")
    parser.add_argument("--port", default=None, help="Porta COM da impressora (padrão: auto-detectada)")
    subparsers = parser.add_subparsers(dest="command")

    # Comando: text
    text_parser = subparsers.add_parser("text", help="Imprimir um texto ou nota")
    text_parser.add_argument("content", help="Texto a ser impresso")
    text_parser.add_argument("--title", default=None, help="Título superior opcional")
    text_parser.add_argument("--font-size", type=int, default=22, help="Tamanho da fonte (padrão: 22)")

    # Comando: image
    img_parser = subparsers.add_parser("image", help="Imprimir um arquivo de imagem (PNG/JPG/BMP)")
    img_parser.add_argument("path", help="Caminho da imagem")

    # Comando: qr
    qr_parser = subparsers.add_parser("qr", help="Imprimir um QR Code")
    qr_parser.add_argument("data", help="Texto ou URL do QR Code")
    qr_parser.add_argument("--caption", default=None, help="Legenda abaixo do QR Code")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)

    printer = PhomemoM02(port=args.port)
    with printer:
        if args.command == "text":
            print(f"Imprimindo texto na {printer.port}...")
            printer.print_text(args.content, font_size=args.font_size, title=args.title)
            print("Concluído!")
        elif args.command == "image":
            print(f"Imprimindo imagem '{args.path}' na {printer.port}...")
            printer.print_image(args.path)
            print("Concluído!")
        elif args.command == "qr":
            print(f"Gerando e imprimindo QR Code na {printer.port}...")
            printer.print_qr(args.data, caption=args.caption)
            print("Concluído!")

if __name__ == "__main__":
    main()
