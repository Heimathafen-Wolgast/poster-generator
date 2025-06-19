from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import cairosvg
import os

PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.27 x 841.89 pt bei 72dpi

DPI = 300
CM_TO_PT = DPI / 2.54
A4_PX = (int(21 * CM_TO_PT), int(29.7 * CM_TO_PT))

# Schriftarten registrieren
FONT_PATH = "app/static/fonts/"
pdfmetrics.registerFont(TTFont("GreatSejagad", os.path.join(FONT_PATH, "GreatSejagad.ttf")))
pdfmetrics.registerFont(TTFont("Rambla-Bold", os.path.join(FONT_PATH, "Rambla-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Rambla-Regular", os.path.join(FONT_PATH, "Rambla-Regular.ttf")))

def generate_poster(data, bg_image_stream, svg_color):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(A4_PX[0], A4_PX[1]))

    # Hintergrundbild
    if bg_image_stream:
        bg_img = Image.open(bg_image_stream)
        bg_img = bg_img.convert("RGB")
        bg_img = resize_and_crop(bg_img, A4_PX)
        bg_io = io.BytesIO()
        bg_img.save(bg_io, format="PNG")
        bg_io.seek(0)
        c.drawImage(ImageReader(bg_io), 0, 0, width=A4_PX[0], height=A4_PX[1])

    # Kopf-Rechteck
    head_rect_h = 1.67 * CM_TO_PT
    c.setFillColor(data["top_bar_color"])
    c.rect(0, A4_PX[1] - head_rect_h, A4_PX[0], head_rect_h, stroke=0, fill=1)

    # Schriftzug "heimathafen-WOLGAST.de"
    c.setFillColorRGB(1, 1, 1)
    c.setFont("GreatSejagad", 80)  # später berechnen
    text_width = c.stringWidth("heimathafen-WOLGAST.de", "GreatSejagad", 80)
    scale = (10.8 * CM_TO_PT) / text_width
    c.saveState()
    c.translate(A4_PX[0] / 2, A4_PX[1] - head_rect_h / 2)
    c.scale(scale, scale)
    c.drawCentredString(0, -25, "heimathafen-WOLGAST.de")
    c.restoreState()

    # Verlauf-Rechteck (optional)
    if data["gradient_enabled"]:
        gradient_path = create_gradient_rect(A4_PX[0], int(15.2 * CM_TO_PT), alpha=128)
        c.drawImage(gradient_path, 0, A4_PX[1] - head_rect_h - (15.2 * CM_TO_PT),
                    width=A4_PX[0], height=(15.2 * CM_TO_PT), mask='auto')

    # Texte
    draw_text(c, data)

    # SVG (in Farbe einfärben)
    svg_path = "app/static/images/Heimathafen-Wave.svg"
    svg_png_path = recolor_svg(svg_path, svg_color)
    c.drawImage(svg_png_path, 2.0 * CM_TO_PT, 23.7 * CM_TO_PT, width=17.0 * CM_TO_PT, height=4.08 * CM_TO_PT, mask='auto')

    c.showPage()
    c.save()
    buffer.seek(0)

    # PNG Export
    buffer_png = io.BytesIO()
    import cairosvg

    # buffer enthält PDF-Daten
    buffer_pdf = buffer.getvalue()
    png_bytes = cairosvg.svg2png(bytestring=buffer_pdf, write_to=None)
    buffer_png = io.BytesIO(png_bytes)
    buffer_png.seek(0)

    return buffer, buffer_png

def resize_and_crop(img, size):
    img_ratio = img.width / img.height
    target_ratio = size[0] / size[1]
    if img_ratio > target_ratio:
        new_height = size[1]
        new_width = int(new_height * img_ratio)
    else:
        new_width = size[0]
        new_height = int(new_width / img_ratio)
    img = img.resize((new_width, new_height))
    left = (new_width - size[0]) / 2
    top = (new_height - size[1]) / 2
    return img.crop((left, top, left + size[0], top + size[1]))

def create_gradient_rect(width, height, alpha=128):
    img = Image.new('RGBA', (width, height))
    for y in range(height):
        a = int(alpha * (1 - y / height))
        for x in range(width):
            img.putpixel((x, y), (0, 0, 0, a))
    path = "/tmp/gradient.png"
    img.save(path)
    return path

def recolor_svg(svg_path, hex_color):
    svg = open(svg_path, 'r').read().replace("fill=\"#000000\"", f"fill=\"{hex_color}\"")
    out_path = "/tmp/logo.png"
    cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=out_path)
    return out_path

def draw_text(c, data):
    # Du implementierst hier analog die Platzierung aller 7 Textfelder nach den gegebenen Koordinaten.
    # Beispiel (Titel):
    c.setFont("Rambla-Bold", 48)
    c.drawString(1.24 * CM_TO_PT, (29.7 - 3.14) * CM_TO_PT, data["titel"])
    # Und so weiter für „Untertitel“, „Datum“, „Ort“ usw.
