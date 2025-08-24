import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_trending_tokens, analyze_token

st.set_page_config(page_title="Solana Meme Scout", layout="wide")

st.title("🚀 Solana Meme Scout")
st.markdown("Style Phantom • Scanner de meme coins Solana avec graphiques.")

# Sidebar
st.sidebar.header("⚙️ Paramètres")
min_liquidity = st.sidebar.slider("Liquidité minimum (SOL)", 50, 5000, 500)
min_volume = st.sidebar.slider("Volume minimum (24h)", 1000, 100000, 10000)

# Récupération des données (fake data pour démo)
coins = get_trending_tokens(min_liquidity=min_liquidity, min_volume=min_volume)

if coins.empty:
    st.error("Aucun coin trouvé avec ces critères.")
else:
    st.subheader("🔥 Meme Coins détectés")
    st.dataframe(coins)

    choix = st.selectbox("Choisir un coin pour voir le graphique", coins["symbol"])
    token_data = analyze_token(choix)

    if token_data is not None:
        st.subheader(f"Analyse de {choix}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Prix actuel", f"{token_data['price']}$")
            st.metric("📊 Volume 24h", f"{token_data['volume_24h']}$")
        with col2:
            st.metric("🏦 Liquidité", f"{token_data['liquidity']}$")
            st.metric("👥 Holders", token_data["holders"])

        # Historique de prix
        history = token_data["history"]
        fig = px.line(history, x="time", y="price", title=f"Évolution du prix de {choix}")
        st.plotly_chart(fig, use_container_width=True)
