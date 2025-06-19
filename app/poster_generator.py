from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import io, os
from lxml import etree
import cairosvg

# Seitenmaße und Einheiten
DPI = 300
CM_TO_PT = DPI / 2.54
A4_PX = (int(21 * CM_TO_PT), int(29.7 * CM_TO_PT))

# Schriftartenpfad
FONT_PATH = os.path.join(os.path.dirname(__file__), "static/fonts")
for name in ["GreatSejagad", "Rambla-Bold", "Rambla-Regular"]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_PATH, f"{name}.ttf")))

def generate_poster(data, bg_image_stream, svg_color):
    # PDF-Buffer anlegen
    buffer_pdf = io.BytesIO()
    c = canvas.Canvas(buffer_pdf, pagesize=A4_PX)

    # Hintergrundbild
    if bg_image_stream:
        bg = Image.open(bg_image_stream).convert("RGB")
        bg = resize_and_crop(bg, A4_PX)
        tmp = io.BytesIO()
        bg.save(tmp, format="PNG")
        tmp.seek(0)
        c.drawImage(ImageReader(tmp), 0, 0, *A4_PX)

    # Kopf-Rechteck & Schriftzug
    head_h = 1.67 * CM_TO_PT
    c.setFillColor(data["top_bar_color"])
    c.rect(0, A4_PX[1] - head_h, A4_PX[0], head_h, stroke=0, fill=1)

    c.setFillColorRGB(1, 1, 1)
    text = "heimathafen-WOLGAST.de"
    font_size = calculate_font_size(c, text, "GreatSejagad", 10.8 * CM_TO_PT)
    c.setFont("GreatSejagad", font_size)
    c.drawCentredString(A4_PX[0] / 2, A4_PX[1] - (head_h / 2) - (font_size / 4), text)

    # Optionaler Verlauf
    if data["gradient_enabled"]:
        grad_png = create_gradient_rect(A4_PX[0], int(15.2 * CM_TO_PT), alpha=128)
        c.drawImage(ImageReader(open(grad_png, "rb")), 0,
                    A4_PX[1] - head_h - (15.2 * CM_TO_PT), width=A4_PX[0],
                    height=15.2 * CM_TO_PT, mask='auto')

    # Textfelder platzieren
    draw_text(c, data)

    # SVG-Logo einfärben und Platzieren
    svg_buf = recolor_svg(os.path.join(os.path.dirname(__file__), "static/images/Heimathafen-Wave.svg"), svg_color)
    c.drawImage(ImageReader(svg_buf), 2 * CM_TO_PT, 23.7 * CM_TO_PT,
                width=17 * CM_TO_PT, height=4.08 * CM_TO_PT, mask='auto')

    c.showPage()
    c.save()
    buffer_pdf.seek(0)

    # PDF → PNG konvertieren
    png_bytes = cairosvg.svg2png(bytestring=buffer_pdf.getvalue(),
                                 output_width=A4_PX[0], output_height=A4_PX[1])
    buffer_png = io.BytesIO(png_bytes)
    buffer_png.seek(0)

    return buffer_pdf, buffer_png

def calculate_font_size(c, text, font, max_width):
    size = 100
    while c.stringWidth(text, font, size) > max_width:
        size -= 1
        if size < 10: break
    return size

def resize_and_crop(img, size):
    img.thumbnail((size[0], size[1]), Image.LANCZOS)
    left = (img.width - size[0]) / 2
    top = (img.height - size[1]) / 2
    return img.crop((left, top, left + size[0], top + size[1]))

def create_gradient_rect(w, h, alpha=128):
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    mask = Image.new('L', (w, h))
    mask.putdata([int(alpha * (1 - y / h)) for y in range(h) for _ in range(w)])
    img.putalpha(mask)
    path = "/tmp/gradient.png"
    img.save(path)
    return path

def recolor_svg(path, hex_color):
    parser = etree.XMLParser(recover=True, encoding="utf-8")
    tree = etree.parse(path, parser)
    for el in tree.xpath('//*[@fill]'):
        el.attrib['fill'] = hex_color
    svg_bytes = etree.tostring(tree)
    png = cairosvg.svg2png(bytestring=svg_bytes,
                           output_width=int(17 * CM_TO_PT),
                           output_height=int(4.08 * CM_TO_PT))
    buf = io.BytesIO(png)
    buf.seek(0)
    return buf

def draw_text(c, data):
    # Beispiel: Titel-Text
    c.setFont("Rambla-Bold", data.get("titel_size", 48))
    c.drawString(1.24 * CM_TO_PT, (29.7 - 3.14) * CM_TO_PT, data["titel"])
    # TODO: Analoge Einträge für Untertitel, Datum, Ort, Organisatoren

