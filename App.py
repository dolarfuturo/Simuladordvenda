import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Configuração da página
st.set_page_config(page_title="Ad Simulator Pro", layout="centered")

# CSS para tornar o visual IDÊNTICO às plataformas
st.markdown("""
    <style>
        .ad-container { background-color: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 15px; color: #000; font-family: sans-serif; max-width: 400px; margin: auto; }
        .sponsored { font-size: 12px; color: #65676b; margin-bottom: 5px; font-weight: 600; }
        .meta-image { width: 100%; height: 200px; background-color: #e4e6eb; display: flex; align-items: center; justify-content: center; color: #888; margin-bottom: 10px; }
        .meta-title { font-weight: 700; font-size: 16px; margin-bottom: 5px; }
        .google-link { color: #1a0dab; font-size: 18px; text-decoration: none; font-weight: 400; }
        .google-url { color: #006621; font-size: 14px; margin-bottom: 5px; }
        .btn-action { background-color: #007bff; color: white; border: none; padding: 10px; border-radius: 6px; width: 100%; font-weight: bold; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# Estado da sessão para logs
if 'conversoes' not in st.session_state:
    st.session_state.conversoes = pd.DataFrame(columns=["Data", "Plataforma", "Ação", "Campanha"])

def registrar_acao(plataforma, acao):
    novo_log = {"Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Plataforma": plataforma, "Ação": acao, "Campanha": "Teste_Sandbox"}
    st.session_state.conversoes = pd.concat([st.session_state.conversoes, pd.DataFrame([novo_log])], ignore_index=True)

# Interface Principal
st.title("📱 Ad Sandbox Simulator")
st.write("Simule comportamentos de usuários em Meta e Google Ads.")

tab1, tab2 = st.tabs(["Meta Ads (Instagram/FB)", "Google Search"])

# 1. META ADS
with tab1:
    st.markdown("""
        <div class="ad-container">
            <div class="sponsored">PATROCINADO • Meta Ads</div>
            <div class="meta-image">📸 IMAGEM DO ANÚNCIO</div>
            <div class="meta-title">Domine seus Dados em 30 Dias!</div>
            <div style="font-size: 14px; color: #444;">Escale seu ROI com nossa nova estratégia de dados.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Saiba Mais (Meta)", key="btn_meta"):
        registrar_acao("Meta", "Clique no Anúncio")
        st.session_state.clicked = True

# 2. GOOGLE ADS
with tab2:
    st.markdown("""
        <div class="ad-container" style="border:none; border-bottom:1px solid #ccc;">
            <div class="sponsored">Patrocinado</div>
            <a class="google-link" href="#">Escale seus Resultados - Ferramenta de Performance</a>
            <div class="google-url">https://seu-site.com.br/performance</div>
            <div style="font-size: 14px; color: #4d5156;">Aumente seu ROAS e otimize sua gestão de tráfego. Teste grátis hoje!</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Saiba Mais (Google)", key="btn_google"):
        registrar_acao("Google", "Clique no Anúncio")
        st.session_state.clicked = True

# LÓGICA DE LANDING PAGE
if st.session_state.get('clicked'):
    st.divider()
    st.subheader("🌐 Landing Page de Destino")
    st.info("Usuário clicou no anúncio. Aguardando conversão...")
    
    if st.button("🚀 REALIZAR COMPRA (Simular Conversão)"):
        registrar_acao("Universal", "Conversão de Compra")
        st.success("Conversão registrada com sucesso!")
        st.balloons()
        st.session_state.clicked = False

# EXPORTAÇÃO DOS DADOS (Portabilidade)
st.sidebar.header("⚙️ Exportação")
if not st.session_state.conversoes.empty:
    st.sidebar.write(f"Total de eventos: {len(st.session_state.conversoes)}")
    csv = st.session_state.conversoes.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        "📥 Baixar Logs de Teste (CSV)",
        data=csv,
        file_name="test_ads_data.csv",
        mime="text/csv",
    )
