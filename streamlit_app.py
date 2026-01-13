import streamlit as st
from openai import OpenAI
import os

# CONFIGURAÇÃO DE SEGURANÇA
# A chave será lida das Environment Variables da Vercel
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="IA Star Studio", layout="wide")

# Estilização Dark Mode
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stButton>button { 
        background: linear-gradient(90deg, #8a2be2, #00d4ff); 
        color: white; border: none; border-radius: 12px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# BARRA LATERAL - DNA DA MODELO
with st.sidebar:
    st.header("🧬 DNA da Modelo")
    cabelo = st.text_input("Cabelo", "Longo, rosa pastel, ondulado")
    rosto = st.text_input("Rosto", "Olhos verdes, sardas leves, traços finos")
    estilo = st.text_input("Estilo", "Cyberpunk chic, roupas neon")
    st.divider()
    personalidade = st.selectbox("Personalidade", ["Debochada", "Meiga", "Alpha"])

# ÁREA CENTRAL
st.title("🎤 AI Content Studio")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 O que ela está fazendo?")
    briefing = st.text_area("Descreva a cena:", placeholder="Ex: No camarim antes de um show...")
    gerar = st.button("🚀 GERAR POST")

with col2:
    if gerar:
        if not api_key:
            st.error("ERRO: Configure a chave OPENAI_API_KEY na Vercel!")
        else:
            with st.spinner("✨ Criando..."):
                try:
                    # Imagem
                    prompt = f"Photo of a woman, {cabelo}, {rosto}, wearing {estilo}. {briefing}. 8k, realistic."
                    img_resp = client.images.generate(model="dall-e-3", prompt=prompt)
                    st.image(img_resp.data[0].url)
                    
                    # Texto
                    txt_resp = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"Legenda para: {briefing}. Persona: {personalidade}"}]
                    )
                    st.success(txt_resp.choices[0].message.content)
                except Exception as e:
                    st.error(f"Erro: {e}")
