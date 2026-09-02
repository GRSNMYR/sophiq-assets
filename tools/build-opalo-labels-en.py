"""Genera las versiones inglesas de los composites de Opalo.

Solo cambia una palabra: la etiqueta REALIDAD pasa a REALITY. RENDER se queda
igual porque se escribe igual en ingles.

Metodo: se borra unicamente la tinta blanca del texto DENTRO del rectangulo
(inpaint sobre la propia caja, que es de relleno casi uniforme) y se vuelve a
escribir la palabra centrada en la misma caja, con la misma altura de mayuscula
y la misma linea base. La caja, su radio, su opacidad y la foto de detras no se
tocan.

Metrica medida sobre el original: caja (616,14)-(704,37), tinta del texto
x 624-696 (72 px) con altura de mayuscula 12 px y linea base en y=31. Suisse
Intl Light a 16 px reproduce "REALIDAD" en 72x12 px exactos.
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

SUISSE_LIGHT = '/Users/laraciordia/Claude/repos/sophiq-assets/fonts/SuisseIntl-Light.otf'
BASE = '/Users/laraciordia/Claude/repos/sophiq-assets/email-banners'
RECT = (616, 14, 704, 37)      # x0, y0, x1, y1 de la caja
BASELINE = 31
TEXT_COLOR = (240, 239, 240)
NEW_WORD = 'REALITY'
TRACK = 0  # sin letterspacing: mismo ajuste tipografico que la etiqueta RENDER

for name in ['opalo-salon-render-realidad', 'opalo-bano-render-realidad']:
    im = Image.open(f'{BASE}/{name}.jpg').convert('RGB')
    arr = np.asarray(im)
    lum = arr.astype(int).sum(2) / 3

    # 1. Mascara: solo la tinta clara dentro de la caja
    mask = np.zeros(lum.shape, np.uint8)
    x0, y0, x1, y1 = RECT
    inner = (slice(y0 + 2, y1 - 1), slice(x0 + 2, x1 - 1))
    mask[inner] = (lum[inner] > 130).astype(np.uint8) * 255
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)
    # nunca tocar fuera de la caja
    keep = np.zeros_like(mask); keep[y0 + 1:y1, x0 + 1:x1] = 255
    mask = cv2.bitwise_and(mask, keep)
    print(f'{name}: pixeles de texto a borrar = {int((mask>0).sum())}')

    # 2. Reconstruir el relleno de la caja
    bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    clean = cv2.inpaint(bgr, mask, 6, cv2.INPAINT_TELEA)
    canvas = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)).convert('RGBA')

    # 3. Escribir la palabra inglesa centrada en la misma caja
    font = ImageFont.truetype(SUISSE_LIGHT, 16)
    pad = 100
    layer = Image.new('RGBA', (canvas.width + pad, canvas.height + pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ascent, _ = font.getmetrics()
    # Sin letterspacing. "REALITY" tiene una letra menos que "REALIDAD", asi que
    # la caja queda con 14 px de aire a cada lado en vez de 8. Se prefiere eso a
    # espaciar las letras: RENDER esta compuesto tight y dos etiquetas con
    # tracking distinto en la misma imagen se notan mas que 6 px de aire (que a
    # la escala del email, 540 de 1200 px, son menos de 3 px).
    x = pad // 2
    for ch in NEW_WORD:
        d.text((x, BASELINE - ascent), ch, font=font, fill=TEXT_COLOR + (255,))
        x += d.textlength(ch, font=font) + TRACK
    alpha = np.asarray(layer.split()[3])
    xs = np.where(alpha.sum(0) > 0)[0]
    w = xs.max() - xs.min() + 1
    dx = (x0 + x1) // 2 - w // 2 - xs.min()
    shifted = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    shifted.paste(layer, (dx, 0))
    canvas.paste(shifted, (0, 0), shifted)
    print(f'   "{NEW_WORD}" ancho {w} px, centrado en x={(x0+x1)//2}')

    out = canvas.convert('RGB')
    dst = f'{BASE}/{name}-en.jpg'
    out.save(dst, quality=94, subsampling=0)

    # 4. Comprobacion
    a2 = np.asarray(out).astype(int); l2 = a2.sum(2) / 3
    m = l2[y0:y1, x0:x1] > 130
    ys = np.where(m.sum(1) > 0)[0]; xs2 = np.where(m.sum(0) > 0)[0]
    print(f'   escrito {dst}  tinta resultante x {xs2.min()+x0}-{xs2.max()+x0} '
          f'y {ys.min()+y0}-{ys.max()+y0}')
