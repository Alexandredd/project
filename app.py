import streamlit as st
import requests
import difflib
from gtts import gTTS
import base64
from io import BytesIO

# ---------------------------------------------------------------
# CONFIGURAÇÃO DO APP
# ---------------------------------------------------------------
st.set_page_config(page_title="English Buddy", page_icon="📘")
st.title("English Buddy - Treine seu Inglês")

# ---------------------------------------------------------------
# MENU LATERAL
# ---------------------------------------------------------------
menu = st.sidebar.radio("Escolha uma habilidade:", [
    "Escrita ✍️",
    "Escuta 🎧",
    "Fala 🗣️",
    "Tradução 🌍",
    "Conjugação 🔄"
])

# ---------------------------------------------------------------
# FUNÇÃO DE CORREÇÃO (LANGUAGETOOL)
# ---------------------------------------------------------------
def corrigir_texto(texto):
    url = "https://api.languagetool.org/v2/check"
    data = {"text": texto, "language": "en-US"}

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return [("Erro na API LanguageTool:", str(e))]

    result = response.json()
    sugestoes = []

    for match in result.get("matches", []):
        palavra_original = texto[match["offset"]:match["offset"] + match["length"]]
        melhores = []