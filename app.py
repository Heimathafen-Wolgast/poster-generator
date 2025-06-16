import streamlit as st
from poster_maker import create_poster
from PIL import Image

st.set_page_config(page_title="Runge-Poster Generator", layout="centered")

st.title("Poster Generator")

uploaded_file = st.file_uploader("Hintergrundbild hochladen", type=["jpg", "png"])
title = st.text_input("Titel", "Runges Geburtstag")
subtitle = st.text_input("Untertitel", "im Rungehaus")
date_text = st.text_input("Datum (mit Zeilenumbruch)", "25.\n07.")
time_text = st.text_input("Uhrzeit", "ab 14:00")
footer_left = st.text_input("Text links unten", "Philipp Otto\nRunge Klub")
footer_right = st.text_input("Text rechts unten", "heimathafen WOLGAST")

if st.button("🎉 Poster generieren"):
    if uploaded_file:
        with open("input.png", "wb") as f:
            f.write(uploaded_file.read())
        create_poster("input.png", "output.png", date_text, time_text, title, subtitle, footer_left, footer_right)
        st.image("output.png", caption="Dein generiertes Poster", use_column_width=True)
        with open("output.png", "rb") as f:
            st.download_button("⬇️ Poster herunterladen", f, file_name="runge_poster.png", mime="image/png")
    else:
        st.warning("Bitte lade ein Hintergrundbild hoch.")
