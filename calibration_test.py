"""
Gera e imprime uma folha de calibracao de tons, cores simuladas
e resolucao para a impressora termica Phomemo M02.
"""

from PIL import Image, ImageDraw
from phomemo import PhomemoM02, WIDTH_DOTS

def create_calibration_chart() -> Image.Image:
    width = WIDTH_DOTS
    height = 540
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 1. Borda externa e Cabecalho
    draw.rectangle([(4, 4), (width - 5, height - 5)], outline=(0, 0, 0), width=2)
    draw.text((width // 2, 22), "CALIBRACAO DE TONS & CORES", fill=(0, 0, 0), anchor="mm", font_size=17)
    draw.text((width // 2, 40), "Phomemo M02 - 203 DPI (384px)", fill=(0, 0, 0), anchor="mm", font_size=12)
    draw.line([(15, 52), (width - 15, 52)], fill=(0, 0, 0), width=1)

    # 2. Escala de Tons de Cinza
    draw.text((15, 60), "1. Degraus de Cinza (0% a 100%):", fill=(0, 0, 0), font_size=12)
    steps = [0, 25, 50, 76, 102, 127, 153, 178, 204, 230, 255]
    box_w = (width - 40) // len(steps)
    start_x = 20
    y_step = 78
    box_h = 30
    for i, gray in enumerate(steps):
        x = start_x + i * box_w
        draw.rectangle([(x, y_step), (x + box_w - 2, y_step + box_h)], fill=(gray, gray, gray), outline=(0, 0, 0))
        pct = int((1.0 - gray / 255.0) * 100)
        draw.text((x + box_w // 2 - 1, y_step + box_h + 8), f"{pct}%", fill=(0, 0, 0), anchor="mm", font_size=9)

    # 3. Degrade Continuo (0% a 100%)
    draw.text((15, 132), "2. Degrade Continuo (Dithering):", fill=(0, 0, 0), font_size=12)
    grad_y = 150
    grad_h = 24
    for px in range(20, width - 20):
        factor = (px - 20) / (width - 40)
        val = int(255 * (1.0 - factor))
        draw.line([(px, grad_y), (px, grad_y + grad_h)], fill=(val, val, val))
    draw.rectangle([(20, grad_y), (width - 20, grad_y + grad_h)], outline=(0, 0, 0))

    # 4. Simulacao de Cores Primarias e Secundarias (RGB + CMY)
    draw.text((15, 190), "3. Cores Primarias / Secundarias:", fill=(0, 0, 0), font_size=12)
    colors = [
        ("RED", (255, 0, 0)),
        ("GREEN", (0, 200, 0)),
        ("BLUE", (0, 0, 255)),
        ("CYAN", (0, 200, 220)),
        ("MAGENTA", (220, 0, 200)),
        ("YELLOW", (240, 220, 0)),
    ]
    col_w = (width - 40) // len(colors)
    c_y = 210
    c_h = 35
    for i, (name, rgb) in enumerate(colors):
        x = 20 + i * col_w
        draw.rectangle([(x, c_y), (x + col_w - 3, c_y + c_h)], fill=rgb, outline=(0, 0, 0))
        draw.text((x + col_w // 2 - 2, c_y + c_h + 8), name[:3], fill=(0, 0, 0), anchor="mm", font_size=10)

    # 5. Nitidez e Padroes de Linha
    draw.text((15, 272), "4. Teste de Nitidez & Resolucao:", fill=(0, 0, 0), font_size=12)
    vx = 25
    vy = 292
    draw.text((vx, vy), "Linhas 1px V:", fill=(0, 0, 0), font_size=10)
    for lx in range(vx, vx + 60, 2):
        draw.line([(lx, vy + 14), (lx, vy + 45)], fill=(0, 0, 0), width=1)
        
    hx = 115
    draw.text((hx, vy), "Linhas 1px H:", fill=(0, 0, 0), font_size=10)
    for ly in range(vy + 14, vy + 45, 2):
        draw.line([(hx, ly), (hx + 60, ly)], fill=(0, 0, 0), width=1)

    cx = 205
    draw.text((cx, vy), "Xadrez 2x2:", fill=(0, 0, 0), font_size=10)
    for bx in range(cx, cx + 50, 4):
        for by in range(vy + 14, vy + 45, 4):
            draw.rectangle([(bx, by), (bx + 1, by + 1)], fill=(0, 0, 0))
            draw.rectangle([(bx + 2, by + 2), (bx + 3, by + 3)], fill=(0, 0, 0))

    tx = 315
    draw.text((tx - 15, vy), "Foco:", fill=(0, 0, 0), font_size=10)
    center = (tx + 15, vy + 30)
    for r in range(4, 20, 3):
        draw.ellipse([(center[0] - r, center[1] - r), (center[0] + r, center[1] + r)], outline=(0, 0, 0), width=1)

    # 6. Teste de Legibilidade de Texto e Negativo
    draw.line([(15, 355), (width - 15, 355)], fill=(0, 0, 0), width=1)
    draw.text((15, 365), "5. Teste de Tipografia & Contraste:", fill=(0, 0, 0), font_size=12)
    
    draw.text((20, 385), "Texto 14px - Alfabeto ABCDEFG abcdefg 12345", fill=(0, 0, 0), font_size=14)
    draw.text((20, 408), "Texto 11px - Nitidez de caracteres pequenos .,;!?", fill=(0, 0, 0), font_size=11)
    draw.text((20, 428), "Texto 9px - Microtexto termico legivel em 203 DPI", fill=(0, 0, 0), font_size=9)

    draw.rectangle([(20, 450), (width - 20, 495)], fill=(0, 0, 0))
    draw.text((width // 2, 465), "TEXTO NEGATIVO (BRANCO NO PRETO)", fill=(255, 255, 255), anchor="mm", font_size=13)
    draw.text((width // 2, 483), "Verifique se a tinta/calor preenche uniforme", fill=(255, 255, 255), anchor="mm", font_size=10)

    draw.line([(15, 510), (width - 15, 510)], fill=(0, 0, 0), width=1)
    draw.text((width // 2, 520), "[ FIM DO TESTE DE CALIBRACAO ]", fill=(0, 0, 0), anchor="mm", font_size=11)

    return img.crop((0, 0, width, 538))

def main():
    print("Gerando cartao de calibracao...")
    chart = create_calibration_chart()
    with PhomemoM02() as printer:
        printer.print_image(chart)
    print("Concluído!")

if __name__ == "__main__":
    main()
