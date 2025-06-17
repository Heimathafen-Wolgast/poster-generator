from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import os
import cairosvg
from io import BytesIO

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f"Fehler beim Laden der Schrift: {e}")
        return ImageFont.load_default()

def draw_text_with_wrap(draw, text, font, max_width, start_pos, fill, line_spacing=1.2):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and draw.textlength(line + words[0], font=font) <= max_width:
            line += words.pop(0) + ' '
        lines.append(line.strip())
    y = start_pos[1]
    for line in lines:
        draw.text((start_pos[0], y), line, font=font, fill=fill)
        y += int(font.size * line_spacing)
    return y  # Return end position

def create_poster(
    background_path,
    title,
    subtitle,
    date,
    time,
    veranstalter1,
    veranstalter2,
    output_path,
    top_wave_color="#A00000"
):
    # Postermaße (A4 bei 144 DPI)
    dpi = 144
    width_mm, height_mm = 210, 297
    width = int(width_mm / 25.4 * dpi)
    height = int(height_mm / 25.4 * dpi)

    # Neues Poster erzeugen
    poster = Image.new("RGB", (width, height), (255, 255, 255))

    # Hintergrundbild einfügen (zentriert, nicht verzerrt, ggf. gecropped)
    bg = Image.open(background_path).convert("RGB")
    bg_ratio = bg.width / bg.height
    poster_ratio = width / height

    if bg_ratio > poster_ratio:
        new_height = height
        new_width = int(bg.width * height / bg.height)
    else:
        new_width = width
        new_height = int(bg.height * width / bg.width)

    bg = bg.resize((new_width, new_height))
    bg = bg.crop(((new_width - width) // 2, (new_height - height) // 2,
                  (new_width - width) // 2 + width, (new_height - height) // 2 + height))
    poster.paste(bg, (0, 0))

    draw = ImageDraw.Draw(poster)

    # Farbverlauf von oben bis Mitte
    gradient = Image.new('L', (1, height // 2), color=0xFF)
    for y in range(height // 2):
        alpha = int(128 * (1 - y / (height / 2)))
        gradient.putpixel((0, y), alpha)
    alpha = gradient.resize((width, height // 2))
    black_overlay = Image.new('RGBA', (width, height // 2), color=(0, 0, 0, 0))
    black_overlay.putalpha(alpha)
    poster.paste(black_overlay, (0, int(height * 0.05)), black_overlay)

    # Obere Leiste
    bar_height = int(height * 0.05)
    draw.rectangle([0, 0, width, bar_height], fill=top_wave_color)

    # Schriftarten
    rambla_path = os.path.join("assets", "Rambla-Bold.ttf")
    sejagad_path = os.path.join("assets", "GreatSejagad.ttf")

    font_header = load_font(sejagad_path, int(bar_height * 0.6))
    font_title = load_font(rambla_path, int(height * 0.06))
    font_subtitle = load_font(rambla_path, int(height * 0.035))
    font_date = load_font(rambla_path, int(height * 0.06))
    font_time = load_font(rambla_path, int(height * 0.03))
    font_org = load_font(rambla_path, int(height * 0.027))

    # Header Text
    header_text = "heimathafen-WOLGAST.de"
    w = draw.textlength(header_text, font=font_header)
    draw.text(((width - w) / 2, bar_height * 0.2), header_text, font=font_header, fill="white")

    # Titel & Untertitel
    margin = int(width * 0.05)
    current_y = int(height * 0.08)
    current_y = draw_text_with_wrap(draw, title, font_title, width * 0.6, (margin, current_y), "white")
    current_y += 5
    current_y = draw_text_with_wrap(draw, subtitle, font_subtitle, width * 0.6, (margin, current_y), "white")

    # Datum (groß)
    date_x = int(width * 0.68)
    date_y = int(height * 0.08)
    date_parts = date.split(".")
    if len(date_parts) >= 2:
        draw.text((date_x, date_y), date_parts[0] + ".", font=font_date, fill="white")
        draw.text((date_x, date_y + font_date.size + 5), date_parts[1] + ".", font=font_date, fill="white")

    # Uhrzeit darunter
    draw.text((date_x, date_y + font_date.size * 2 + 10), f"ab {time}", font=font_time, fill="white")

    # Welle einfügen (aus .svg)
    svg_path = os.path.join("assets", "heimathafen_wave_blue.svg")
    wave_png = BytesIO()
    cairosvg.svg2png(url=svg_path, write_to=wave_png, output_width=width)
    wave_img = Image.open(wave_png).convert("RGBA")

    # Farbe der Welle anpassen (wenn nötig)
    wave_colored = ImageOps.colorize(ImageOps.grayscale(wave_img), black="black", white=top_wave_color)
    poster.paste(wave_colored, (0, height - wave_colored.height), wave_img)

    # Veranstalter (mittig über der Welle)
    org_text = veranstalter1 if not veranstalter2 else veranstalter1 + " · " + veranstalter2
    text_w = draw.textlength(org_text, font=font_org)
    draw.text(((width - text_w) / 2, height - wave_colored.height - font_org.size - 10), org_text, font=font_org, fill="white")

    # Speichern
    poster.save(output_path)
