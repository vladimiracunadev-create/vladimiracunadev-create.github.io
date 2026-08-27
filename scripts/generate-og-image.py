#!/usr/bin/env python3
"""Genera las tarjetas Open Graph del sitio (1200x630).

El sitio declaraba `twitter:card = summary_large_image` sin publicar ninguna
imagen: al compartir un enlace en LinkedIn, X, Slack o WhatsApp salia la tarjeta
vacia. Este script produce las imagenes con la misma paleta del sitio, para que
la vista previa se lea como el portafolio y no como un enlace generico.

Salidas -> assets/og/
    og-home.png                  portada
    og-auditoria-codigo-ia.png   /servicios/auditoria-codigo-ia/

Uso:  python scripts/generate-og-image.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "og"
AVATAR = ROOT / "assets" / "icons" / "avatar-vladimir.jpg"

W, H = 1200, 630
PAD = 72

# Paleta: los mismos tokens que :root en styles.css (tema oscuro).
INK = (11, 13, 16)            # --bg
TEXT = (232, 238, 252)        # --text
MUTED = (167, 176, 195)       # --muted
ACCENT = (112, 165, 255)      # --accent
ACCENT_2 = (45, 212, 191)     # teal de la familia de iconos

FONT_BOLD = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_REGULAR = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

CARDS = [
    {
        "out": "og-home.png",
        "title": "Arquitectura, modernización, automatización e IA aplicada",
        "subtitle": "Modernización de sistemas legacy, automatización de procesos, "
                    "cloud y CI/CD, e integración de IA aplicada.",
        "kicker": "PORTAFOLIO PROFESIONAL",
        "pills": ["PHP", "Node.js", "TypeScript", "AWS", "Docker", "IA aplicada"],
    },
    {
        "out": "og-auditoria-codigo-ia.png",
        "title": "Auditoría y recuperación de software generado por IA",
        "subtitle": "Verificación funcional, auditoría técnica, limpieza y reducción "
                    "de deuda técnica, y gobernanza de IA.",
        "kicker": "AI CODE ASSURANCE & REMEDIATION",
        "pills": ["Verificación", "Auditoría", "Limpieza", "Gobernanza"],
    },
]


def load_font(candidates, px):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, px)
    raise SystemExit("No se encontro ninguna fuente utilizable: %s" % candidates)


def radial_glow(size, center, radius, color, strength):
    """Mancha radial suave, como los radial-gradient del body en styles.css.
    Se construye pequena y se escala: el degradado sobrevive al reescalado sin
    banding, y evita un bucle de 1200x630 pixeles en Python."""
    w, h = size
    n = 96
    mask = Image.new("L", (n, n), 0)
    px = mask.load()
    cx, cy = center[0] * n / w, center[1] * n / h
    r = radius * n / max(w, h)
    for y in range(n):
        for x in range(n):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d < r:
                px[x, y] = int(strength * (1 - d / r) ** 2)
    mask = mask.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(24))

    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(mask)
    return layer


def wrap(draw, text, font, max_width):
    """Ajuste por palabras midiendo el ancho real pintado."""
    words, lines, line = text.split(), [], ""
    for word in words:
        probe = (line + " " + word).strip()
        if draw.textlength(probe, font=font) <= max_width or not line:
            line = probe
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def circular_avatar(path, size):
    if not path.exists():
        return None
    img = Image.open(path).convert("RGB")
    side = min(img.size)
    img = img.crop(((img.width - side) // 2, (img.height - side) // 2,
                    (img.width + side) // 2, (img.height + side) // 2))
    # Se rasteriza 4x y se reduce: el borde del circulo queda sin dientes sin
    # necesitar antialias manual.
    img = img.resize((size * 4, size * 4), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse([(0, 0), (size * 4 - 1, size * 4 - 1)], fill=255)
    img.putalpha(mask)
    return img.resize((size, size), Image.LANCZOS)


def build(card):
    base = Image.new("RGBA", (W, H), INK + (255,))
    base.alpha_composite(radial_glow((W, H), (240, -60), 760, ACCENT, 92))
    base.alpha_composite(radial_glow((W, H), (1120, 90), 640, ACCENT_2, 46))

    draw = ImageDraw.Draw(base)

    # Barra de acento en el canto izquierdo: la misma marca visual que .ai-claim.
    draw.rectangle([(0, 0), (10, H)], fill=ACCENT)

    f_kicker = load_font(FONT_BOLD, 22)
    f_title = load_font(FONT_BOLD, 58)
    f_sub = load_font(FONT_REGULAR, 27)
    f_name = load_font(FONT_BOLD, 30)
    f_role = load_font(FONT_REGULAR, 22)
    f_pill = load_font(FONT_REGULAR, 21)

    text_w = W - PAD * 2

    # ── Kicker ──────────────────────────────────────────────────────
    y = PAD
    draw.text((PAD, y), " ".join(card["kicker"]), font=f_kicker, fill=ACCENT)
    y += 54

    # ── Titular ─────────────────────────────────────────────────────
    lines = wrap(draw, card["title"], f_title, text_w)
    for line in lines[:3]:
        draw.text((PAD, y), line, font=f_title, fill=TEXT)
        y += 70
    y += 10

    # ── Bajada ──────────────────────────────────────────────────────
    for line in wrap(draw, card["subtitle"], f_sub, text_w)[:2]:
        draw.text((PAD, y), line, font=f_sub, fill=MUTED)
        y += 38

    # ── Pills ───────────────────────────────────────────────────────
    y += 18
    x = PAD
    for label in card["pills"]:
        tw = draw.textlength(label, font=f_pill)
        box = [(x, y), (x + tw + 32, y + 42)]
        draw.rounded_rectangle(box, radius=21, fill=(255, 255, 255, 16),
                               outline=(255, 255, 255, 46), width=1)
        draw.text((x + 16, y + 8), label, font=f_pill, fill=MUTED)
        x += tw + 44

    # ── Pie: avatar, nombre y dominio ───────────────────────────────
    foot_y = H - PAD - 96
    avatar = circular_avatar(AVATAR, 96)
    if avatar:
        ring = 3
        draw.ellipse([(PAD - ring, foot_y - ring), (PAD + 96 + ring, foot_y + 96 + ring)],
                     outline=ACCENT, width=ring)
        base.alpha_composite(avatar, (PAD, foot_y))
        tx = PAD + 96 + 24
    else:
        tx = PAD

    draw.text((tx, foot_y + 16), "Vladimir Acuña", font=f_name, fill=TEXT)
    draw.text((tx, foot_y + 56), "vladimiracunadev-create.github.io",
              font=f_role, fill=MUTED)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / card["out"]
    base.convert("RGB").save(out, "PNG", optimize=True)
    print("%-32s %5d x %d  %6.1f KB" % (card["out"], W, H, out.stat().st_size / 1024))


if __name__ == "__main__":
    for card in CARDS:
        build(card)
