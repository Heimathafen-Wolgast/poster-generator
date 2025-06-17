import streamlit as st
from poster_generator import create_poster
import tempfile
import os

st.set_page_config(page_title="Heimathafen Plakat Generator", layout="centered")

st.title("🎨 Heimathafen Plakat Generator")

with st.form("poster_form"):
    title = st.text_input("Titel")
    subtitle = st.text_input("Untertitel")
    date = st.text_input("Datum (TT.MM)")
    time = st.text_input("Uhrzeit")
    veranstalter1 = st.text_input("Veranstalter 1")
    veranstalter2 = st.text_input("Veranstalter 2 (optional)")
    top_wave_color = st.color_picker("Farbe für oberen Balken & Welle", "#A00000")
    bg_file = st.file_uploader("Hintergrundbild (JPG oder PNG)", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Plakat generieren")

    if submitted:
        if not bg_file:
            st.error("Bitte lade ein Hintergrundbild hoch.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(bg_file.read())
                tmp_path = tmp.name

            output_path = "poster_output.png"
            create_poster(
                background_path=tmp_path,
                title=title,
                subtitle=subtitle,
                date=date,
                time=time,
                veranstalter1=veranstalter1,
                veranstalter2=veranstalter2,
                output_path=output_path,
                top_wave_color=top_wave_color
            )

            st.image(output_path, caption="Vorschau", use_column_width=True)

            with open(output_path, "rb") as f:
                st.download_button("📥 Poster herunterladen", f, file_name="poster.png", mime="image/png")
