import streamlit as st

# Captura limpa dos parâmetros que vêm da URL do anúncio
params = st.query_params

# Separa cada UTM individualmente para não misturar nas tabelas
utm_source = params.get("utm_source", "direto")
utm_campaign = params.get("utm_campaign", "geral")
utm_medium = params.get("utm_medium", "cpc")

# Exemplo de como salvar no seu log/banco de dados:
novo_registro = {
    "Origem": utm_source,       # Vai salvar 'facebook' ou 'google'
    "Campanha": utm_campaign,   # Vai salvar 'primavera' isoladamente
    "Status": "Capturado"
}
