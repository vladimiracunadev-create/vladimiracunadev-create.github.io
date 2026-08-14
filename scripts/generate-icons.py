#!/usr/bin/env python3
"""Genera el set completo de iconos del portafolio a partir de una sola
definicion: monograma VA sobre el degradado de acento del sitio.

Sustituye a los iconos que habia antes: una "A" generica en la web y, en
Android, el icono de plantilla de Android Studio sobre fondo blanco.

Salidas
-------
Web / PWA  -> assets/icons/
    icon-192.png, icon-512.png        rounded square (purpose: any)
    icon-maskable-512.png             full bleed, glifo dentro del circulo seguro
    apple-touch-icon.png              180px, sin transparencia (iOS pone su mascara)

Android    -> apps/mobile/android/app/src/main/res/mipmap-*/
    ic_launcher.png                   legacy, rounded square
    ic_launcher_round.png             legacy, circular
    ic_launcher_foreground.png        capa adaptativa: glifo en la zona segura
    ic_launcher_background.png        capa adaptativa: degradado a sangre

Uso:  python scripts/generate-icons.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
WEB_ICONS = ROOT / "assets" / "icons"
ANDROID_RES = ROOT / "apps" / "mobile" / "android" / "app" / "src" / "main" / "res"

# Paleta del sitio: --accent en claro/oscuro y el teal de la familia de iconos.
ACCENT_A = (59, 130, 246)    # #3B82F6  = theme_color del manifest
ACCENT_B = (45, 212, 191)    # #2DD4BF
INK = (11, 13, 16)           # #0B0D10  (--bg oscuro)

MONOGRAM = "VA"
FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

# Android: el contenido de la capa foreground debe caber en el circulo central
# de 66dp sobre un lienzo de 108dp. Todo lo de fuera lo recorta el sistema.
ADAPTIVE_SAFE = 66 / 108
# PWA maskable: la zona segura es un circulo del 80% del lado.
MASKABLE_SAFE = 0.80


def load_font(px):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, px)
    raise SystemExit("No se encontro ninguna fuente bold utilizable")


def diagonal_gradient(size, c1, c2):
    """Degradado lineal a 135 grados. Se construye pequeno y se escala:
    un degradado lineal sobrevive al reescalado sin banding visible."""
    n = 64
    mask = Image.new("L", (n, n))
    px = mask.load()
    for y in range(n):
        for x in range(n):
            px[x, y] = int(255 * (x + y) / (2 * n - 2))
    mask = mask.resize((size, size), Image.BICUBIC)

    base = Image.new("RGB", (size, size), c1)
    base.paste(Image.new("RGB", (size, size), c2), (0, 0), mask)
    return base.convert("RGBA")


def draw_monogram(size, color, box_ratio):
    """Glifo VA centrado, escalado para ocupar `box_ratio` del lienzo."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    target = size * box_ratio

    # Busca el tamano de fuente cuyo bbox real cabe en el objetivo. Se mide el
    # bbox pintado, no las metricas, porque el interlineado de la fuente deja
    # aire arriba y abajo que descentraria el monograma.
    px = int(target)
    while px > 4:
        font = load_font(px)
        bbox = font.getbbox(MONOGRAM)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if w <= target and h <= target * 0.78:
            break
        px = int(px * 0.94)

    font = load_font(px)
    bbox = font.getbbox(MONOGRAM)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]

    ImageDraw.Draw(layer).text((x, y), MONOGRAM, font=font, fill=color)
    return layer


def rounded_mask(size, radius_ratio=0.225):
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [(0, 0), (size - 1, size - 1)], radius=int(size * radius_ratio), fill=255
    )
    return mask


def circle_mask(size):
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([(0, 0), (size - 1, size - 1)], fill=255)
    return mask


def composed(size, shape="rounded", glyph_ratio=0.56, opaque=False):
    """Icono completo: fondo degradado + monograma oscuro."""
    icon = diagonal_gradient(size, ACCENT_A, ACCENT_B)
    icon.alpha_composite(draw_monogram(size, INK + (255,), glyph_ratio))

    if shape == "rounded":
        icon.putalpha(rounded_mask(size))
    elif shape == "circle":
        icon.putalpha(circle_mask(size))

    if opaque:  # iOS no admite transparencia en el apple-touch-icon
        flat = Image.new("RGB", (size, size), INK)
        flat.paste(icon, (0, 0), icon)
        return flat
    return icon


def save(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    print(f"  {path.relative_to(ROOT)}  ({path.stat().st_size:,} B)")


def main():
    print("== Web / PWA ==")
    save(composed(192), WEB_ICONS / "icon-192.png")
    save(composed(512), WEB_ICONS / "icon-512.png")
    # Maskable: a sangre y con el glifo mas pequeno, para sobrevivir al recorte
    # circular que aplican Android y Chrome.
    maskable = diagonal_gradient(512, ACCENT_A, ACCENT_B)
    maskable.alpha_composite(draw_monogram(512, INK + (255,), MASKABLE_SAFE * 0.56))
    save(maskable, WEB_ICONS / "icon-maskable-512.png")
    save(composed(180, opaque=True), WEB_ICONS / "apple-touch-icon.png")

    print("== Android legacy ==")
    for dpi, px in [("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)]:
        save(composed(px), ANDROID_RES / f"mipmap-{dpi}" / "ic_launcher.png")
        save(composed(px, shape="circle"), ANDROID_RES / f"mipmap-{dpi}" / "ic_launcher_round.png")

    print("== Android adaptativo ==")
    for dpi, px in [("mdpi", 108), ("hdpi", 162), ("xhdpi", 216), ("xxhdpi", 324), ("xxxhdpi", 432)]:
        save(diagonal_gradient(px, ACCENT_A, ACCENT_B),
             ANDROID_RES / f"mipmap-{dpi}" / "ic_launcher_background.png")
        save(draw_monogram(px, INK + (255,), ADAPTIVE_SAFE * 0.72),
             ANDROID_RES / f"mipmap-{dpi}" / "ic_launcher_foreground.png")


if __name__ == "__main__":
    main()
