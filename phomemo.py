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

    def print_image(self, image_or_path):
        """Imprime uma imagem com controle de fluxo para não estourar o buffer da impressora."""
        if isinstance(image_or_path, (str, Path)):
            img = Image.open(image_or_path)
        else:
            img = image_or_path

        if not self.ser or not self.ser.is_open:
            self.connect()

        # Redimensiona proporcionalmente para 384 pixels se necessário
        if img.width != WIDTH_DOTS:
            new_height = int(img.height * (WIDTH_DOTS / img.width))
            img = img.resize((WIDTH_DOTS, new_height), Image.Resampling.LANCZOS)

        bw = img.convert('L').convert('1', dither=Image.Dither.FLOYDSTEINBERG)
        width, height = bw.size
        pixels = bw.load()

        # Reset e inicialização
        init_cmd = bytearray()
        init_cmd.extend(b'\x1b\x40')        # ESC @
        init_cmd.extend(b'\x1f\x11\x02\x04') # Densidade Phomemo
        self.ser.write(init_cmd)
        self.ser.flush()
        time.sleep(0.05)

        # Transmissão em blocos de 32 linhas para respeitar o buffer de memória da M02
        CHUNK_ROWS = 32
        for start_y in range(0, height, CHUNK_ROWS):
            block_height = min(CHUNK_ROWS, height - start_y)
            block_data = bytearray()
            
            # Cabeçalho ESC/POS GS v 0
            block_data.extend(b'\x1d\x76\x30\x00')
            block_data.append(BYTES_PER_LINE & 0xFF)
            block_data.append((BYTES_PER_LINE >> 8) & 0xFF)
            block_data.append(block_height & 0xFF)
            block_data.append((block_height >> 8) & 0xFF)

            for y in range(start_y, start_y + block_height):
                for byte_idx in range(BYTES_PER_LINE):
                    byte_val = 0
                    for bit_idx in range(8):
                        x = byte_idx * 8 + bit_idx
                        if x < width and pixels[x, y] == 0:
                            byte_val |= (1 << (7 - bit_idx))
                    block_data.append(byte_val)

            self.ser.write(block_data)
            self.ser.flush()
            # Pausa para o cabeçote térmico processar as 32 linhas sem estourar o buffer
            time.sleep(0.22)

        # Feed de avanço final
        feed_cmd = bytearray()
        feed_cmd.extend(b'\x1b\x64\x06')
        feed_cmd.extend(b'\x1f\x11\x08')
        feed_cmd.extend(b'\n\n\n')
        self.ser.write(feed_cmd)
        self.ser.flush()

        # Aguarda a finalização mecânica antes de desconectar
        time.sleep(3.5)

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
