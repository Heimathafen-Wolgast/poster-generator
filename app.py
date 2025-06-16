import streamlit as st
import tempfile
from poster_maker import create_poster
from PIL import Image
import os

st.set_page_config(layout="centered", page_title="Plakatgenerator Heimathafen")

st.title("🎨 Plakatgenerator Heimathafen")

with st.form("poster_form"):
    st.subheader("🖼️ Eingaben für das Plakat")

    background_file = st.file_uploader("Hintergrundbild (JPG/PNG)", type=["jpg", "jpeg", "png"], key="background")
    wave_file = st.file_uploader("Wellen-Grafik (SVG/PNG)", type=["png", "svg"], key="wave")

    top_color = st.color_picker("Farbe für obere Leiste und Welle", "#952926")

    title = st.text_input("Titel", "SOMMERKONZERT")
    subtitle = st.text_input("Untertitel", "mit der Wolgaster Band")

    date = st.text_input("Datum (Format: DD.MM)", "12.08")
    time = st.text_input("Uhrzeit", "19:00")

    veranstalter1 = st.text_input("Veranstalter links", "Kulturverein Heimathafen")
    veranstalter2 = st.text_input("Veranstalter rechts (optional)", "")

    submitted = st.form_submit_button("Plakat generieren")

if submitted:
    if not background_file or not wave_file:
        st.error("Bitte lade sowohl ein Hintergrundbild als auch eine Wellen-Grafik hoch.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_wave, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_out:

            tmp_bg.write(background_file.read())
            tmp_bg.flush()

            wave_ext = os.path.splitext(wave_file.name)[1].lower()
            if wave_ext == ".svg":
                # SVG muss in PNG konvertiert werden
                from cairosvg import svg2png
                svg2png(bytestring=wave_file.read(), write_to=tmp_wave.name)
            else:
                tmp_wave.write(wave_file.read())
                tmp_wave.flush()

            create_poster(
                background_path=tmp_bg.name,
                wave_path=tmp_wave.name,
                output_path=tmp_out.name,
                top_color=top_color,
                title=title,
                subtitle=subtitle,
                date=date,
                time=time,
                veranstalter1=veranstalter1,
                veranstalter2=veranstalter2
            )

            st.success("✅ Plakat erfolgreich erstellt!")
            st.image(Image.open(tmp_out.name), caption="Generiertes Plakat", use_column_width=True)
            with open(tmp_out.name, "rb") as f:
                st.download_button("⬇️ Plakat herunterladen", f, file_name="plakat.png", mime="image/png")
