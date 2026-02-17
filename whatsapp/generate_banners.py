"""
Generador de banners WhatsApp para propiedad Ríos Rosas 52 - SERENA
3 opciones de diseño sobre la foto hero
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.path.join(BASE_DIR, "hero_original.jpg")
LOGO_PATH = os.path.join(BASE_DIR, "..", "logos", "sophiq-logo-white.png")
OUTPUT_DIR = BASE_DIR

# WhatsApp optimal size (landscape, good for sharing)
W, H = 1200, 630

# Fonts
FONT_DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
FONT_FUTURA = "/System/Library/Fonts/Supplemental/Futura.ttc"
FONT_AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
FONT_GEORGIA_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
FONT_GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
FONT_HELVETICA = "/System/Library/Fonts/HelveticaNeue.ttc"

# Colors
DARK = (20, 25, 30)
GOLD = (198, 169, 120)
WHITE = (255, 255, 255)
CREAM = (245, 240, 232)
CHARCOAL = (45, 45, 50)


def load_hero():
    img = Image.open(HERO_PATH)
    # Crop to 1200x630 ratio from center
    ratio = W / H
    img_ratio = img.width / img.height
    if img_ratio > ratio:
        new_w = int(img.height * ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        new_h = int(img.width / ratio)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))
    return img.resize((W, H), Image.LANCZOS)


def load_logo(max_width=160, max_height=45):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo.thumbnail((max_width, max_height), Image.LANCZOS)
    return logo


def draw_gradient(draw, y_start, y_end, width, color_top, color_bottom, alpha_top=0, alpha_bottom=220):
    """Draw a vertical gradient."""
    for y in range(y_start, y_end):
        ratio = (y - y_start) / (y_end - y_start)
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        a = int(alpha_top + (alpha_bottom - alpha_top) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, a))


def option_1():
    """
    OPCIÓN 1: Elegante Gradient
    Foto completa con gradiente oscuro inferior.
    Texto blanco con detalles dorados. Limpio y sofisticado.
    """
    hero = load_hero()
    # Slight brightness/contrast adjustment
    hero = ImageEnhance.Contrast(hero).enhance(1.1)
    hero = ImageEnhance.Brightness(hero).enhance(0.95)

    # Create overlay for gradient
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Top subtle gradient (for logo visibility)
    draw_gradient(draw_ov, 0, 100, W, DARK, DARK, alpha_top=120, alpha_bottom=0)

    # Bottom strong gradient
    draw_gradient(draw_ov, H - 280, H, W, DARK, DARK, alpha_top=0, alpha_bottom=240)

    # Composite
    result = hero.convert("RGBA")
    result = Image.alpha_composite(result, overlay)
    result = result.convert("RGB")

    draw = ImageDraw.Draw(result)

    # Logo top-left
    logo = load_logo(140, 40)
    result.paste(logo, (40, 30), logo)

    # "NUEVA PROPIEDAD" tag top-right
    font_tag = ImageFont.truetype(FONT_AVENIR, 13, index=6)  # Demibold
    tag_text = "NUEVA PROPIEDAD"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = W - tag_w - 50
    tag_y = 35

    # Gold line before tag
    draw.line([(tag_x - 20, tag_y + 8), (tag_x - 8, tag_y + 8)], fill=GOLD, width=1)
    draw.text((tag_x, tag_y), tag_text, fill=GOLD, font=font_tag)

    # Property name - bottom area
    font_name = ImageFont.truetype(FONT_DIDOT, 42)
    draw.text((50, H - 200), "SERENA", fill=WHITE, font=font_name)

    # Thin gold separator line
    draw.line([(50, H - 148), (200, H - 148)], fill=GOLD, width=1)

    # Location
    font_loc = ImageFont.truetype(FONT_AVENIR, 16, index=0)  # Regular
    draw.text((50, H - 135), "Ríos Rosas 52  ·  Chamberí, Madrid", fill=CREAM, font=font_loc)

    # Price and details
    font_price = ImageFont.truetype(FONT_AVENIR, 22, index=6)  # Demibold
    draw.text((50, H - 100), "1.850.000 €", fill=WHITE, font=font_price)

    font_detail = ImageFont.truetype(FONT_AVENIR, 15, index=0)
    draw.text((230, H - 96), "167 m²  ·  11.078 €/m²  ·  A reformar", fill=(200, 200, 200), font=font_detail)

    # Tagline bottom-right
    font_tagline = ImageFont.truetype(FONT_AVENIR, 12, index=4)  # Medium italic or regular
    draw.text((W - 290, H - 50), "Esquinazo señorial en finca clásica", fill=GOLD, font=font_tagline)

    result.save(os.path.join(OUTPUT_DIR, "opcion_1_elegante_gradient.jpg"), quality=95)
    print("✓ Opción 1 generada: opcion_1_elegante_gradient.jpg")


def option_2():
    """
    OPCIÓN 2: Premium Split
    Imagen a la izquierda (60%), panel oscuro premium a la derecha (40%)
    con detalles de la propiedad.
    """
    hero_full = load_hero()

    # Create canvas
    result = Image.new("RGB", (W, H), DARK)

    # Left side: cropped image (60% width)
    img_w = int(W * 0.6)
    # Crop hero to fit left panel
    hero_crop = hero_full.crop((0, 0, img_w, H))
    result.paste(hero_crop, (0, 0))

    # Soft edge transition from image to dark panel
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    for x in range(img_w - 80, img_w):
        ratio = (x - (img_w - 80)) / 80
        alpha = int(ratio * 255)
        draw_ov.line([(x, 0), (x, H)], fill=(DARK[0], DARK[1], DARK[2], alpha))

    result_rgba = result.convert("RGBA")
    result_rgba = Image.alpha_composite(result_rgba, overlay)
    result = result_rgba.convert("RGB")

    draw = ImageDraw.Draw(result)

    # Right panel content
    panel_x = img_w + 20
    panel_center = panel_x + (W - panel_x) // 2

    # Logo centered in panel
    logo = load_logo(130, 36)
    logo_x = panel_center - logo.width // 2
    result.paste(logo, (logo_x, 40), logo)

    # Gold decorative line
    line_w = 60
    line_x = panel_center - line_w // 2
    draw.line([(line_x, 90), (line_x + line_w, 90)], fill=GOLD, width=1)

    # "NUEVA PROPIEDAD" label
    font_label = ImageFont.truetype(FONT_AVENIR, 11, index=6)
    label_text = "NUEVA PROPIEDAD"
    label_bbox = draw.textbbox((0, 0), label_text, font=font_label)
    label_w = label_bbox[2] - label_bbox[0]
    draw.text((panel_center - label_w // 2, 105), label_text, fill=GOLD, font=font_label)

    # Property name
    font_name = ImageFont.truetype(FONT_DIDOT, 46)
    name_text = "SERENA"
    name_bbox = draw.textbbox((0, 0), name_text, font=font_name)
    name_w = name_bbox[2] - name_bbox[0]
    draw.text((panel_center - name_w // 2, 140), name_text, fill=WHITE, font=font_name)

    # Location
    font_loc = ImageFont.truetype(FONT_AVENIR, 14, index=0)
    loc_text = "Ríos Rosas 52 · Chamberí"
    loc_bbox = draw.textbbox((0, 0), loc_text, font=font_loc)
    loc_w = loc_bbox[2] - loc_bbox[0]
    draw.text((panel_center - loc_w // 2, 200), loc_text, fill=(180, 180, 180), font=font_loc)

    # Separator
    draw.line([(panel_x + 30, 240), (W - 40, 240)], fill=(60, 60, 65), width=1)

    # Price
    font_price = ImageFont.truetype(FONT_AVENIR, 30, index=6)
    price_text = "1.850.000 €"
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    draw.text((panel_center - price_w // 2, 260), price_text, fill=WHITE, font=font_price)

    # Details grid
    font_detail_label = ImageFont.truetype(FONT_AVENIR, 11, index=0)
    font_detail_value = ImageFont.truetype(FONT_AVENIR, 16, index=6)

    details = [
        ("SUPERFICIE", "167 m²"),
        ("PRECIO/M²", "11.078 €"),
    ]

    detail_y = 320
    col_w = (W - panel_x - 60) // 2
    for i, (label, value) in enumerate(details):
        dx = panel_x + 30 + i * col_w
        # Center each column
        label_bbox = draw.textbbox((0, 0), label, font=font_detail_label)
        label_cw = label_bbox[2] - label_bbox[0]
        value_bbox = draw.textbbox((0, 0), value, font=font_detail_value)
        value_cw = value_bbox[2] - value_bbox[0]

        draw.text((dx + col_w // 2 - label_cw // 2, detail_y), label, fill=GOLD, font=font_detail_label)
        draw.text((dx + col_w // 2 - value_cw // 2, detail_y + 20), value, fill=WHITE, font=font_detail_value)

    # Separator
    draw.line([(panel_x + 30, 380), (W - 40, 380)], fill=(60, 60, 65), width=1)

    # Key features
    font_feat = ImageFont.truetype(FONT_AVENIR, 13, index=0)
    features = [
        "Esquinazo señorial · Finca clásica",
        "8 huecos a calle · Luz excepcional",
        "Techos 3m · Balcones de piedra",
        "Proyecto 100% personalizable",
    ]
    feat_y = 400
    for feat in features:
        feat_bbox = draw.textbbox((0, 0), feat, font=font_feat)
        feat_w = feat_bbox[2] - feat_bbox[0]
        # Gold dot + text
        dot_x = panel_center - feat_w // 2 - 10
        draw.text((dot_x, feat_y), "·", fill=GOLD, font=font_feat)
        draw.text((dot_x + 12, feat_y), feat, fill=(210, 210, 210), font=font_feat)
        feat_y += 28

    # Bottom tagline
    font_tag = ImageFont.truetype(FONT_AVENIR, 11, index=4)
    tag_text = "A REFORMAR · ZONA PRIME CHAMBERÍ"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text((panel_center - tag_w // 2, H - 45), tag_text, fill=GOLD, font=font_tag)

    result.save(os.path.join(OUTPUT_DIR, "opcion_2_premium_split.jpg"), quality=95)
    print("✓ Opción 2 generada: opcion_2_premium_split.jpg")


def option_3():
    """
    OPCIÓN 3: Bold Cinematic
    Foto completa con una franja horizontal semi-transparente al centro-inferior
    estilo cinematográfico. Más moderno y llamativo.
    """
    hero = load_hero()
    hero = ImageEnhance.Contrast(hero).enhance(1.15)
    hero = ImageEnhance.Color(hero).enhance(0.85)  # Slightly desaturated for cinematic feel

    # Create RGBA composite
    result = hero.convert("RGBA")

    # Top bar - thin dark strip
    top_bar = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_top = ImageDraw.Draw(top_bar)
    draw_top.rectangle([(0, 0), (W, 55)], fill=(DARK[0], DARK[1], DARK[2], 200))
    result = Image.alpha_composite(result, top_bar)

    # Main info band in lower portion
    band_y = H - 230
    band_h = 180
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_band = ImageDraw.Draw(band)

    # Gradient band
    for y in range(band_y - 40, band_y):
        ratio = (y - (band_y - 40)) / 40
        draw_band.line([(0, y), (W, y)], fill=(DARK[0], DARK[1], DARK[2], int(ratio * 210)))

    draw_band.rectangle([(0, band_y), (W, band_y + band_h)], fill=(DARK[0], DARK[1], DARK[2], 210))

    # Bottom solid bar
    draw_band.rectangle([(0, band_y + band_h), (W, H)], fill=(DARK[0], DARK[1], DARK[2], 235))

    result = Image.alpha_composite(result, band)
    result_rgb = result.convert("RGB")
    draw = ImageDraw.Draw(result_rgb)

    # Top bar: logo left, "NUEVA PROPIEDAD" right
    logo = load_logo(120, 34)
    result_rgb.paste(logo, (35, 10), logo)

    font_new = ImageFont.truetype(FONT_AVENIR, 12, index=6)
    draw.text((W - 185, 20), "NUEVA PROPIEDAD", fill=GOLD, font=font_new)

    # Main band content
    content_y = band_y + 10

    # Left column: Name + Location
    font_name = ImageFont.truetype(FONT_DIDOT, 50)
    draw.text((50, content_y), "SERENA", fill=WHITE, font=font_name)

    font_subtitle = ImageFont.truetype(FONT_AVENIR, 15, index=0)
    draw.text((50, content_y + 60), "Esquinazo señorial en finca clásica", fill=GOLD, font=font_subtitle)

    font_loc = ImageFont.truetype(FONT_AVENIR, 14, index=0)
    draw.text((50, content_y + 88), "Ríos Rosas 52 · Chamberí, Madrid", fill=(190, 190, 190), font=font_loc)

    # Right column: Price + Key stats
    # Price block - right aligned
    font_price = ImageFont.truetype(FONT_AVENIR, 36, index=6)
    price_text = "1.850.000 €"
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    draw.text((W - price_w - 50, content_y + 5), price_text, fill=WHITE, font=font_price)

    # Stats below price
    font_stat = ImageFont.truetype(FONT_AVENIR, 14, index=0)
    stat_text = "167 m²  ·  11.078 €/m²  ·  A reformar"
    stat_bbox = draw.textbbox((0, 0), stat_text, font=font_stat)
    stat_w = stat_bbox[2] - stat_bbox[0]
    draw.text((W - stat_w - 50, content_y + 52), stat_text, fill=(190, 190, 190), font=font_stat)

    # Vertical gold separator between columns
    sep_x = W // 2 + 40
    draw.line([(sep_x, content_y + 10), (sep_x, content_y + 80)], fill=GOLD, width=1)

    # Bottom strip: key highlights
    font_highlights = ImageFont.truetype(FONT_AVENIR, 12, index=0)
    highlights = "8 huecos a calle  ·  Techos 3m  ·  Balcones de piedra  ·  Azotea comunitaria  ·  Proyecto personalizable"
    hl_bbox = draw.textbbox((0, 0), highlights, font=font_highlights)
    hl_w = hl_bbox[2] - hl_bbox[0]
    draw.text(((W - hl_w) // 2, content_y + 130), highlights, fill=(170, 170, 170), font=font_highlights)

    # Thin gold line above highlights
    draw.line([(50, content_y + 118), (W - 50, content_y + 118)], fill=(GOLD[0], GOLD[1], GOLD[2]), width=1)

    result_rgb.save(os.path.join(OUTPUT_DIR, "opcion_3_bold_cinematic.jpg"), quality=95)
    print("✓ Opción 3 generada: opcion_3_bold_cinematic.jpg")


if __name__ == "__main__":
    print("Generando banners WhatsApp para Ríos Rosas 52 - SERENA...")
    print(f"Tamaño: {W}x{H}px\n")
    option_1()
    option_2()
    option_3()
    print("\n✅ 3 opciones generadas en:", OUTPUT_DIR)
