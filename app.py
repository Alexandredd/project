import streamlit as st
import requests
import difflib
from gtts import gTTS
import base64
from io import BytesIO

st.set_page_config(page_title="English Buddy", page_icon="📘")
st.title("English Buddy - Treine seu Inglês")

# --- Menu lateral ---
menu = st.sidebar.radio("Escolha uma habilidade:", [
    "Escrita ✍️", "Escuta 🎧", "Fala 🗣️", "Tradução 🌍", "Conjugação 🔄"
])

# --- Função de correção ---
def corrigir_texto(texto):
    url = "https://api.languagetool.org/v2/check"
    data = {
        "text": texto,
        "language": "en-US"
    }

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

        for r in match.get("replacements", []):
            sugestao = r["value"]
            similaridade = difflib.SequenceMatcher(None, palavra_original, sugestao).ratio()

            if similaridade > 0.5:
                melhores.append((sugestao, similaridade))

        if melhores:
            melhores.sort(key=lambda x: x[1], reverse=True)
            sugestoes.append((match["message"], melhores[0][0]))

    return sugestoes

# --- Função de áudio ---
def gerar_audio(frase):
    try:
        tts = gTTS(frase, lang="en")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
    except Exception as e:
        return f"Erro ao gerar áudio: {e}"

    audio_base64 = base64.b64encode(buffer.read()).decode()

    audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Seu navegador não suporta áudio.
        </audio>
    """
    return audio_html

# --- Função de tradução ---
def traduzir_texto(texto, origem="pt", destino="en"):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": texto, "langpair": f"{origem}|{destino}"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["responseData"]["translatedText"]
    except Exception as e:
        return f"Erro na API de tradução: {e}"

# --- Conjugação (continuar seu dicionário normalmente) ---
conjugacoes = {
    "be": {"Present": "am / is / are", "Past": "was / were", "Past Participle": "been", "Gerund": "being"},
    # ... (restante igual ao seu)
}