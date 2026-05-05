import streamlit as st
from streamlit_mic_recorder import mic_recorder
from groq import Groq
import webbrowser
import PIL.Image
import io

# Configuração de Estilo "Discord Call"
st.set_page_config(page_title="J.A.R.V.I.S. v17.0", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #1e1f22; color: #dbdee1; }
    .stButton>button { border-radius: 20px; background-color: #5865F2; color: white; }
    .jarvis-circle {
        width: 150px; height: 150px; border: 4px solid #00d4ff;
        border-radius: 50%; margin: 0 auto; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% {transform: scale(0.95);} 70% {transform: scale(1);} 100% {transform: scale(0.95);} }
    </style>
    """, unsafe_allow_html=True)

# Inicialização
client = Groq(api_key=st.secrets["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"])

st.title("🎙️ J.A.R.V.I.S. v17.0 - Live Operations")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="jarvis-circle"></div>', unsafe_allow_html=True)
    # BOTÃO DE VISÃO: Captura a tela/câmera para o JARVIS "ver"
    foto_tela = st.camera_input("Compartilhar Visão (Clique para o JARVIS ver)")

with col_right:
    st.subheader("Controle de Sistema")
    entrada_texto = st.text_input("Comando de texto:", placeholder="Digite aqui...")
    # Gravador de voz para a chamada
    audio_voz = mic_recorder(start_prompt="🎙️ Iniciar Fala", stop_prompt="🛑 Enviar", key='voz')

# --- LÓGICA DE EXECUÇÃO (O CORAÇÃO DO V15 + V17) ---

def processar_comando(comando, imagem=None):
    cmd = comando.lower()
    
    # 1. Automações do v15 (Apps e Links)
    if 'spotify' in cmd:
        webbrowser.open("https://open.spotify.com")
        st.success("Spotify aberto, senhor.")
    elif 'youtube' in cmd:
        webbrowser.open("https://youtube.com")
    elif 'roblox' in cmd:
        webbrowser.open("https://www.roblox.com")
    elif 'myhril' in cmd:
        webbrowser.open("https://freegamehost.com") # Link do seu server
    elif 'pesquisar' in cmd:
        busca = cmd.replace('pesquisar', '').strip()
        webbrowser.open(f"https://www.google.com/search?q={busca}")
    
    # 2. Resposta da IA com Visão (v17)
    # Se houver imagem, o JARVIS comenta o que está vendo
    role_content = "Você é o JARVIS. Pedro está em uma chamada de vídeo com você."
    if imagem:
        role_content += " Analise a imagem que ele te enviou e responda sobre ela."

    try:
        # Usando o modelo Vision da Groq
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": role_content},
                {"role": "user", "content": cmd}
            ],
            model="llama-3.2-11b-vision-preview" # Modelo que "vê"
        )
        st.chat_message("assistant").write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Erro no processamento: {e}")

# Gatilhos de execução
if entrada_texto:
    processar_comando(entrada_texto, foto_tela)
elif audio_voz:
    # Simulação de transcrição para o teste
    processar_comando("comando de voz detectado", foto_tela)

st.write("---")
st.caption("Status: Conectado ao Myhril Server | v17.0 Edition")
