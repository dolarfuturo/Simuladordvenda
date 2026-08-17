import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.parse

st.set_page_config(page_title="Simulador Real de Anúncios e Vendas", layout="wide")

# Arquivos de dados locais
LOGS_FILE = "logs_cliques.csv"
VENDAS_FILE = "logs_vendas.csv"

# Verifica se a URL tem parâmetros de tráfego (Simulando o clique real no anúncio)
params = st.query_params
destino = params.get("destino", "")

# --- MODO LANDING PAGE (O usuário clicou no anúncio e caiu aqui) ---
if destino == "landing":
    utm_campaign = params.get("utm_campaign", "geral")
    utm_source = params.get("utm_source", "direto")
    
    # Captura IP
    headers = st.context.headers
    user_ip = headers.get("X-Forwarded-For", "127.0.0.1")
    
    # Registra o clique automaticamente na primeira visualização da sessão
    if "clique_registrado" not in st.session_state:
        clique_data = {
            "Data_Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "IP": user_ip,
            "Origem": utm_source,
            "Campanha": utm_campaign,
            "Acao": "Clique / Visualizacao"
        }
        df_clique = pd.DataFrame([clique_data])
        if os.path.exists(LOGS_FILE):
            df_c = pd.read_csv(LOGS_FILE)
            df_c = pd.concat([df_c, df_clique], ignore_index=True)
        else:
            df_c = df_clique
        df_c.to_csv(LOGS_FILE, index=False)
        st.session_state.clique_registrado = True

    st.title("🛒 Ecossistema / Página de Vendas")
    st.info(f"🛰️ Tráfego capturado via anúncio! Origem: **{utm_source}** | Campanha: **{utm_campaign}** | IP: **{user_ip}**")
    
    st.subheader("Produto: Kit Primavera Master")
    st.write("O seu clique e o seu IP foram registrados com sucesso no sistema de auditoria.")
    
    if st.button("🚀 COMPRAR AGORA (Simular Conversão/Venda)", use_container_width=True):
        venda_data = {
            "Data_Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "IP": user_ip,
            "Campanha": utm_campaign,
            "Origem": utm_source,
            "Valor": 297.00,
            "Status": "Aprovado"
        }
        df_venda = pd.DataFrame([venda_data])
        if os.path.exists(VENDAS_FILE):
            df_v = pd.read_csv(VENDAS_FILE)
            df_v = pd.concat([df_v, df_venda], ignore_index=True)
        else:
            df_v = df_venda
        df_v.to_csv(VENDAS_FILE, index=False)
        
        st.success("🎉 Venda realizada e computada com sucesso no painel principal!")
        st.balloons()
        
    st.stop()

# --- MODO CENTRAL DE ANÚNCIOS E DASHBOARD ---
st.title("🌐 Simulador Completo de Rede de Anúncios")
st.write("Crie anúncios reais, dispare tráfego simulado com rastreamento de IP e acompanhe conversões.")

tab1, tab2, tab3 = st.tabs(["🛠️ 1. Criar Anúncio", "📊 2. Logs de Cliques & IP", "💰 3. Dashboard de Vendas"])

with tab1:
    col_A, col_B = st.columns(2)
    with col_A:
        st.subheader("Configuração do Anúncio")
        plataforma = st.selectbox("Plataforma", ["Meta Ads (IG/FB)", "Google Ads (Search)"])
        headline = st.text_input("Título", "Domine seus Dados na Primavera")
        body = st.text_area("Texto", "Escale seu tráfego com nossa estratégia.")
        utm_campaign = st.text_input("Nome da Campanha (UTM)", "primavera")
        utm_source = "facebook" if "Meta" in plataforma else "google"
        
    with col_B:
        st.subheader("Preview e Link de Disparo")
        
        # Monta os parâmetros de rastreamento apontando para a própria aplicação
        query_params = {
            "destino": "landing",
            "utm_source": utm_source,
            "utm_medium": "cpc",
            "utm_campaign": utm_campaign
        }
        
        link_simulado = f"/?{urllib.parse.urlencode(query_params)}"
        
        st.markdown(f"""
            <div style="background:white; border:1px solid #ddd; padding:15px; border-radius:8px; color:black;">
                <div style="font-size:12px; color:gray; font-weight:bold;">PATROCINADO • {plataforma}</div>
                <div style="font-weight:bold; font-size:16px; margin-top:5px;">{headline}</div>
                <div style="font-size:14px; color:#444; margin-top:5px;">{body}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("### Link Gerado:")
        st.code(link_simulado, language="text")
        
        # Botão que simula o usuário clicando no anúncio real
        st.link_button("🚀 Simular Clique no Anúncio (Ir para Landing Page)", link_simulado, use_container_width=True)

with tab2:
    st.subheader("Auditoria de Cliques e IPs")
    if os.path.exists(LOGS_FILE):
        df_logs = pd.read_csv(LOGS_FILE)
        st.dataframe(df_logs, use_container_width=True)
        if st.button("Limpar Logs de Cliques"):
            os.remove(LOGS_FILE)
            st.rerun()
    else:
        st.info("Nenhum clique registrado. Clique no botão de teste do anúncio para gerar dados.")

with tab3:
    st.subheader("Painel Financeiro e Conversões")
    if os.path.exists(VENDAS_FILE):
        df_vendas = pd.read_csv(VENDAS_FILE)
        col1, col2 = st.columns(2)
        col1.metric(label="Total de Vendas", value=len(df_vendas))
        col2.metric(label="Faturamento", value=f"R$ {df_vendas['Valor'].sum():.2f}")
        st.dataframe(df_vendas, use_container_width=True)
        if st.button("Limpar Dados de Vendas"):
            os.remove(VENDAS_FILE)
            st.rerun()
    else:
        st.info("Nenhuma venda registrada. Simule uma compra na página de destino.")
