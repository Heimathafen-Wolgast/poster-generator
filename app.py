import streamlit as st
from poster_maker import create_poster
from PIL import Image
import tempfile

st.set_page_config(page_title="Runge-Poster Generator", layout="centered")

st.title("Poster-Generator")

uploaded_file = st.file_uploader("Hintergrundbild hochladen", type=["jpg", "png"])

title = st.text_input("Titel", "Runges Geburtstag")
subtitle = st.text_input("Untertitel", "im Rungehaus")
date_text = st.text_input("Datum (mit Zeilenumbruch)", "25.\n07.")
time_text = st.text_input("Uhrzeit", "ab 14:00")
footer_left = st.text_input("Text links unten", "Philipp Otto\nRunge Klub")
footer_right = st.text_input("Text rechts unten", "heimathafen WOLGAST")

if st.button("🎉 Poster generieren"):
    if uploaded_file:
        # Temporäre Dateien sicher anlegen
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_input:
            tmp_input.write(uploaded_file.read())
            tmp_input_path = tmp_input.name

        tmp_output_path = tmp_input_path.replace("input", "output")

        # Poster generieren
        create_poster(
            background_path=tmp_input_path,
            output_path=tmp_output_path,
            date_text=date_text,
            time_text=time_text,
            title=title,
            subtitle=subtitle,
            footer_left=footer_left,
            footer_right=footer_right
        )

        # Vorschau anzeigen
        st.image(tmp_output_path, caption="Dein generiertes Poster", use_column_width=True)

        # Download anbieten
        with open(tmp_output_path, "rb") as f:
            st.download_button("⬇️ Poster herunterladen", f, file_name="runge_poster.png", mime="image/png")
    else:
        st.warning("Bitte lade ein Hintergrundbild hoch.")

