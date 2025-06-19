from flask import Flask, render_template, request, send_file
from .poster_generator import generate_poster
from reportlab.lib.colors import HexColor

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "titel": request.form["titel"],
            "untertitel": request.form["untertitel"],
            "datum": request.form["datum"],
            "ort": request.form["ort"],
            "organisator1": request.form["organisator1"],
            "organisator2": request.form["organisator2"],
            "gradient_enabled": "gradient" in request.form,
            "top_bar_color": HexColor(request.form["top_bar_color"]),
        }

        bg_image = request.files["background"]
        pdf, png = generate_poster(data, bg_image.stream, request.form["top_bar_color"])

        return send_file(pdf, mimetype="application/pdf", as_attachment=True, download_name="plakat.pdf")

    return render_template("index.html")
