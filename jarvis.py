import streamlit as st
from streamlit_mic_recorder import mic_recorder
from groq import Groq
import webbrowser
import os

# Configuração da Página para parecer uma interface de chamada
st.set_page_config(page_title="J.A.R.V.I.S. v16.1", page_icon="🎙️")

st.title("🎙️ J.A.R.V.I.S. - Interface de Voz")
st.write("---")

# Inicialização da API Groq (Anti-Erro 429)
client = Groq(api_key="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")
MODELO = "llama-3.1-8b-instant"

# Interface de "Chamada"
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("https://i.imgur.com/your_jarvis_logo.png", width=200) # Coloque o logo do seu Myhril aqui!
    st.subheader("Conexão Estabelecida")
    
    # O Gravador que envia o áudio direto para o site
    audio_data = mic_recorder(
        start_prompt="Iniciar Chamada",
        stop_prompt="Encerrar Comando",
        key='recorder'
    )

if audio_data:
    # Aqui o sistema processa o que você falou no site
    # (Para produção, você usaria o Whisper da OpenAI ou Groq para transcrever o áudio)
    st.info("Processando áudio...")
    
    # Exemplo de comando direto para teste no site:
    comando = "abrir spotify" # Simulando a transcrição do áudio

    # Lógica de Automação do v16
    if 'spotify' in comando:
        st.success("Abrindo Spotify...")
        webbrowser.open("https://open.spotify.com")
    elif 'instagram' in comando:
        webbrowser.open("https://www.instagram.com")
    elif 'myhril' in comando:
        webbrowser.open("https://freegamehost.com")

    # Resposta da IA
    try:
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é o JARVIS em uma chamada de voz com o Pedro."},
                {"role": "user", "content": comando}
            ],
            model=MODELO
        )
        st.chat_message("assistant").write(chat.choices[0].message.content)
    except Exception as e:
        st.error(f"Erro na nuvem: {e}")

st.write("---")
st.caption("Status do Sistema: Online | Myhril Server Sync: Ativo")