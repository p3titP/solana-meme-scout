import streamlit as st
import pandas as pd
import plotly.express as px
from utils import fetch_top_meme_coins, fetch_price_history

st.set_page_config(page_title="Solana Meme Scout", layout="wide")

st.title("🚀 Solana Meme Scout")
st.markdown("Style Phantom • Scanner de meme coins Solana avec graphiques.")

# Sidebar
st.sidebar.header("⚙️ Paramètres")
limit = st.sidebar.slider("Nombre de coins affichés", 5, 50, 10)

# Récupération des données
coins = fetch_top_meme_coins(limit=limit)

if coins.empty:
    st.error("Aucun coin trouvé. Vérifie tes clés API dans `.env`.")
else:
    st.subheader("🔥 Top Meme Coins détectés")
    st.dataframe(coins)

    choix = st.selectbox("Choisir un coin pour voir le graphique", coins["symbol"])
    token = coins[coins["symbol"] == choix].iloc[0]

    # Historique de prix
    history = fetch_price_history(token["address"])
    if not history.empty:
        fig = px.line(history, x="time", y="price", title=f"Évolution de {choix}")
        st.plotly_chart(fig, use_container_width=True)
