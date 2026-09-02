# Versiones inglesas de los heroes de email (SQM-2153)

Tres heroes de la secuencia de Lienzos llevaban copy castellano quemado dentro
del JPG. Estos scripts generan la versión `-en` a partir del original, sin
rehacer la imagen: reconstruyen solo la zona del texto y vuelven a escribirlo.

| Script | Original | Salida | Qué cambia |
| --- | --- | --- | --- |
| `build-madrid-forbes-en.py` | `hero/madrid-forbes-mejor-ciudad.jpg` | `...-en.jpg` | Titular y "FUENTE: FORBES" → "SOURCE: FORBES" |
| `build-opalo-labels-en.py` | `email-banners/opalo-{salon,bano}-render-realidad.jpg` | `...-en.jpg` | Etiqueta REALIDAD → REALITY (RENDER no cambia) |
| `build-quien-es-sophiq-ai-badge-en.py` | `email-banners/quien-es-sophiq-ia-hero.jpg` | `...-en.jpg` | Badge del holograma IA → AI |

## Tipografía

El titular del hero de Forbes es **Playfair Display Bold**. No estaba
identificada en ningún sitio: se dedujo ajustando candidatos contra el original
hasta clavar la métrica. A 72 px con tracking −3 px reproduce "Madrid," en
242×66 px exactos, y las otras dos líneas con menos del 1,5 % de desviación.
El fichero va en `tools/PlayfairDisplay-Bold.ttf` (Google Fonts, OFL) porque
NO es una fuente de marca: la de marca es Suisse Intl, que sí está en `fonts/`.

La línea de fuente y las etiquetas de Ópalo son Suisse Intl (Medium 14 px con
1 px de tracking, y Light 16 px respectivamente), ajustadas también por
métrica contra el original.

## Método

1. Máscara de la tinta del texto castellano y `cv2.inpaint` para reconstruir el
   fondo. En el hero de Forbes la pared es lisa y queda invisible; en Ópalo se
   limita al interior de la propia caja de la etiqueta, así que la foto de
   detrás no se toca.
2. Se vuelve a escribir el texto inglés alineando el borde izquierdo de la
   tinta y la línea base a las coordenadas medidas del original.
3. Cada script termina midiendo la tinta resultante y comparándola con la del
   original, para que un cambio no pase inadvertido.

El badge IA → AI no re-tipografía nada: son las mismas dos letras en otro
orden, así que se extrae la máscara de opacidad de cada glifo y se recomponen
intercambiadas. Se conserva el trazo, el antialias y el brillo originales.

## Requisitos

`python3` con `pillow`, `numpy` y `opencv-python`.
