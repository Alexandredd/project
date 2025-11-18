import streamlit as st
import requests
import difflib
from gtts import gTTS
import base64
from io import BytesIO

st.set_page_config(page_title="English Buddy", page_icon="📘")

st.title("English Buddy - Treine seu Inglês")

menu = st.sidebar.radio("Escolha uma habilidade:", [
    "Escrita ✍️", 
    "Escuta 🎧", 
    "Fala 🗣️", 
    "Tradução 🌍", 
    "Conjugação 🔄"])
# Função para correção de texto via API LanguageTool

def corrigir_texto(texto):
    url = "https://api.languagetool.org/v2/check"
    data = {"text": texto, "language": "en-US"}
    response = requests.post(url, data=data)
    result = response.json()
    sugestoes = []
    for match in result.get("matches", []):
        palavra_original = texto[match["offset"]:match["offset"] + match["length"]]
        melhores = []
        for r in match.get("replacements", []):
            sugestao = r["value"]
            similaridade = difflib.SequenceMatcher(None, palavra_original, sugestao).ratio()
            if similaridade > 0.5:  # ajustável
                melhores.append((sugestao, similaridade))
        if melhores:
            melhores.sort(key=lambda x: x[1], reverse=True)
            sugestoes.append((match["message"], melhores[0][0]))
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

# Função de tradução usando API MyMemory
def traduzir_texto(texto, origem="pt", destino="en"):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": texto, "langpair": f"{origem}|{destino}"}
    response = requests.get(url, params=params)
    result = response.json()
    return result["responseData"]["translatedText"]

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

elif menu == "Tradução 🌍":
    texto = st.text_area("Digite um texto para traduzir:")
    origem = st.selectbox("Idioma de origem:", ["pt", "en", "es", "fr"])
    destino = st.selectbox("Idioma de destino:", ["en", "pt", "es", "fr"])
    if st.button("Traduzir"):
        resultado = traduzir_texto(texto, origem, destino)
        st.subheader("Tradução:")
        st.write(resultado)

elif menu == "Conjugação 🔄":
    verbo = st.text_input("Digite um verbo em inglês (ex: go, eat, be):").lower()
    if st.button("Conjugar"):
        if verbo in conjugacoes:
            st.subheader(f"Conjugação de '{verbo}':")
            for tempo, forma in conjugacoes[verbo].items():
                st.write(f"**{tempo}**: {forma}")
        else:
            # Busca aproximada
            aproximado = buscar_verbo_aproximado(verbo, conjugacoes.keys())
            if aproximado:
                st.warning(f"Você digitou '{verbo}', mostrando conjugação de '{aproximado}':")
                for tempo, forma in conjugacoes[aproximado].items():
                    st.write(f"**{tempo}**: {forma}")
            else:
                st.error("Verbo não disponível ainda. Tente: be, go, eat, have, do, see, make, say, get, take, write, come, run, drink, know.")

def buscar_verbo_aproximado(verbo, lista_verbos):
    # Encontra o verbo mais parecido na lista
    candidatos = difflib.get_close_matches(verbo, lista_verbos, n=1, cutoff=0.6)
    return candidatos[0] if candidatos else None