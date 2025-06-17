from flask import Flask, render_template, request, send_file
from poster_generator import generate_poster
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bg_file = request.files["background"]
        bg_path = os.path.join(UPLOAD_FOLDER, bg_file.filename)
        bg_file.save(bg_path)

        svg_path = 'Welle-weiß.svg'  # already in project

        data = {
            'background': bg_path,
            'theme_color': request.form['theme_color'],
            'domain': request.form['domain'],
            'title': request.form['title'],
            'subtitle': request.form['subtitle'],
            'date_day': request.form['date_day'],
            'date_month': request.form['date_month'],
            'time_start': request.form['time_start'],
            'time_desc': request.form['time_desc'],
            'organizers': request.form.getlist('organizers'),
            'svg_path': svg_path
        }

        generate_poster(data)
        return send_file("output/poster.png", as_attachment=True)

    return '''
    <!doctype html>
    <title>Poster Generator</title>
    <h1>Generiere dein Poster</h1>
    <form method=post enctype=multipart/form-data>
      Hintergrundbild: <input type=file name=background><br>
      Farbe (Hex): <input type=text name=theme_color value="#D32F2F"><br>
      Domain: <input type=text name=domain value="heimathafen-WOLGAST.de"><br>
      Titel: <input type=text name=title><br>
      Untertitel: <input type=text name=subtitle><br>
      Datum Tag: <input type=text name=date_day><br>
      Datum Monat: <input type=text name=date_month><br>
      Uhrzeit Beginn: <input type=text name=time_start><br>
      Uhrzeit Beschreibung: <input type=text name=time_desc><br>
      Veranstalter 1: <input type=text name=organizers><br>
      Veranstalter 2: <input type=text name=organizers><br>
      <input type=submit value="Poster generieren">
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)

 