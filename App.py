import streamlit as st
import urllib.parse

st.set_page_config(page_title="Gerenciador de Anúncios", layout="wide")

st.title("🚀 Gerenciador de Anúncios - Sandbox")
st.write("Crie sua campanha e dispare o tráfego para o seu Ecossistema.")

with st.sidebar:
    st.header("Configuração da Campanha")
    # AQUI VOCÊ COLA O LINK DO SEU DASHBOARD REAL
    url_dashboard = st.text_input("URL do seu Ecossistema (Dashboard)", "https://ecosistem.streamlit.app")
    
    plataforma = st.selectbox("Plataforma", ["Meta Ads (Facebook/Instagram)", "Google Ads"])
    utm_source = "facebook" if "Meta" in plataforma else "google"
    utm_campaign = st.text_input("Nome da Campanha (UTM)", "primavera")
    utm_medium = st.text_input("Mídia (UTM)", "cpc")

# Lógica de montagem
query_params = {
    "utm_source": utm_source,
    "utm_medium": utm_medium,
    "utm_campaign": utm_campaign
}
url_final = f"{url_dashboard}/?{urllib.parse.urlencode(query_params)}"

# Exibição
st.subheader("Simulação de Anúncio")
st.markdown(f"""
    <div style="background:white; border:1px solid #ddd; padding:20px; border-radius:8px; color:black;">
        <div style="font-size:12px; font-weight:bold; color:gray;">PATROCINADO • {plataforma}</div>
        <div style="font-weight:bold; font-size:16px;">Campanha: {utm_campaign}</div>
        <div style="font-size:14px;">Clique para testar o rastreamento real.</div>
    </div>
""", unsafe_allow_html=True)

st.write("---")
st.success(f"Link gerado: {url_final}")
st.link_button("🚀 IR PARA O ECOSISTEMA (Simular Tráfego Real)", url_final, use_container_width=True)
