import streamlit as st
import requests
from gtts import gTTS
import base64
from io import BytesIO

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

# Função para gerar áudio embutido
def gerar_audio(frase):
    tts = gTTS(frase, lang="en")
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    audio_base64 = base64.b64encode(buffer.read()).decode()
    audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Seu navegador não suporta áudio.
        </audio>
    """
    return audio_html

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
        audio_html = gerar_audio(frase)
        st.markdown(audio_html, unsafe_allow_html=True)

elif menu == "Fala 🗣️":
    st.info("Reconhecimento de fala será implementado em breve.")