"""
Gerador de Tiras de Estudo de Verbos em Espanhol para Phomemo M02
384px de largura (203 DPI)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

WIDTH = 384

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

def get_font(size: int, bold: bool = False):
    try:
        font_path = FONT_BOLD if bold else FONT_REG
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

VERBS_DATA = {
    "hablar": {
        "verb": "HABLAR",
        "pt": "Falar",
        "icon": "speech",
        "present": [
            ("yo hablo", "eu falo"),
            ("tú hablas", "você fala"),
            ("él / ella habla", "ele / ela fala"),
            ("nosotros hablamos", "nós falamos"),
            ("ellos / ellas hablan", "eles / elas falam")
        ],
        "past": [
            ("yo hablé", "eu falei"),
            ("tú hablaste", "você falou"),
            ("él / ella habló", "ele / ela falou"),
            ("nosotros hablamos", "nós falamos"),
            ("ellos / ellas hablaron", "eles / elas falaram")
        ],
        "future": [
            ("yo hablaré", "eu falarei"),
            ("tú hablarás", "você falará"),
            ("él / ella hablará", "ele / ela falará"),
            ("nosotros hablaremos", "nós falaremos"),
            ("ellos / ellas hablarán", "eles / elas falarão")
        ],
        "example_es": "Ayer hablé con María sobre eso.",
        "example_pt": "Ontem falei com a Maria sobre isso."
    },
    "comer": {
        "verb": "COMER",
        "pt": "Comer",
        "icon": "food",
        "present": [
            ("yo como", "eu como"),
            ("tú comes", "você come"),
            ("él / ella come", "ele / ela come"),
            ("nosotros comemos", "nós comemos"),
            ("ellos / ellas comen", "eles / elas comem")
        ],
        "past": [
            ("yo comí", "eu comi"),
            ("tú comiste", "você comeu"),
            ("él / ella comió", "ele / ela comeu"),
            ("nosotros comimos", "nós comemos"),
            ("ellos / ellas comieron", "eles / elas comeram")
        ],
        "future": [
            ("yo comeré", "eu comerei"),
            ("tú comerás", "você comerá"),
            ("él / ella comerá", "ele / ela comerá"),
            ("nosotros comeremos", "nós comeremos"),
            ("ellos / ellas comerán", "eles / elas comerão")
        ],
        "example_es": "Mañana comeremos paella juntos.",
        "example_pt": "Amanhã comeremos paella juntos."
    },
    "vivir": {
        "verb": "VIVIR",
        "pt": "Viver / Morar",
        "icon": "house",
        "present": [
            ("yo vivo", "eu vivo / moro"),
            ("tú vives", "você vive / mora"),
            ("él / ella vive", "ele / ela vive"),
            ("nosotros vivimos", "nós vivemos"),
            ("ellos / ellas viven", "eles / elas vivem")
        ],
        "past": [
            ("yo viví", "eu vivi / morei"),
            ("tú viviste", "você viveu"),
            ("él / ella vivió", "ele / ela viveu"),
            ("nosotros vivimos", "nós vivemos"),
            ("ellos / ellas vivieron", "eles / elas viveram")
        ],
        "future": [
            ("yo viviré", "eu viverei"),
            ("tú vivirás", "você viverá"),
            ("él / ella vivirá", "ele / ela viverá"),
            ("nosotros viviremos", "nós viveremos"),
            ("ellos / ellas vivirán", "eles / elas viverão")
        ],
        "example_es": "Yo viví dos años en Madrid.",
        "example_pt": "Eu morei dois anos em Madri."
    }
}

def draw_speech_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    # Balão 1 (fundo branco, borda preta)
    draw.rounded_rectangle([(x, y), (x + 55, y + 36)], radius=8, outline=(0, 0, 0), width=2, fill=(255, 255, 255))
    draw.polygon([(x + 12, y + 35), (x + 18, y + 44), (x + 24, y + 35)], fill=(255, 255, 255), outline=(0, 0, 0))
    draw.line([(x + 13, y + 35), (x + 23, y + 35)], fill=(255, 255, 255), width=2)
    # Linhas de texto no balão 1
    draw.line([(x + 10, y + 13), (x + 45, y + 13)], fill=(0, 0, 0), width=2)
    draw.line([(x + 10, y + 21), (x + 35, y + 21)], fill=(0, 0, 0), width=2)

    # Balão 2 (fundo preto sólido)
    draw.rounded_rectangle([(x + 40, y + 14), (x + 85, y + 46)], radius=7, outline=(0, 0, 0), width=2, fill=(0, 0, 0))
    draw.polygon([(x + 65, y + 45), (x + 72, y + 53), (x + 76, y + 45)], fill=(0, 0, 0))
    # Linhas brancas no balão 2
    draw.line([(x + 48, y + 25), (x + 77, y + 25)], fill=(255, 255, 255), width=2)
    draw.line([(x + 48, y + 33), (x + 68, y + 33)], fill=(255, 255, 255), width=2)

def draw_food_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    cx, cy = x + 45, y + 28
    draw.ellipse([(cx - 24, cy - 24), (cx + 24, cy + 24)], outline=(0, 0, 0), width=2)
    draw.ellipse([(cx - 16, cy - 16), (cx + 16, cy + 16)], outline=(0, 0, 0), width=1)
    
    gx = cx - 35
    draw.line([(gx, cy - 20), (gx, cy + 20)], fill=(0, 0, 0), width=2)
    draw.line([(gx - 4, cy - 20), (gx + 4, cy - 20)], fill=(0, 0, 0), width=2)
    draw.line([(gx - 4, cy - 20), (gx - 4, cy - 10)], fill=(0, 0, 0), width=1)
    draw.line([(gx + 4, cy - 20), (gx + 4, cy - 10)], fill=(0, 0, 0), width=1)
    
    fx = cx + 35
    draw.line([(fx, cy - 20), (fx, cy + 20)], fill=(0, 0, 0), width=2)
    draw.arc([(fx - 4, cy - 22), (fx + 4, cy - 6)], start=270, end=90, fill=(0, 0, 0), width=2)

def draw_house_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    cx, cy = x + 45, y + 28
    # Telhado
    draw.polygon([(cx, cy - 25), (cx - 30, cy - 2), (cx + 30, cy - 2)], fill=(0, 0, 0))
    # Paredes
    draw.rectangle([(cx - 22, cy - 2), (cx + 22, cy + 22)], outline=(0, 0, 0), width=2)
    # Porta
    draw.rectangle([(cx - 7, cy + 4), (cx + 7, cy + 22)], fill=(0, 0, 0))
    # Coraçãozinho na porta / telhado
    draw.ellipse([(cx - 15, cy + 4), (cx - 7, cy + 12)], outline=(0, 0, 0), width=1)

def generate_verb_strip(verb_key: str) -> Image.Image:
    data = VERBS_DATA[verb_key]
    height = 930
    img = Image.new('RGB', (WIDTH, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 1. Linha de corte superior
    draw.text((WIDTH // 2, 10), "- - - - - - - - - - - - - - - - - - - - -", fill=(130, 130, 130), anchor="mm", font=get_font(11))

    # 2. Borda externa do cartão
    draw.rounded_rectangle([(8, 22), (WIDTH - 8, height - 22)], radius=12, outline=(0, 0, 0), width=3)

    # 3. Cabeçalho / Tag de idioma
    draw.rectangle([(8, 22), (WIDTH - 8, 52)], fill=(0, 0, 0))
    draw.text((WIDTH // 2, 37), "GUIA DE VERBOS : ESPANHOL", fill=(255, 255, 255), anchor="mm", font=get_font(13, bold=True))

    # 4. Verbo principal e tradução
    draw.text((WIDTH // 2, 85), data["verb"], fill=(0, 0, 0), anchor="mm", font=get_font(30, bold=True))
    
    # Tag de tradução PT-BR
    trans_text = f"({data['pt']})"
    draw.rounded_rectangle([(WIDTH // 2 - 60, 110), (WIDTH // 2 + 60, 135)], radius=6, outline=(0, 0, 0), width=1, fill=(240, 240, 240))
    draw.text((WIDTH // 2, 122), trans_text, fill=(0, 0, 0), anchor="mm", font=get_font(14, bold=True))

    # 5. Ilustração
    icon_box_y = 145
    draw.rounded_rectangle([(20, icon_box_y), (WIDTH - 20, icon_box_y + 65)], radius=8, outline=(180, 180, 180), width=1, fill=(252, 252, 252))
    if data["icon"] == "speech":
        draw_speech_icon(draw, WIDTH // 2 - 45, icon_box_y + 6)
    elif data["icon"] == "food":
        draw_food_icon(draw, WIDTH // 2 - 45, icon_box_y + 6)
    elif data["icon"] == "house":
        draw_house_icon(draw, WIDTH // 2 - 45, icon_box_y + 6)

    # 6. Blocos de Conjugação (PRESENTE, PASSADO, FUTURO)
    def render_tense_block(start_y: int, title_es: str, title_pt: str, conjugations: list) -> int:
        # Header da seção
        draw.rounded_rectangle([(20, start_y), (WIDTH - 20, start_y + 26)], radius=5, fill=(0, 0, 0))
        draw.text((28, start_y + 13), title_es, fill=(255, 255, 255), anchor="lm", font=get_font(12, bold=True))
        draw.text((WIDTH - 28, start_y + 13), f"[{title_pt}]", fill=(210, 210, 210), anchor="rm", font=get_font(11))
        
        cur_y = start_y + 32
        for idx, (es, pt) in enumerate(conjugations):
            if idx % 2 == 1:
                draw.rectangle([(20, cur_y - 2), (WIDTH - 20, cur_y + 20)], fill=(245, 245, 245))
            
            draw.text((26, cur_y + 9), es, fill=(0, 0, 0), anchor="lm", font=get_font(12, bold=True))
            draw.text((WIDTH - 26, cur_y + 9), f"-> {pt}", fill=(70, 70, 70), anchor="rm", font=get_font(11))
            cur_y += 22
        return cur_y + 8

    # Presente
    y_next = render_tense_block(225, "1. PRESENTE", "Presente", data["present"])
    # Passado
    y_next = render_tense_block(y_next, "2. PRETÉRITO INDEFINIDO", "Passado", data["past"])
    # Futuro
    y_next = render_tense_block(y_next, "3. FUTURO SIMPLE", "Futuro", data["future"])

    # 7. Frase de Exemplo no cotidiano
    draw.line([(24, y_next), (WIDTH - 24, y_next)], fill=(200, 200, 200), width=1)
    y_next += 8
    draw.text((WIDTH // 2, y_next + 6), "EXEMPLO PRÁTICO", fill=(0, 0, 0), anchor="mm", font=get_font(11, bold=True))
    y_next += 20
    
    # Caixa do exemplo
    draw.rounded_rectangle([(20, y_next), (WIDTH - 20, y_next + 52)], radius=6, outline=(0, 0, 0), width=1, fill=(248, 248, 248))
    draw.text((26, y_next + 14), f"[ES]  {data['example_es']}", fill=(0, 0, 0), font=get_font(11, bold=True))
    draw.text((26, y_next + 34), f"[PT]  {data['example_pt']}", fill=(80, 80, 80), font=get_font(11))

    # 8. Linha de corte inferior
    draw.text((WIDTH // 2, height - 10), "- - - - - - - - - - - - - - - - - - - - -", fill=(130, 130, 130), anchor="mm", font=get_font(11))

    return img

def main():
    out_dir = Path(r"C:\Users\felip\Documents\git\phomemo-m02\tiras")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for key in VERBS_DATA:
        img = generate_verb_strip(key)
        path = out_dir / f"tira_{key}.png"
        img.save(path)
        print(f"Gerada: {path}")

if __name__ == "__main__":
    main()
