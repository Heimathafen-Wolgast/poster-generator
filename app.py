from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from poster_generator import create_poster

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Formulardaten
        title = request.form.get("title", "")
        subtitle = request.form.get("subtitle", "")
        date = request.form.get("date", "")  # Format: TT.MM
        time = request.form.get("time", "")  # z.B. "14:00"
        veranstalter = request.form.get("veranstalter", "")
        color = request.form.get("top_color", "#992323")

        # Datei verarbeiten
        bg_file = request.files.get("background")
        if not bg_file:
            return "Hintergrundbild erforderlich", 400
        filename = secure_filename(bg_file.filename)
        bg_path = os.path.join(UPLOAD_FOLDER, filename)
        bg_file.save(bg_path)

        output_path = os.path.join(OUTPUT_FOLDER, "poster_output.png")
        create_poster(
            background_path=bg_path,
            output_path=output_path,
            title=title,
            subtitle=subtitle,
            date=date,
            time=time,
            veranstalter=veranstalter,
            top_color=hex_to_rgb(color),
        )

        return send_file(output_path, mimetype="image/png", as_attachment=True)

    return render_template("form.html")

def hex_to_rgb(hex_color):
    """Wandelt z. B. '#992323' in (153, 35, 35)"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

if __name__ == "__main__":
    app.run(debug=True)
