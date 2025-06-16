from PIL import Image, ImageDraw, ImageFont

def create_poster(
    background_path,
    output_path,
    date_text="25.\n07.",
    time_text="ab 14:00",
    title="Runges Geburtstag",
    subtitle="im Rungehaus",
    footer_left="Philipp Otto\nRunge Klub",
    footer_right="heimathafen WOLGAST",
):
    bg = Image.open(background_path).convert("RGBA")
    width, height = bg.size
    draw = ImageDraw.Draw(bg)

    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", int(height * 0.06))
    font_subtitle = ImageFont.truetype("DejaVuSans.ttf", int(height * 0.035))
    font_date = ImageFont.truetype("DejaVuSans-Bold.ttf", int(height * 0.09))
    font_time = ImageFont.truetype("DejaVuSans-Oblique.ttf", int(height * 0.035))
    font_footer = ImageFont.truetype("DejaVuSans.ttf", int(height * 0.035))
    font_footer_bold = ImageFont.truetype("DejaVuSans-Bold.ttf", int(height * 0.04))

    draw.rectangle([(0, 0), (width, int(height * 0.12))], fill=(140, 0, 0))
    draw.text((width * 0.05, height * 0.13), title, font=font_title, fill="white")
    draw.text((width * 0.05, height * 0.2), subtitle, font=font_subtitle, fill="white")
    draw.text((width * 0.75, height * 0.13), date_text, font=font_date, fill="white", align="right")
    draw.text((width * 0.75, height * 0.28), time_text, font=font_time, fill="white")
    draw.rectangle([(0, height * 0.85), (width, height)], fill=(140, 0, 0))
    draw.text((width * 0.07, height * 0.87), footer_left, font=font_footer, fill="white")
    draw.text((width * 0.6, height * 0.88), footer_right, font=font_footer_bold, fill="white")

    bg.save(output_path)