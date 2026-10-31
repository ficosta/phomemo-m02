"""
Gerador de Tiras de Estudo de Verbos em Espanhol para Phomemo M02
Versão com FONTES GRANDES e alta legibilidade térmica.
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
            ("él habla", "ele fala"),
            ("nosotros hablamos", "nós falamos"),
            ("ellos hablan", "eles falam")
        ],
        "past": [
            ("yo hablé", "eu falei"),
            ("tú hablaste", "você falou"),
            ("él habló", "ele falou"),
            ("nosotros hablamos", "nós falamos"),
            ("ellos hablaron", "eles falaram")
        ],
        "future": [
            ("yo hablaré", "eu falarei"),
            ("tú hablarás", "você falará"),
            ("él hablará", "ele falará"),
            ("nosotros hablaremos", "nós falaremos"),
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
            ("él come", "ele come"),
            ("nosotros comemos", "nós comemos"),
            ("ellos comen", "eles comem")
        ],
        "past": [
            ("yo comí", "eu comi"),
            ("tú comiste", "você comeu"),
            ("él comió", "ele comeu"),
            ("nosotros comimos", "nós comemos"),
            ("ellos comieron", "eles comeram")
        ],
        "future": [
            ("yo comeré", "eu comerei"),
            ("tú comerás", "você comerá"),
            ("él comerá", "ele comerá"),
            ("nosotros comeremos", "nós comeremos"),
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
            ("él vive", "ele mora"),
            ("nosotros vivimos", "nós moramos"),
            ("ellos viven", "eles moram")
        ],
        "past": [
            ("yo viví", "eu morei"),
            ("tú viviste", "você morou"),
            ("él vivió", "ele morou"),
            ("nosotros vivimos", "nós moramos"),
            ("ellos vivieron", "eles moraram")
        ],
        "future": [
            ("yo viviré", "eu morarei"),
            ("tú vivirás", "você morará"),
            ("él vivirá", "ele morará"),
            ("nosotros viviremos", "nós moraremos"),
            ("ellos vivirán", "eles morarão")
        ],
        "example_es": "Yo viví dos años en Madrid.",
        "example_pt": "Eu morei dois anos em Madri."
    }
}

def draw_speech_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    # Balão 1
    draw.rounded_rectangle([(x, y), (x + 60, y + 40)], radius=9, outline=(0, 0, 0), width=3, fill=(255, 255, 255))
    draw.polygon([(x + 14, y + 38), (x + 20, y + 50), (x + 28, y + 38)], fill=(255, 255, 255), outline=(0, 0, 0))
    draw.line([(x + 15, y + 38), (x + 27, y + 38)], fill=(255, 255, 255), width=3)
    draw.line([(x + 12, y + 14), (x + 48, y + 14)], fill=(0, 0, 0), width=3)
    draw.line([(x + 12, y + 24), (x + 38, y + 24)], fill=(0, 0, 0), width=3)

    # Balão 2
    draw.rounded_rectangle([(x + 44, y + 15), (x + 95, y + 50)], radius=8, outline=(0, 0, 0), width=3, fill=(0, 0, 0))
    draw.polygon([(x + 72, y + 49), (x + 80, y + 60), (x + 86, y + 49)], fill=(0, 0, 0))
    draw.line([(x + 52, y + 26), (x + 86, y + 26)], fill=(255, 255, 255), width=3)
    draw.line([(x + 52, y + 36), (x + 76, y + 36)], fill=(255, 255, 255), width=3)

def draw_food_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    cx, cy = x + 50, y + 32
    draw.ellipse([(cx - 28, cy - 28), (cx + 28, cy + 28)], outline=(0, 0, 0), width=3)
    draw.ellipse([(cx - 18, cy - 18), (cx + 18, cy + 18)], outline=(0, 0, 0), width=2)
    
    gx = cx - 42
    draw.line([(gx, cy - 25), (gx, cy + 25)], fill=(0, 0, 0), width=3)
    draw.line([(gx - 5, cy - 25), (gx + 5, cy - 25)], fill=(0, 0, 0), width=3)
    draw.line([(gx - 5, cy - 25), (gx - 5, cy - 12)], fill=(0, 0, 0), width=2)
    draw.line([(gx + 5, cy - 25), (gx + 5, cy - 12)], fill=(0, 0, 0), width=2)
    
    fx = cx + 42
    draw.line([(fx, cy - 25), (fx, cy + 25)], fill=(0, 0, 0), width=3)
    draw.arc([(fx - 5, cy - 28), (fx + 5, cy - 8)], start=270, end=90, fill=(0, 0, 0), width=3)

def draw_house_icon(draw: ImageDraw.ImageDraw, x: int, y: int):
    cx, cy = x + 50, y + 32
    draw.polygon([(cx, cy - 30), (cx - 36, cy - 2), (cx + 36, cy - 2)], fill=(0, 0, 0))
    draw.rectangle([(cx - 26, cy - 2), (cx + 26, cy + 26)], outline=(0, 0, 0), width=3)
    draw.rectangle([(cx - 9, cy + 5), (cx + 9, cy + 26)], fill=(0, 0, 0))

def generate_verb_strip(verb_key: str) -> Image.Image:
    data = VERBS_DATA[verb_key]
    height = 1140
    img = Image.new('RGB', (WIDTH, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 1. Linha de corte superior
    draw.text((WIDTH // 2, 12), "- - - - - - - - - - - - - - - - - - - - -", fill=(120, 120, 120), anchor="mm", font=get_font(13))

    # 2. Borda externa do cartão
    draw.rounded_rectangle([(6, 26), (WIDTH - 6, height - 26)], radius=14, outline=(0, 0, 0), width=3)

    # 3. Cabeçalho
    draw.rectangle([(6, 26), (WIDTH - 6, 64)], fill=(0, 0, 0))
    draw.text((WIDTH // 2, 45), "ESPAÑOL : VERBOS", fill=(255, 255, 255), anchor="mm", font=get_font(16, bold=True))

    # 4. Verbo principal BEM GRANDE
    draw.text((WIDTH // 2, 106), data["verb"], fill=(0, 0, 0), anchor="mm", font=get_font(38, bold=True))
    
    # Tag de tradução PT-BR
    trans_text = f"=  {data['pt']}  ="
    draw.rounded_rectangle([(WIDTH // 2 - 85, 138), (WIDTH // 2 + 85, 170)], radius=7, outline=(0, 0, 0), width=2, fill=(240, 240, 240))
    draw.text((WIDTH // 2, 154), trans_text, fill=(0, 0, 0), anchor="mm", font=get_font(17, bold=True))

    # 5. Ilustração
    icon_box_y = 182
    draw.rounded_rectangle([(16, icon_box_y), (WIDTH - 16, icon_box_y + 78)], radius=10, outline=(160, 160, 160), width=1, fill=(252, 252, 252))
    if data["icon"] == "speech":
        draw_speech_icon(draw, WIDTH // 2 - 50, icon_box_y + 8)
    elif data["icon"] == "food":
        draw_food_icon(draw, WIDTH // 2 - 50, icon_box_y + 8)
    elif data["icon"] == "house":
        draw_house_icon(draw, WIDTH // 2 - 50, icon_box_y + 8)

    # 6. Blocos de Conjugação com FONTES MAIORES
    def render_tense_block(start_y: int, title_es: str, title_pt: str, conjugations: list) -> int:
        # Header da seção
        draw.rounded_rectangle([(16, start_y), (WIDTH - 16, start_y + 32)], radius=6, fill=(0, 0, 0))
        draw.text((26, start_y + 16), title_es, fill=(255, 255, 255), anchor="lm", font=get_font(15, bold=True))
        draw.text((WIDTH - 26, start_y + 16), f"[{title_pt}]", fill=(220, 220, 220), anchor="rm", font=get_font(14))
        
        cur_y = start_y + 40
        for idx, (es, pt) in enumerate(conjugations):
            if idx % 2 == 1:
                draw.rectangle([(16, cur_y - 2), (WIDTH - 16, cur_y + 27)], fill=(244, 244, 244))
            
            # Espanhol (tamanho 17pt bold)
            draw.text((24, cur_y + 12), es, fill=(0, 0, 0), anchor="lm", font=get_font(17, bold=True))
            # Português (tamanho 15pt regular)
            draw.text((WIDTH - 24, cur_y + 12), f"-> {pt}", fill=(60, 60, 60), anchor="rm", font=get_font(15))
            cur_y += 30
        return cur_y + 10

    # Presente
    y_next = render_tense_block(274, "1. PRESENTE", "Presente", data["present"])
    # Passado
    y_next = render_tense_block(y_next, "2. PASSADO", "Pret. Indefinido", data["past"])
    # Futuro
    y_next = render_tense_block(y_next, "3. FUTURO", "Futuro Simples", data["future"])

    # 7. Frase de Exemplo no cotidiano
    draw.line([(20, y_next), (WIDTH - 20, y_next)], fill=(180, 180, 180), width=1)
    y_next += 8
    draw.text((WIDTH // 2, y_next + 10), "EXEMPLO PRÁTICO", fill=(0, 0, 0), anchor="mm", font=get_font(14, bold=True))
    y_next += 26
    
    # Caixa do exemplo ampliada
    draw.rounded_rectangle([(16, y_next), (WIDTH - 16, y_next + 68)], radius=8, outline=(0, 0, 0), width=2, fill=(248, 248, 248))
    draw.text((24, y_next + 19), f"[ES]  {data['example_es']}", fill=(0, 0, 0), font=get_font(15, bold=True))
    draw.text((24, y_next + 44), f"[PT]  {data['example_pt']}", fill=(70, 70, 70), font=get_font(14))

    # 8. Linha de corte inferior
    draw.text((WIDTH // 2, height - 12), "- - - - - - - - - - - - - - - - - - - - -", fill=(120, 120, 120), anchor="mm", font=get_font(13))

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
