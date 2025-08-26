import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import get_trending_tokens, analyze_token

st.set_page_config(page_title="Solana Meme Scout", layout="wide")

st.title("🚀 Solana Meme Scout")
st.markdown("Style Phantom • Scanner de vrais meme coins Solana avec graphiques + score potentiel.")

# Récupération des tokens
tokens = get_trending_tokens()

if tokens.empty:
    st.error("Aucun coin trouvé (erreur API ?).")
else:
    st.subheader("🔥 Meme Coins détectés avec Score")
    st.dataframe(tokens)

    choix = st.selectbox("Choisir un coin pour voir l’analyse", tokens["symbol"])
    token = tokens[tokens["symbol"] == choix].iloc[0]

    # Analyse détaillée
    details = analyze_token(token["symbol"])
    if details:
        st.markdown(f"""
        ### 📊 Analyse de **{token['symbol']}**
        - 💰 Prix actuel : **{details['price']} USD**
        - 📈 Volume 24h : **{details['volume_24h']}**
        - 💦 Liquidité : **{details['liquidity']}**
        - 👥 Holders : **{details['holders']}**
        - ⭐ Score potentiel : **{details['score']}/10**
        """)

        # Graphique historique
        fig = px.line(details["history"], x="time", y="price", title=f"Évolution de {token['symbol']}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Impossible de récupérer l’analyse de ce token.")
