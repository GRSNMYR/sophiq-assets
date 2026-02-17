"""
Banner WhatsApp simplificado - Ríos Rosas 52 SERENA
Formato cuadrado 1080x1080, texto grande para preview móvil
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.path.join(BASE_DIR, "hero_original.jpg")
LOGO_PATH = os.path.join(BASE_DIR, "..", "logos", "sophiq-logo-white.png")

# Square format - WhatsApp friendly
W, H = 1080, 1080

FONT_DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
FONT_AVENIR = "/System/Library/Fonts/Avenir Next.ttc"

DARK = (20, 25, 30)
GOLD = (198, 169, 120)
WHITE = (255, 255, 255)


def load_hero():
    img = Image.open(HERO_PATH)
    # Crop to square from center
    side = min(img.width, img.height)
    left = (img.width - side) // 2
    top = (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side))
    return img.resize((W, H), Image.LANCZOS)


def load_logo(max_width=200, max_height=56):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo.thumbnail((max_width, max_height), Image.LANCZOS)
    return logo


def generate():
    hero = load_hero()
    hero = ImageEnhance.Contrast(hero).enhance(1.1)
    hero = ImageEnhance.Brightness(hero).enhance(0.9)

    result = hero.convert("RGBA")

    # Strong bottom gradient covering bottom 45%
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    grad_start = int(H * 0.5)
    for y in range(grad_start, H):
        ratio = (y - grad_start) / (H - grad_start)
        alpha = int((ratio ** 1.3) * 250)
        draw_ov.line([(0, y), (W, y)], fill=(DARK[0], DARK[1], DARK[2], alpha))

    result = Image.alpha_composite(result, overlay)
    result = result.convert("RGB")
    draw = ImageDraw.Draw(result)

    # Logo - top left
    logo = load_logo(180, 50)
    result.paste(logo, (50, 40), logo)

    # SERENA - very big
    font_name = ImageFont.truetype(FONT_DIDOT, 90)
    draw.text((60, H - 290), "SERENA", fill=WHITE, font=font_name)

    # Gold line
    draw.line([(60, H - 185), (280, H - 185)], fill=GOLD, width=2)

    # Location - big
    font_loc = ImageFont.truetype(FONT_AVENIR, 30, index=0)
    draw.text((60, H - 165), "Ríos Rosas 52 · Chamberí", fill=(220, 220, 220), font=font_loc)

    # Price - very big
    font_price = ImageFont.truetype(FONT_AVENIR, 48, index=6)  # Demibold
    draw.text((60, H - 110), "1.850.000 €", fill=WHITE, font=font_price)

    result.save(os.path.join(BASE_DIR, "serena_whatsapp.jpg"), quality=95)
    print("✓ serena_whatsapp.jpg generado (1080x1080)")


if __name__ == "__main__":
    generate()
