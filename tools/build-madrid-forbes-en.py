"""Genera hero/madrid-forbes-mejor-ciudad-en.jpg a partir del original castellano.

Tipografia identificada por ajuste numerico sobre el original: Playfair Display
Bold a 72 px con tracking -3 px reproduce "Madrid," en 242x66 px exactos y las
otras dos lineas con menos de 1,5% de desviacion. La linea de fuente es Suisse
Intl Medium 14 px con tracking 1 px (133x11 px frente a 134x11 del original).
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib

import numpy as np
import cv2

SRC = '/Users/laraciordia/Claude/repos/sophiq-assets/hero/madrid-forbes-mejor-ciudad.jpg'
DST = '/Users/laraciordia/Claude/repos/sophiq-assets/hero/madrid-forbes-mejor-ciudad-en.jpg'
PLAYFAIR = str(pathlib.Path(__file__).parent / 'PlayfairDisplay-Bold.ttf')
SUISSE = '/Users/laraciordia/Claude/repos/sophiq-assets/fonts/SuisseIntl-Medium.otf'

HEADLINE_COLOR = (27, 21, 9)
SOURCE_COLOR = (54, 44, 29)
# Lineas del original: (x_ink_izq, baseline)
LINES_EN = [('Madrid,', 103, 208), ('best city in', 104, 278), ('the world.', 104, 347)]
SOURCE_EN = ('SOURCE: FORBES', 105, 428)

im = Image.open(SRC).convert('RGB')
arr = np.asarray(im).astype(int)
lum = arr.sum(2) / 3

# ---- 1. Mascara del texto castellano -------------------------------------
mask = np.zeros(lum.shape, np.uint8)
# titular
box_h = (135, 100, 520, 360)   # x0, y0, x1, y1
box_s = (100, 412, 250, 436)
for x0, y0, x1, y1 in [(box_h[0], box_h[1], box_h[2], box_h[3]), box_s]:
    pass
# titular: umbral bajo (texto casi negro sobre pared clara)
sub = lum[100:360, 95:520]
mask[100:360, 95:520] = (sub < 150).astype(np.uint8) * 255
# linea de fuente: texto gris medio
sub2 = lum[412:436, 100:250]
mask[412:436, 100:250] = (sub2 < 175).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((9, 9), np.uint8), iterations=2)

# ---- 2. Reconstruir la pared --------------------------------------------
bgr = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
clean = cv2.inpaint(bgr, mask, 12, cv2.INPAINT_TELEA)
# La pared es lisa: un suavizado suave solo dentro de la mascara elimina
# cualquier veta que el inpaint arrastre de los bordes.
blur = cv2.GaussianBlur(clean, (0, 0), 9)
m3 = cv2.merge([mask, mask, mask]).astype(float) / 255.0
clean = (clean * (1 - m3) + blur * m3).astype(np.uint8)
canvas = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))

# ---- 3. Texto ingles -----------------------------------------------------
def draw_tracked(target, text, font, color, ink_left, baseline, track):
    """Dibuja `text` con tracking manual alineando el borde izquierdo de la
    tinta a `ink_left` y la linea base a `baseline`."""
    pad = 200
    layer = Image.new('RGBA', (target.width + pad, target.height + pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ascent, _ = font.getmetrics()
    x = pad // 2
    y = baseline - ascent
    for ch in text:
        d.text((x, y), ch, font=font, fill=color + (255,))
        x += d.textlength(ch, font=font) + track
    alpha = np.asarray(layer.split()[3])
    xs = np.where(alpha.sum(0) > 0)[0]
    ys = np.where(alpha.sum(1) > 0)[0]
    dx = ink_left - xs.min()
    # el eje y ya esta puesto por la linea base; solo corregimos x
    target.alpha_composite(layer, dest=(0, 0)) if False else None
    shifted = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    shifted.paste(layer, (dx, 0))
    target.paste(shifted, (0, 0), shifted)
    return ys.min(), ys.max()

canvas = canvas.convert('RGBA')
f_head = ImageFont.truetype(PLAYFAIR, 72)
for text, ink_left, baseline in LINES_EN:
    draw_tracked(canvas, text, f_head, HEADLINE_COLOR, ink_left, baseline, -3)
f_src = ImageFont.truetype(SUISSE, 14)
draw_tracked(canvas, SOURCE_EN[0], f_src, SOURCE_COLOR, SOURCE_EN[1], SOURCE_EN[2], 1.0)

out = canvas.convert('RGB')
out.save(DST, quality=92, subsampling=0)
print('escrito', DST, out.size)

# ---- 4. Comprobacion: medir la tinta resultante --------------------------
a2 = np.asarray(out).astype(int); l2 = a2.sum(2) / 3
def ink_box(y0, y1, x0, x1, thr=150):
    m = l2[y0:y1, x0:x1] < thr
    ys = np.where(m.sum(1) > 0)[0]; xs = np.where(m.sum(0) > 0)[0]
    return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)
print('linea 1 EN:', ink_box(140, 216, 95, 520), ' (original 103,149,344,214)')
print('linea 2 EN:', ink_box(218, 292, 95, 520))
print('linea 3 EN:', ink_box(294, 360, 95, 520))
print('fuente EN :', ink_box(410, 440, 95, 300, thr=175), ' (original 105,418,238,428)')
