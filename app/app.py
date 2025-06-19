from flask import Flask, render_template, request, send_file, Response
from werkzeug.wsgi import FileWrapper
from reportlab.lib.colors import HexColor
from poster_generator import generate_poster 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Formulardaten sammeln
        data = {
            "titel": request.form.get("titel", ""),
            "untertitel": request.form.get("untertitel", ""),
            "datum": request.form.get("datum", ""),
            "ort": request.form.get("ort", ""),
            "organisator1": request.form.get("organisator1", ""),
            "organisator2": request.form.get("organisator2", ""),
            "gradient_enabled": "gradient" in request.form,
            "top_bar_color": HexColor(request.form.get("top_bar_color", "#000000")),
        }

        # Hintergrundbild prüfen
        bg_file = request.files.get("background")
        if not bg_file or bg_file.filename == "":
            return "Fehler: Kein Hintergrundbild ausgewählt.", 400

        # Poster erstellen
        pdf_buf, png_buf = generate_poster(data, bg_file.stream, request.form.get("top_bar_color"))

        # Range für sicheren Download
        pdf_buf.seek(0)
        wrapper = FileWrapper(pdf_buf)
        headers = {
            "Content-Type": "application/pdf",
            "Content-Disposition": 'attachment; filename="plakat.pdf"',
        }

        return Response(wrapper, headers=headers, direct_passthrough=True)

    return render_template("index.html")

