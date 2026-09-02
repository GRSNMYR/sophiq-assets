"""Genera quien-es-sophiq-ia-hero-en.jpg: el badge "IA" del holograma pasa a "AI".

No se re-tipografia nada. Las dos letras son las mismas, solo cambia el orden,
asi que se extrae la mascara de opacidad de cada glifo (diferencia entre el
original y el panel reconstruido) y se vuelven a componer intercambiadas. Se
conserva el trazo exacto, el antialias y el brillo del original.

Medido sobre el original (1200x675): tinta del badge en x 907-924, y 253-272.
Palo de la "I" en x 907-908, "A" en x 913-924, hueco entre letras de 4 px.
"AI" recompone la A en 907-918 y la I en 923-924: mismo ancho total y mismo
hueco.
"""
from PIL import Image
import numpy as np
import cv2

SRC = '/Users/laraciordia/Claude/repos/sophiq-assets/email-banners/quien-es-sophiq-ia-hero.jpg'
DST = '/Users/laraciordia/Claude/repos/sophiq-assets/email-banners/quien-es-sophiq-ia-hero-en.jpg'

ROI = (900, 246, 932, 280)         # x0, y0, x1, y1
GLYPH_I = (907, 909)               # [x0, x1)
GLYPH_A = (913, 925)
SHIFT_A = -6                       # A: 913-924 -> 907-918
SHIFT_I = +16                      # I: 907-908 -> 923-924

im = Image.open(SRC).convert('RGB')
orig = np.asarray(im).astype(float)
lum = orig.sum(2) / 3

# ---- 1. Panel limpio, sin las letras ------------------------------------
mask = np.zeros(lum.shape, np.uint8)
x0, y0, x1, y1 = ROI
sub = lum[y0:y1, x0:x1]
mask[y0:y1, x0:x1] = (sub > 145).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)
keep = np.zeros_like(mask); keep[y0:y1, x0:x1] = 255
mask = cv2.bitwise_and(mask, keep)
bgr = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
clean_bgr = cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)
clean = cv2.cvtColor(clean_bgr, cv2.COLOR_BGR2RGB).astype(float)

# ---- 2. Opacidad de cada glifo -----------------------------------------
clean_lum = clean.sum(2) / 3
alpha = np.clip((lum - clean_lum) / np.maximum(255.0 - clean_lum, 1.0), 0, 1)
alpha[alpha < 0.06] = 0            # el ruido del JPEG fuera de la letra

# color del trazo: media de los pixeles mas opacos
sel = alpha > 0.6
glyph_color = orig[sel].mean(0)
print('color del trazo:', glyph_color.round(1), ' pixeles opacos:', int(sel.sum()))

# ---- 3. Recomponer AI ---------------------------------------------------
out = clean.copy()
new_alpha = np.zeros_like(alpha)
for (gx0, gx1), shift in [(GLYPH_A, SHIFT_A), (GLYPH_I, SHIFT_I)]:
    band = alpha[y0:y1, gx0:gx1]
    new_alpha[y0:y1, gx0 + shift:gx1 + shift] = np.maximum(
        new_alpha[y0:y1, gx0 + shift:gx1 + shift], band)

a3 = new_alpha[:, :, None]
out = out * (1 - a3) + glyph_color[None, None, :] * a3
res = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
res.save(DST, quality=94, subsampling=0)
print('escrito', DST, res.size)

# ---- 4. Comprobacion ----------------------------------------------------
a2 = np.asarray(res).astype(int); l2 = a2.sum(2) / 3
m = l2[y0:y1, x0:x1] > 145
xs = np.where(m.sum(0) > 0)[0]; ys = np.where(m.sum(1) > 0)[0]
print(f'tinta resultante x {xs.min()+x0}-{xs.max()+x0}  y {ys.min()+y0}-{ys.max()+y0}'
      f'   (original x 907-924, y 253-272)')
cols = sorted(set(xs + x0))
print('columnas con tinta:', cols)
