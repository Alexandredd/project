import streamlit as st
import requests
from gtts import gTTS
import os

st.set_page_config(page_title="English Buddy", page_icon="📘")

st.title("English Buddy - Treine seu Inglês")

menu = st.sidebar.radio("Escolha uma habilidade:", ["Escrita ✍️", "Escuta 🎧", "Fala 🗣️"])

# Função para correção de texto via API LanguageTool
def corrigir_texto(texto):
    url = "https://api.languagetool.org/v2/check"
    data = {"text": texto, "language": "en-US"}
    response = requests.post(url, data=data)
    result = response.json()
    sugestoes = []
    for match in result.get("matches", []):
        if match["replacements"]:
            sugestoes.append((match["message"], match["replacements"][0]["value"]))
    return sugestoes

if menu == "Escrita ✍️":
    texto = st.text_area("Digite um texto em inglês para correção:")
    if st.button("Corrigir"):
        sugestoes = corrigir_texto(texto)
        if sugestoes:
            st.subheader("Sugestões de correção:")
            for msg, rep in sugestoes:
                st.write(f"- {msg} → **{rep}**")
        else:
            st.success("Nenhum erro encontrado!")

elif menu == "Escuta 🎧":
    frase = st.text_input("Digite uma frase em inglês para ouvir:")
    if st.button("Ouvir"):
        tts = gTTS(frase, lang="en")
        tts.save("audio.mp3")
        st.audio("audio.mp3")

elif menu == "Fala 🗣️":
    st.info("Reconhecimento de fala será implementado em breve.")