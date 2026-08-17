import streamlit as st
import urllib.parse

st.set_page_config(page_title="Ad Creator Sandbox", layout="wide")

# CSS para previews fiéis
st.markdown("""
    <style>
        .preview-container { background: white; border: 1px solid #ddd; padding: 20px; border-radius: 8px; color: black; max-width: 400px; }
        .meta-ad { font-family: Helvetica, Arial, sans-serif; }
        .google-ad { font-family: Roboto, Arial, sans-serif; }
        .sponsored { color: #65676b; font-size: 12px; font-weight: 600; margin-bottom: 8px; }
        .headline { font-weight: 700; font-size: 16px; margin-bottom: 4px; }
        .google-link { color: #1a0dab; font-size: 18px; text-decoration: none; }
        .google-url { color: #006621; font-size: 14px; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ Sandbox de Criação de Anúncios")
st.write("Crie seu anúncio, configure as UTMs e valide a integração com seu ecossistema.")

# --- BARRA LATERAL: O CRIADOR ---
with st.sidebar:
    st.header("1. Configurar Anúncio")
    plataforma = st.selectbox("Plataforma", ["Meta Ads (IG/FB)", "Google Ads (Search)"])
    headline = st.text_input("Título (Headline)", "Título do seu Anúncio aqui")
    body = st.text_area("Descrição / Corpo do Anúncio", "Texto persuasivo de vendas...")
    
    st.header("2. Destino e Rastreamento")
    url_base = st.text_input("URL do seu Ecossistema", "https://seu-dominio.com.br")
    utm_campaign = st.text_input("UTM Campaign (ID da Campanha)", "campanha_teste_01")
    utm_source = st.text_input("UTM Source", "facebook" if "Meta" in plataforma else "google")

# --- LÓGICA DE MONTAGEM DO LINK ---
query_params = {
    "utm_source": utm_source,
    "utm_medium": "cpc",
    "utm_campaign": utm_campaign
}
url_final = f"{url_base}?{urllib.parse.urlencode(query_params)}"

# --- ÁREA PRINCIPAL: PREVIEW ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Visualização (Preview)")
    if "Meta" in plataforma:
        st.markdown(f"""
            <div class="preview-container meta-ad">
                <div class="sponsored">PATROCINADO • Meta Ads</div>
                <div style="background:#ddd; height:200px; display:flex; align-items:center; justify-content:center; margin-bottom:10px;">IMAGEM/VÍDEO</div>
                <div class="headline">{headline}</div>
                <div style="font-size: 14px;">{body}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="preview-container google-ad">
                <div class="sponsored">Patrocinado</div>
                <div class="google-link">{headline}</div>
                <div class="google-url">{url_base}</div>
                <div style="font-size: 14px; color: #4d5156;">{body}</div>
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("Link para Teste")
    st.write("Copie este link para testar o rastreamento no seu ecossistema:")
    st.code(url_final, language="text")
    
    if st.button("Abrir link para simular tráfego"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url={url_final}">', unsafe_allow_html=True)
        st.success("Redirecionando para o ambiente de teste...")

    st.info("💡 **Dica:** Ao abrir este link, seu ecossistema deve capturar os parâmetros `utm_source` e `utm_campaign` automaticamente.")
