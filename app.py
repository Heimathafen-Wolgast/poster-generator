import streamlit as st
from poster_maker import create_poster
import tempfile
import os

st.set_page_config(page_title="Heimathafen Poster Generator", layout="centered")

st.title("🖼️ Heimathafen Plakat Generator")

with st.form("poster_form"):
    title = st.text_input("Titel", "Rungefest")
    subtitle = st.text_input("Untertitel", "Kunst & Kultur in Wolgast")
    date = st.text_input("Datum (TT.MM)", "25.07")
    time = st.text_input("Uhrzeit", "ab 14:00 Uhr")
    org1 = st.text_input("Veranstalter 1 (zweizeilig mit \\n)", "Philipp Otto\nRunge Klub")
    org2 = st.text_input("Veranstalter 2 (zweizeilig mit \\n, optional)", "heimathafen\nWolgast")
    main_color = st.color_picker("Hauptfarbe (Welle & Kopfzeile)", "#a52a2a")
    background_img = st.file_uploader("Hintergrundbild hochladen", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Plakat generieren")

if submitted and background_img:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_out:

        tmp_bg.write(background_img.read())
        tmp_bg.flush()

        create_poster(
            background_path=tmp_bg.name,
            wave_path="wave.svg",  # ggf. vorher in PNG umwandeln
            output_path=tmp_out.name,
            title=title,
            subtitle=subtitle,
            date=date,
            time=time,
            org1=org1,
            org2=org2,
            main_color=main_color
        )

        st.image(tmp_out.name, caption="Vorschau", use_column_width=True)
        with open(tmp_out.name, "rb") as f:
            st.download_button("📥 Herunterladen", f, file_name="plakat.png")
