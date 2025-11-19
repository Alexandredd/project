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

# --- Conjugação manual de 50 verbos irregulares ---
conjugacoes = {
    "be": {"Present": "am / is / are", "Past": "was / were", "Past Participle": "been", "Gerund": "being"},
    "become": {"Present": "become / becomes", "Past": "became", "Past Participle": "become", "Gerund": "becoming"},
    "begin": {"Present": "begin / begins", "Past": "began", "Past Participle": "begun", "Gerund": "beginning"},
    "break": {"Present": "break / breaks", "Past": "broke", "Past Participle": "broken", "Gerund": "breaking"},
    "bring": {"Present": "bring / brings", "Past": "brought", "Past Participle": "brought", "Gerund": "bringing"},
    "build": {"Present": "build / builds", "Past": "built", "Past Participle": "built", "Gerund": "building"},
    "buy": {"Present": "buy / buys", "Past": "bought", "Past Participle": "bought", "Gerund": "buying"},
    "catch": {"Present": "catch / catches", "Past": "caught", "Past Participle": "caught", "Gerund": "catching"},
    "choose": {"Present": "choose / chooses", "Past": "chose", "Past Participle": "chosen", "Gerund": "choosing"},
    "come": {"Present": "come / comes", "Past": "came", "Past Participle": "come", "Gerund": "coming"},
    "cost": {"Present": "cost / costs", "Past": "cost", "Past Participle": "cost", "Gerund": "costing"},
    "cut": {"Present": "cut / cuts", "Past": "cut", "Past Participle": "cut", "Gerund": "cutting"},
    "do": {"Present": "do / does", "Past": "did", "Past Participle": "done", "Gerund": "doing"},
    "draw": {"Present": "draw / draws", "Past": "drew", "Past Participle": "drawn", "Gerund": "drawing"},
    "drink": {"Present": "drink / drinks", "Past": "drank", "Past Participle": "drunk", "Gerund": "drinking"},
    "drive": {"Present": "drive / drives", "Past": "drove", "Past Participle": "driven", "Gerund": "driving"},
    "eat": {"Present": "eat / eats", "Past": "ate", "Past Participle": "eaten", "Gerund": "eating"},
    "fall": {"Present": "fall / falls", "Past": "fell", "Past Participle": "fallen", "Gerund": "falling"},
    "feel": {"Present": "feel / feels", "Past": "felt", "Past Participle": "felt", "Gerund": "feeling"},
    "find": {"Present": "find / finds", "Past": "found", "Past Participle": "found", "Gerund": "finding"},
    "fly": {"Present": "fly / flies", "Past": "flew", "Past Participle": "flown", "Gerund": "flying"},
    "forget": {"Present": "forget / forgets", "Past": "forgot", "Past Participle": "forgotten", "Gerund": "forgetting"},
    "get": {"Present": "get / gets", "Past": "got", "Past Participle": "got / gotten", "Gerund": "getting"},
    "give": {"Present": "give / gives", "Past": "gave", "Past Participle": "given", "Gerund": "giving"},
    "go": {"Present": "go / goes", "Past": "went", "Past Participle": "gone", "Gerund": "going"},
    "grow": {"Present": "grow / grows", "Past": "grew", "Past Participle": "grown", "Gerund": "growing"},
    "have": {"Present": "have / has", "Past": "had", "Past Participle": "had", "Gerund": "having"},
    "hear": {"Present": "hear / hears", "Past": "heard", "Past Participle": "heard", "Gerund": "hearing"},
    "hold": {"Present": "hold / holds", "Past": "held", "Past Participle": "held", "Gerund": "holding"},
    "keep": {"Present": "keep / keeps", "Past": "kept", "Past Participle": "kept", "Gerund": "keeping"},
    "know": {"Present": "know / knows", "Past": "knew", "Past Participle": "known", "Gerund": "knowing"},
    "leave": {"Present": "leave / leaves", "Past": "left", "Past Participle": "left", "Gerund": "leaving"},
    "lose": {"Present": "lose / loses", "Past": "lost", "Past Participle": "lost", "Gerund": "losing"},
    "make": {"Present": "make / makes", "Past": "made", "Past Participle": "made", "Gerund": "making"},
    "meet": {"Present": "meet / meets", "Past": "met", "Past Participle": "met", "Gerund": "meeting"},
    "pay": {"Present": "pay / pays", "Past": "paid", "Past Participle": "paid", "Gerund": "paying"},
    "put": {"Present": "put / puts", "Past": "put", "Past Participle": "put", "Gerund": "putting"},
    "read": {"Present": "read / reads", "Past": "read", "Past Participle": "read", "Gerund": "reading"},
    "run": {"Present": "run / runs", "Past": "ran", "Past Participle": "run", "Gerund": "running"},
    "say": {"Present": "say / says", "Past": "said", "Past Participle": "said", "Gerund": "saying"}
}
# --- Interação com o usuário ---
if menu == "Escrita ✍️":
    st.subheader("Corrija seu texto em inglês")
    texto = st.text_area("Digite seu texto em inglês:")
    if st.button("Corrigir"):
        sugestoes = corrigir_texto(texto)
        if sugestoes:
            for msg, sug in sugestoes:
                st.write(f"⚠️ {msg} → Sugestão: **{sug}**")
        else:
            st.success("✅ Nenhum erro encontrado!")

elif menu == "Escuta 🎧":
    st.subheader("Ouça frases em inglês")
    frase = st.text_input("Digite uma frase em inglês:")
    if st.button("Ouvir"):
        audio_html = gerar_audio(frase)
        st.markdown(audio_html, unsafe_allow_html=True)

elif menu == "Fala 🗣️":
    st.subheader("Pratique sua fala")
    frase = st.text_input("Digite uma frase em inglês para praticar:")
    if st.button("Ouvir e repetir"):
        audio_html = gerar_audio(frase)
        st.markdown(audio_html, unsafe_allow_html=True)
        st.info("🎤 Repita a frase em voz alta para treinar sua pronúncia.")

elif menu == "Tradução 🌍":
    st.subheader("Traduza entre Português ↔ Inglês")
    texto = st.text_area("Digite o texto para traduzir:")
    direcao = st.radio("Direção da tradução:", ["Português → Inglês", "Inglês → Português"])
    if st.button("Traduzir"):
        if direcao == "Português → Inglês":
            traducao = traduzir_texto(texto, origem="pt", destino="en")
        else:
            traducao = traduzir_texto(texto, origem="en", destino="pt")
        st.success(f"Tradução: {traducao}")

elif menu == "Conjugação 🔄":
    st.subheader("Conjugação de verbos irregulares")
    verbo = st.selectbox("Escolha um verbo:", list(conjugacoes.keys()))
    if verbo:
        tempos = conjugacoes[verbo]
        st.write(f"**Present:** {tempos['Present']}")
        st.write(f"**Past:** {tempos['Past']}")
        st.write(f"**Past Participle:** {tempos['Past Participle']}")
        st.write(f"**Gerund:** {tempos['Gerund']}")