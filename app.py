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
            if similaridade > 0.5:
                melhores.append((sugestao, similaridade))
        if melhores:
            melhores.sort(key=lambda x: x[1], reverse=True)
            sugestoes.append((match["message"], melhores[0][0]))
    return sugestoes

# --- Função de áudio ---
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

# --- Função de tradução ---
def traduzir_texto(texto, origem="pt", destino="en"):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": texto, "langpair": f"{origem}|{destino}"}
    response = requests.get(url, params=params)
    result = response.json()
    return result["responseData"]["translatedText"]

# --- Conjugação manual de verbos ---
conjugacoes = {
    "be": {"Present": "am / is / are", "Past": "was / were", "Past Participle": "been", "Gerund": "being"},
    "go": {"Present": "go / goes", "Past": "went", "Past Participle": "gone", "Gerund": "going"},
    "eat": {"Present": "eat / eats", "Past": "ate", "Past Participle": "eaten", "Gerund": "eating"},
    "have": {"Present": "have / has", "Past": "had", "Past Participle": "had", "Gerund": "having"},
    "do": {"Present": "do / does", "Past": "did", "Past Participle": "done", "Gerund": "doing"},
    "see": {"Present": "see / sees", "Past": "saw", "Past Participle": "seen", "Gerund": "seeing"},
    "make": {"Present": "make / makes", "Past": "made", "Past Participle": "made", "Gerund": "making"},
    "say": {"Present": "say / says", "Past": "said", "Past Participle": "said", "Gerund": "saying"},
    "get": {"Present": "get / gets", "Past": "got", "Past Participle": "got / gotten", "Gerund": "getting"},
    "take": {"Present": "take / takes", "Past": "took", "Past Participle": "taken", "Gerund": "taking"},
    "write": {"Present": "write / writes", "Past": "wrote", "Past Participle": "written", "Gerund": "writing"},
    "come": {"Present": "come / comes", "Past": "came", "Past Participle": "come", "Gerund": "coming"},
    "run": {"Present": "run / runs", "Past": "ran", "Past Participle": "run", "Gerund": "running"},
    "drink": {"Present": "drink / drinks", "Past": "drank", "Past Participle": "drunk", "Gerund": "drinking"},
    "know": {"Present": "know / knows", "Past": "knew", "Past Participle": "known", "Gerund": "knowing"}
}

# --- Função de busca aproximada ---
def buscar_verbo_aproximado(verbo, lista_verbos):
    candidatos = difflib.get_close_matches(verbo, lista_verbos, n=1, cutoff=0.6)
    return candidatos[0] if candidatos else None

# --- Interface ---
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
    st.caption("💡 Dica: digite frases completas para melhorar a correção.")

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