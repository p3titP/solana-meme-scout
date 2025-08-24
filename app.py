import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_trending_tokens, analyze_token

st.set_page_config(
    page_title="Solana Meme Scout",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🚀 Solana Meme Scout")
st.markdown("Reste informé des nouveaux **meme coins Solana** avec gros potentiel 📈")

# Sidebar
st.sidebar.header("⚙️ Paramètres")
min_liquidity = st.sidebar.slider("Liquidité minimum (SOL)", 50, 5000, 500)
min_volume = st.sidebar.slider("Volume minimum (24h)", 1000, 100000, 10000)

# Charger les tokens
st.sidebar.write("📡 Récupération des données en cours...")
tokens = get_trending_tokens(min_liquidity, min_volume)

if tokens.empty:
    st.warning("Aucun token ne correspond aux critères.")
else:
    st.success(f"{len(tokens)} tokens trouvés ✅")

    # Tableau principal
    st.dataframe(tokens, use_container_width=True)

    # Sélection d’un token
    choix = st.selectbox("🔎 Choisir un token à analyser", tokens["symbol"])
    token_data = analyze_token(choix)

    if token_data is not None:
        st.subheader(f"Analyse détaillée : {choix}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("💰 Prix actuel", f"{token_data['price']} $")
            st.metric("📊 Volume 24h", f"{token_data['volume_24h']} $")

        with col2:
            st.metric("🏦 Liquidité", f"{token_data['liquidity']} $")
            st.metric("👥 Holders", token_data["holders"])

        # Graphique prix
        fig = px.line(
            token_data["history"],
            x="time",
            y="price",
            title=f"Évolution du prix ({choix})",
            template="plotly_dark",
        )
        st.plotly_chart(fig, use_container_width=True)
