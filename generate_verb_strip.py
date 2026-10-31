"""
Gerador de Tiras de Estudo de Verbos em Espanhol para Phomemo M02
Versão COMPLETA com as 6 PESSOAS GRAMATICAIS (incluindo Vosotros).
Compacta e sem desperdício de papel.
Largura: 384px (203 DPI)
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
        "pt": "FALAR",
        "icon": "speech",
        "present": [
            ("yo hablo", "eu falo"),
            ("tú hablas", "você fala"),
            ("él / ella habla", "ele / ela fala"),
            ("nosotros hablamos", "nós falamos"),
            ("vosotros habláis", "vocês falam [vós]"),
            ("ellos hablan", "eles falam")
        ],
        "past": [
            ("yo hablé", "eu falei"),
            ("tú hablaste", "você falou"),
            ("él / ella habló", "ele / ela falou"),
            ("nosotros hablamos", "nós falamos"),
            ("vosotros hablasteis", "vocês falaram [vós]"),
            ("ellos hablaron", "eles falaram")
        ],
        "future": [
            ("yo hablaré", "eu falarei"),
            ("tú hablarás", "você falará"),
            ("él / ella hablará", "ele / ela falará"),
            ("nosotros hablaremos", "nós falaremos"),
            ("vosotros hablaréis", "vocês falarão [vós]"),
            ("ellos hablarán", "eles falarão")
        ],
        "example_es": "Ayer hablé con María.",
        "example_pt": "Ontem falei com a Maria."
    },
    "comer": {
        "verb": "COMER",
        "pt": "COMER",
        "icon": "food",
        "present": [
            ("yo como", "eu como"),
            ("tú comes", "você come"),
            ("él / ella come", "ele / ela come"),
            ("nosotros comemos", "nós comemos"),
            ("vosotros coméis", "vocês comem [vós]"),
            ("ellos comen", "eles comem")
        ],
        "past": [
            ("yo comí", "eu comi"),
            ("tú comiste", "você comeu"),
            ("él / ella comió", "ele / ela comeu"),
            ("nosotros comimos", "nós comemos"),
            ("vosotros comisteis", "vocês comeram [vós]"),
            ("ellos comieron", "eles comeram")
        ],
        "future": [
            ("yo comeré", "eu comerei"),
            ("tú comerás", "você comerá"),
            ("él / ella comerá", "ele / ela comerá"),
            ("nosotros comeremos", "nós comeremos"),
            ("vosotros comeréis", "vocês comerão [vós]"),
            ("ellos comerán", "eles comerão")
        ],
        "example_es": "Mañana comeremos paella.",
        "example_pt": "Amanhã comeremos paella."
    },
    "vivir": {
        "verb": "VIVIR",
        "pt": "VIVER / MORAR",
        "icon": "house",
        "present": [
            ("yo vivo", "eu moro"),
            ("tú vives", "você mora"),
            ("él / ella vive", "ele / ela mora"),
            ("nosotros vivimos", "nós moramos"),
            ("vosotros vivís", "vocês moram [vós]"),
            ("ellos viven", "eles moram")
        ],
        "past": [
            ("yo viví", "eu morei"),
            ("tú viviste", "você morou"),
            ("él / ella vivió", "ele / ela morou"),
            ("nosotros vivimos", "nós moramos"),
            ("vosotros vivisteis", "vocês moraram [vós]"),
            ("ellos vivieron", "eles moraram")
        ],
        "future": [
            ("yo viviré", "eu morarei"),
            ("tú vivirás", "você morará"),
            ("él / ella vivirá", "ele / ela morará"),
            ("nosotros viviremos", "nós moraremos"),
            ("vosotros viviréis", "vocês morarão [vós]"),
            ("ellos vivirán", "eles morarão")
        ],
        "example_es": "Yo viví dos años en Madrid.",
        "example_pt": "Eu morei dois anos em Madri."
    }
}

def draw_mini_speech_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    draw.rounded_rectangle([(x, y), (x + 32, y + 20)], radius=5, outline=(0, 0, 0), width=2, fill=(255, 255, 255))
    draw.polygon([(x + 6, y + 19), (x + 11, y + 26), (x + 16, y + 19)], fill=(255, 255, 255), outline=(0, 0, 0))
    draw.line([(x + 7, y + 19), (x + 15, y + 19)], fill=(255, 255, 255), width=2)
    draw.line([(x + 6, y + 7), (x + 26, y + 7)], fill=(0, 0, 0), width=2)
    draw.line([(x + 6, y + 13), (x + 20, y + 13)], fill=(0, 0, 0), width=2)

def draw_mini_food_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    cx, cy = x + 18, y + 12
    draw.ellipse([(cx - 12, cy - 12), (cx + 12, cy + 12)], outline=(0, 0, 0), width=2)
    draw.line([(cx - 18, cy - 10), (cx - 18, cy + 10)], fill=(0, 0, 0), width=2)
    draw.line([(cx + 18, cy - 10), (cx + 18, cy + 10)], fill=(0, 0, 0), width=2)

def draw_mini_house_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    cx, cy = x + 18, y + 12
    draw.polygon([(cx, cy - 12), (cx - 16, cy), (cx + 16, cy)], fill=(0, 0, 0))
    draw.rectangle([(cx - 12, cy), (cx + 12, cy + 12)], outline=(0, 0, 0), width=2)
    draw.rectangle([(cx - 4, cy + 4), (cx + 4, cy + 12)], fill=(0, 0, 0))

def generate_verb_strip(verb_key: str) -> Image.Image:
    data = VERBS_DATA[verb_key]
    
    canvas_h = 1400
    img = Image.new('RGB', (WIDTH, canvas_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y = 6
    draw.text((WIDTH // 2, y), "- - - - - - - - - - - - - - - - - - - - - - - -", fill=(140, 140, 140), anchor="mm", font=get_font(11))
    y += 12

    card_start_y = y
    
    # Barra de Título Superior Integrada
    draw.rectangle([(6, y), (WIDTH - 6, y + 54)], fill=(0, 0, 0))
    draw.text((18, y + 27), data["verb"], fill=(255, 255, 255), anchor="lm", font=get_font(32, bold=True))
    draw.text((WIDTH - 18, y + 27), f"({data['pt']})", fill=(230, 230, 230), anchor="rm", font=get_font(17, bold=True))
    y += 58

    # Faixa de subtítulo + Ícone
    draw.rectangle([(6, y), (WIDTH - 6, y + 32)], fill=(245, 245, 245))
    draw.text((18, y + 16), "6 PESSOAS GRAMATICAIS", fill=(80, 80, 80), anchor="lm", font=get_font(11, bold=True))
    
    if data["icon"] == "speech":
        draw_mini_speech_icon(draw, WIDTH - 52, y + 4)
    elif data["icon"] == "food":
        draw_mini_food_icon(draw, WIDTH - 52, y + 4)
    elif data["icon"] == "house":
        draw_mini_house_icon(draw, WIDTH - 52, y + 4)
    y += 36

    # 4. Blocos com as 6 Pessoas
    def render_tense_block(cur_y: int, title_es: str, title_pt: str, conjugations: list) -> int:
        draw.rectangle([(6, cur_y), (WIDTH - 6, cur_y + 24)], fill=(40, 40, 40))
        draw.text((16, cur_y + 12), title_es, fill=(255, 255, 255), anchor="lm", font=get_font(13, bold=True))
        draw.text((WIDTH - 16, cur_y + 12), f"[{title_pt}]", fill=(210, 210, 210), anchor="rm", font=get_font(12))
        cur_y += 26

        for idx, (es, pt) in enumerate(conjugations):
            if idx % 2 == 1:
                draw.rectangle([(6, cur_y - 1), (WIDTH - 6, cur_y + 24)], fill=(244, 244, 244))
            
            # Espanhol (16pt Bold)
            draw.text((16, cur_y + 11), es, fill=(0, 0, 0), anchor="lm", font=get_font(16, bold=True))
            # Português (14pt)
            draw.text((WIDTH - 16, cur_y + 11), f"-> {pt}", fill=(60, 60, 60), anchor="rm", font=get_font(14))
            cur_y += 24
            
        return cur_y + 4

    # 1. Presente
    y = render_tense_block(y, "1. PRESENTE", "Presente", data["present"])
    # 2. Passado
    y = render_tense_block(y, "2. PASSADO", "Pret. Indefinido", data["past"])
    # 3. Futuro
    y = render_tense_block(y, "3. FUTURO", "Futuro Simples", data["future"])

    # 5. Frase de Exemplo no cotidiano
    draw.rectangle([(6, y), (WIDTH - 6, y + 48)], fill=(245, 245, 245), outline=(0, 0, 0), width=1)
    draw.text((16, y + 14), f"[ES]  {data['example_es']}", fill=(0, 0, 0), anchor="lm", font=get_font(14, bold=True))
    draw.text((16, y + 34), f"[PT]  {data['example_pt']}", fill=(70, 70, 70), anchor="lm", font=get_font(13))
    y += 52

    # Moldura externa em volta do cartão inteiro
    draw.rectangle([(6, card_start_y), (WIDTH - 6, y)], outline=(0, 0, 0), width=3)
    y += 10

    draw.text((WIDTH // 2, y), "- - - - - - - - - - - - - - - - - - - - - - - -", fill=(140, 140, 140), anchor="mm", font=get_font(11))
    y += 10

    return img.crop((0, 0, WIDTH, y))

def main():
    out_dir = Path(r"C:\Users\felip\Documents\git\phomemo-m02\tiras")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for key in VERBS_DATA:
        img = generate_verb_strip(key)
        path = out_dir / f"tira_{key}.png"
        img.save(path)
        print(f"Gerada ({img.width}x{img.height}px): {path}")

if __name__ == "__main__":
    main()
