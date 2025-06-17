from PIL import Image, ImageDraw, ImageFont
import cairosvg
import io
import textwrap
import os

DPI = 144
A4_WIDTH_PX = int(8.27 * DPI)
A4_HEIGHT_PX = int(11.69 * DPI)

def load_font(font_path, size):
    return ImageFont.truetype(font_path, size)

def add_gradient(draw, width, height):
    for y in range(int(height/2)):
        alpha = int(128 * (1 - y / (height/2)))
        draw.rectangle([0, y, width, y+1], fill=(0, 0, 0, alpha))

def wrap_text_to_fit(text, font, max_width):
    lines = []
    for paragraph in text.split('\n'):
        line = ""
        for word in paragraph.split():
            test_line = f"{line} {word}".strip()
            if font.getlength(test_line) <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines

def svg_to_png(svg_path, color, width, height):
    with open(svg_path, 'r') as f:
        svg = f.read().replace("#FFFFFF", color)  # Recolor white to given color
    png_data = cairosvg.svg2png(bytestring=svg, output_width=width, output_height=height)
    return Image.open(io.BytesIO(png_data))

def generate_poster(data, output_path='output/poster.png'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Setup
    base = Image.new('RGB', (A4_WIDTH_PX, A4_HEIGHT_PX), (255, 255, 255))
    draw = ImageDraw.Draw(base, 'RGBA')

    # Hintergrundbild einfügen
    bg = Image.open(data['background']).convert("RGB")
    bg_ratio = bg.width / bg.height
    crop_width = A4_WIDTH_PX
    crop_height = int(A4_WIDTH_PX / bg_ratio)
    if crop_height > A4_HEIGHT_PX:
        crop_height = A4_HEIGHT_PX
        crop_width = int(bg_ratio * A4_HEIGHT_PX)
    bg = bg.resize((crop_width, crop_height))
    base.paste(bg.crop((0, 0, A4_WIDTH_PX, A4_HEIGHT_PX)), (0, 0))

    # Schwarzer Verlauf
    gradient = Image.new('RGBA', (A4_WIDTH_PX, A4_HEIGHT_PX), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(gradient)
    add_gradient(grad_draw, A4_WIDTH_PX, A4_HEIGHT_PX)
    base = Image.alpha_composite(base.convert('RGBA'), gradient)

    # Rechteck oben mit Farbe
    draw.rectangle([0, 0, A4_WIDTH_PX, 180], fill=data['theme_color'])

    # Fonts
    font_dir = "fonts"
    headline_font = load_font(f"{font_dir}/GreatSejagad-Regular.ttf", 90)
    rambla_font = load_font(f"{font_dir}/Rambla-Bold.ttf", 60)

    # A - Domain
    draw.text((90, 40), data['domain'], font=headline_font, fill="white")

    # B - Titel & Untertitel
    title_area = (80, 200, A4_WIDTH_PX - 80, 550)
    max_width = title_area[2] - title_area[0]
    title_font = load_font(f"{font_dir}/Rambla-Bold.ttf", 100)
    subtitle_font = load_font(f"{font_dir}/Rambla-Bold.ttf", 40)

    title_lines = wrap_text_to_fit(data['title'], title_font, max_width)
    subtitle_lines = wrap_text_to_fit(data['subtitle'], subtitle_font, max_width)
    y = title_area[1]
    for line in title_lines:
        draw.text((title_area[0], y), line, font=title_font, fill="white")
        y += 100
    for line in subtitle_lines:
        draw.text((title_area[0], y), line, font=subtitle_font, fill="white")
        y += 50

    # C - Datum
    draw.text((A4_WIDTH_PX - 240, 210), data['date_day'], font=rambla_font, fill="white")
    draw.text((A4_WIDTH_PX - 240, 280), data['date_month'], font=rambla_font, fill="white")

    # D - Uhrzeit (zwei Zeilen)
    draw.text((A4_WIDTH_PX - 270, 370), data['time_start'], font=subtitle_font, fill="white")
    draw.text((A4_WIDTH_PX - 270, 420), data['time_desc'], font=subtitle_font, fill="white")

    # E & F - Veranstalter
    org_font = load_font(f"{font_dir}/Rambla-Bold.ttf", 40)
    if len(data['organizers']) >= 1:
        lines = wrap_text_to_fit(data['organizers'][0], org_font, 600)
        draw.text((80, 630), lines[0], font=org_font, fill="white", anchor="lt")
        if len(lines) > 1:
            draw.text((80, 670), lines[1], font=org_font, fill="white", anchor="rt")
    if len(data['organizers']) == 2:
        lines = wrap_text_to_fit(data['organizers'][1], org_font, 600)
        draw.text((80, 730), lines[0], font=org_font, fill="white", anchor="lt")
        if len(lines) > 1:
            draw.text((80, 770), lines[1], font=org_font, fill="white", anchor="rt")

    # G - SVG Logo
    wave = svg_to_png(data['svg_path'], data['theme_color'], 500, 100)
    base.paste(wave, (int((A4_WIDTH_PX - wave.width)/2), 800), wave)

    base.convert('RGB').save(output_path, dpi=(DPI, DPI))


