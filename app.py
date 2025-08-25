import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import get_trending_tokens, analyze_token

st.set_page_config(page_title="Solana Meme Scouteeee", layout="wide")

st.title("🚀 Solana Meme Scout")
st.markdown("Style Phantom • Scanner de vrais meme coins Solana viashhsklfh Dexscreener.")

# Sidebar
st.sidebar.header("⚙️ Paramètres")
min_liquidity = st.sidebar.slider("Liquidité minimum (USD)", 50, 500000, 5000)
min_volume = st.sidebar.slider("Volume minimum (24h, USD)", 1000, 10000000, 10000)

# Récupération des données
coins = get_trending_tokens(min_liquidity=min_liquidity, min_volume=min_volume)

if coins.empty:
    st.error("Aucun coin trouvé avec ces critères.")
else:
    st.subheader("🔥 Meme Coins détectés sur Solana")
    st.dataframe(coins)

    choix = st.selectbox("Choisir un coin pour voir le graphique", coins["symbol"])
    token = coins[coins["symbol"] == choix].iloc[0]

    token_data = analyze_token(token["address"])

    if token_data is not None:
        st.subheader(f"Analyse de {choix}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Prix actuel", f"{token_data['price']:.6f} $")
            st.metric("📊 Volume 24h", f"{token_data['volume_24h']:,} $")
        with col2:
            st.metric("🏦 Liquidité", f"{token_data['liquidity']:,} $")
            st.metric("👥 Holders (txns 24h)", token_data["holders"])

        # Historique simulé
        history = token_data["history"]
        fig = px.line(history, x="time", y="price", title=f"Évolution du prix de {choix}")
        st.plotly_chart(fig, use_container_width=True)

        # 🔗 Bouton "Acheter sur Jupiter"
        jupiter_url = f"https://jup.ag/swap/SOL-{token['address']}"
        st.markdown(f"[👉 Acheter {choix} sur Jupiter]({jupiter_url})", unsafe_allow_html=True)
