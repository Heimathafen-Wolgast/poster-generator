from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap
import os

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_poster(
    background_path,
    wave_path,
    output_path,
    top_color,
    title,
    subtitle,
    date,
    time,
    veranstalter1,
    veranstalter2=None
):
    # Poster settings
    dpi = 144
    width_mm, height_mm = 210, 297
    width = int(width_mm / 25.4 * dpi)
    height = int(height_mm / 25.4 * dpi)

    poster = Image.new("RGB", (width, height), (255, 255, 255))

    # Load background image and resize
    bg = Image.open(background_path).convert("RGB")
    bg = bg.resize((width, height))
    poster.paste(bg, (0, 0))

    draw = ImageDraw.Draw(poster)

    # Black gradient
    gradient = Image.new('L', (1, height // 2), color=0xFF)
    for y in range(height // 2):
        gradient.putpixel((0, y), int(128 * (1 - y / (height / 2))))
    alpha = gradient.resize((width, height // 2))
    black_img = Image.new('RGB', (width, height // 2), color=(0, 0, 0))
    black_img.putalpha(alpha)
    poster.paste(black_img, (0, int(height * 0.1)), black_img)

    # Fonts
    rambla_path = os.path.join("assets", "Rambla-Bold.ttf")
    sejagad_path = os.path.join("assets", "GreatSejagad.ttf")

    font_size_title = int(height * 0.05)
    font_size_subtitle = int(height * 0.025)
    font_size_date = 96
    font_size_time = 33
    font_size_organizer = 28
    font_size_header = 32

    font_title = load_font(rambla_path, font_size_title)
    font_subtitle = load_font(rambla_path, font_size_subtitle)
    font_date = load_font(rambla_path, font_size_date)
    font_time = load_font(rambla_path, font_size_time)
    font_org = load_font(rambla_path, font_size_organizer)
    font_header = load_font(sejagad_path, font_size_header)

    # Red top bar
    bar_height = int(height * 0.05)
    draw.rectangle([0, 0, width, bar_height], fill=top_color)
    
    # Header text
    text = "heimathafen-WOLGAST.de"
    text_width, _ = draw.textbbox(text, font=font_header)
    draw.text(((width - text_width) / 2, bar_height / 4), text, font=font_header, fill="white")

    # Title + subtitle (green box area)
    margin = int(width * 0.05)
    text_area_width = int(width * 0.6)
    draw.text((margin, bar_height + 20), title, font=font_title, fill="white")
    draw.text((margin, bar_height + 30 + font_size_title), subtitle, font=font_subtitle, fill="white")

    # Date box (black placeholder area)
    date_x = int(width * 0.7)
    date_y = bar_height + 20
    draw.text((date_x, date_y), date.split(".")[0] + ".", font=font_date, fill="white")
    draw.text((date_x, date_y + font_size_date), date.split(".")[1] + ".", font=font_date, fill="white")

    # Time box (lilac area)
    draw.text((date_x, date_y + font_size_date * 2 + 10), "ab " + time, font=font_time, fill="white")

    # Wave graphic
    wave = Image.open(wave_path).convert("RGBA")
    wave = wave.resize((width, int(height * 0.15)))
    poster.paste(wave, (0, height - wave.height), wave)

    # Organizer names (gray box positions)
    org1 = veranstalter1.strip()
    org2 = veranstalter2.strip() if veranstalter2 else ""

    left_x = int(width * 0.15)
    right_x = int(width * 0.55)
    org_y = height - wave.height + 20

    draw.text((left_x, org_y), org1, font=font_org, fill="white")
    if org2:
        draw.text((right_x, org_y), org2, font=font_org, fill="white")

    poster.save(output_path)