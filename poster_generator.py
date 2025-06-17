from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

def load_font(path, size):
    return ImageFont.truetype(path, size)

def auto_wrap_text(draw, text, font_path, max_width, max_lines=None, start_font_size=150):
    """Find the largest possible font size that fits text into max_width and optional max_lines"""
    font_size = start_font_size
    while font_size > 10:
        font = load_font(font_path, font_size)
        wrapped = textwrap.wrap(text, width=30)
        lines = []
        for line in wrapped:
            if draw.textlength(line, font=font) <= max_width:
                lines.append(line)
            else:
                break
        if not max_lines or len(lines) <= max_lines:
            return font, lines
        font_size -= 2
    return load_font(font_path, 12), [text]

def create_poster(
    background_path,
    output_path,
    title,
    subtitle,
    date,
    time,
    veranstalter,
    top_color=(153, 35, 35),
):
    # Setup
    DPI = 144
    W_MM, H_MM = 210, 297
    W, H = int(W_MM / 25.4 * DPI), int(H_MM / 25.4 * DPI)

    poster = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(poster)

    # Load & center-crop background
    bg = Image.open(background_path).convert("RGB")
    ratio = max(W / bg.width, H / bg.height)
    new_size = (int(bg.width * ratio), int(bg.height * ratio))
    bg = bg.resize(new_size)
    left = (bg.width - W) // 2
    top = (bg.height - H) // 2
    bg = bg.crop((left, top, left + W, top + H))
    poster.paste(bg, (0, 0))

    # Add gradient
    gradient = Image.new("L", (1, H // 2))
    for y in range(H // 2):
        gradient.putpixel((0, y), int(128 * (1 - y / (H / 2))))
    alpha = gradient.resize((W, H // 2))
    black_overlay = Image.new("RGBA", (W, H // 2), color=(0, 0, 0, 0))
    black_overlay.putalpha(alpha)
    poster.paste(black_overlay, (0, int(H * 0.05)), black_overlay)

    # Red bar
    bar_h = int(H * 0.05)
    draw.rectangle([0, 0, W, bar_h], fill=top_color)

    # Load fonts
    font_dir = "assets"
    rambla = os.path.join(font_dir, "Rambla-Bold.ttf")
    sejagad = os.path.join(font_dir, "GreatSejagad.ttf")

    # Header
    header_text = "heimathafen-WOLGAST.de"
    header_font = load_font(sejagad, int(bar_h * 0.5))
    w = draw.textlength(header_text, font=header_font)
    draw.text(((W - w) / 2, bar_h * 0.2), header_text, font=header_font, fill="white")

    # Title + Subtitle
    content_margin = int(W * 0.05)
    content_width = int(W * 0.6)

    y_offset = bar_h + int(H * 0.03)
    title_font, title_lines = auto_wrap_text(draw, title, rambla, content_width)
    for line in title_lines:
        draw.text((content_margin, y_offset), line, font=title_font, fill="white")
        y_offset += title_font.size + 5

    subtitle_font, subtitle_lines = auto_wrap_text(draw, subtitle, rambla, content_width, max_lines=2, start_font_size=70)
    for line in subtitle_lines:
        draw.text((content_margin, y_offset), line, font=subtitle_font, fill="white")
        y_offset += subtitle_font.size + 5

    # Date & Time
    date_font = load_font(rambla, 120)
    time_font = load_font(rambla, 40)

    date_x = int(W * 0.7)
    date_y = bar_h + int(H * 0.03)
    tag, monat = date.split(".")
    draw.text((date_x, date_y), f"{tag}.", font=date_font, fill="white")
    draw.text((date_x, date_y + date_font.size), f"{monat}.", font=date_font, fill="white")
    draw.text((date_x, date_y + date_font.size * 2 + 10), f"ab {time}", font=time_font, fill="white")

    # Wave (fixierte Version – fest eingebaut)
    wave_path = "assets/Heimathafen_Wave_Blue.svg"
    # Optional: konvertieren nach PNG mit cairosvg
    try:
        import cairosvg
        cairosvg.svg2png(url=wave_path, write_to="temp_wave.png", output_width=W)
        wave = Image.open("temp_wave.png").convert("RGBA")
    except:
        wave = Image.new("RGBA", (W, int(H * 0.15)), (top_color[0], top_color[1], top_color[2], 255))  # Fallback

    wave_y = H - wave.height
    poster.paste(wave, (0, wave_y), wave)

    # Veranstalter auf der Welle
    org_font = load_font(rambla, 42)
    org_lines = textwrap.wrap(veranstalter, width=30)
    org_y = wave_y + 20
    for line in org_lines:
        w = draw.textlength(line, font=org_font)
        draw.text(((W - w) / 2, org_y), line, font=org_font, fill="white")
        org_y += org_font.size + 4

    poster.save(output_path)
