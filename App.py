import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Gerenciador de Anúncios Sandbox", layout="wide")

# Arquivos de Dados
ADS_DB = "meus_anuncios.csv"
LOGS_DB = "logs_auditoria.csv"

# --- FUNÇÕES DE SISTEMA ---
def salvar_anuncio(data):
    df = pd.DataFrame([data])
    if os.path.exists(ADS_DB):
        df.to_csv(ADS_DB, mode='a', header=False, index=False)
    else:
        df.to_csv(ADS_DB, index=False)

def logar_clique(campanha, link, ip):
    data = {
        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Campanha": campanha,
        "Link_Destino": link,
        "IP_Visitante": ip
    }
    df = pd.DataFrame([data])
    if os.path.exists(LOGS_DB):
        df.to_csv(LOGS_DB, mode='a', header=False, index=False)
    else:
        df.to_csv(LOGS_DB, index=False)

# --- INTERFACE ---
st.title("🧪 Sandbox: Gerenciador de Anúncios")

tab1, tab2, tab3 = st.tabs(["🏗️ Criar Anúncio", "📱 Simular Rede (Feed)", "📊 Auditoria (Recebimento de Dados)"])

with tab1:
    st.header("Configurar Nova Campanha")
    with st.form("criar_anuncio"):
        titulo = st.text_input("Título do Anúncio")
        link = st.text_input("Link do seu Ecossistema (URL final)")
        campanha = st.text_input("Nome da Campanha (ID)")
        if st.form_submit_button("Criar e Publicar na Simulação"):
            salvar_anuncio({"titulo": titulo, "link": link, "campanha": campanha})
            st.success("Anúncio criado e 'publicado' no simulador!")

with tab2:
    st.header("Simulador de Rede (Onde o cliente clica)")
    if os.path.exists(ADS_DB):
        anuncios = pd.read_csv(ADS_DB)
        for i, row in anuncios.iterrows():
            st.markdown(f"---")
            st.write(f"**Anúncio Ativo:** {row['titulo']}")
            st.write(f"Campanha: {row['campanha']}")
            # Botão que simula o clique no anúncio real
            if st.button(f"Simular Clique em: {row['titulo']}", key=i):
                # Captura IP
                ip = st.context.headers.get("X-Forwarded-For", "192.168.0.1")
                logar_clique(row['campanha'], row['link'], ip)
                st.info(f"CLIQUE EFETUADO! O dado foi enviado para auditoria.")
                st.rerun()
    else:
        st.warning("Nenhum anúncio criado. Vá na aba 'Criar Anúncio'.")

with tab3:
    st.header("Painel de Auditoria (Recebimento de Dados)")
    if os.path.exists(LOGS_DB):
        logs = pd.read_csv(LOGS_DB)
        st.dataframe(logs, use_container_width=True)
        if st.button("Limpar Auditoria"):
            os.remove(LOGS_DB)
            st.rerun()
    else:
        st.info("Aguardando cliques... Crie um anúncio e simule um clique na aba 2.")
