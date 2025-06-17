import streamlit as st
from poster_generator import generate_poster
import tempfile
import os

st.set_page_config(page_title="Poster Generator", layout="centered")

st.title("🖼️ Poster Generator – Heimathafen Wolgast")

with st.form("poster_form"):
    st.subheader("🎨 Design-Parameter")

    background_file = st.file_uploader("Hintergrundbild (JPG/PNG)", type=["jpg", "jpeg", "png"])
    theme_color = st.color_picker("Farbthema", "#D32F2F")

    domain = st.text_input("Domain", "heimathafen-WOLGAST.de")
    title = st.text_input("Titel", "Motocross")
    subtitle = st.text_input("Untertitel", "am Zieseberg")

    date_day = st.text_input("Datum – Tag", "26.")
    date_month = st.text_input("Datum – Monat", "07.")

    time_start = st.text_input("Uhrzeit", "ab 09:00")
    time_desc = st.text_input("Uhrzeit Beschreibung", "Training")

    org1 = st.text_input("Veranstalter 1", "Jugendchor des Runge-Gymnasiums")
    org2 = st.text_input("Veranstalter 2", "Wolgaster Vokalisten")

    submitted = st.form_submit_button("📤 Poster generieren")

if submitted and background_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg:
        tmp_bg.write(background_file.read())
        tmp_bg_path = tmp_bg.name

    data = {
        "background": tmp_bg_path,
        "theme_color": theme_color,
        "domain": domain,
        "title": title,
        "subtitle": subtitle,
        "date_day": date_day,
        "date_month": date_month,
        "time_start": time_start,
        "time_desc": time_desc,
        "organizers": [org1] if not org2 else [org1, org2],
        "svg_path": "Welle-weiß.svg"
    }

    output_path = "output/poster.png"
    os.makedirs("output", exist_ok=True)

    with st.spinner("🖌️ Generiere Poster..."):
        generate_poster(data, output_path)

    st.success("✅ Poster erfolgreich erstellt!")
    st.image(output_path, caption="Vorschau", use_column_width=True)
    with open(output_path, "rb") as f:
        st.download_button("📥 Download Poster", f, file_name="poster.png")

 