import streamlit as st
import plotly.express as px
from helpers import get_trending_tokens, analyze_token

st.set_page_config(page_title="Solana Meme Scout", layout="wide")

st.title("🚀 Solana Meme Scout (via Dexscreener)")
st.markdown("Scanner les **meme coins Solana** en tendance avec graphiques + score potentiel.")

# 🔍 Récupération des tokens trending
tokens = get_trending_tokens()

if tokens.empty:
    st.error("Aucun coin trouvé (erreur API ?).")
else:
    st.subheader("🔥 Meme Coins détectés avec Score")
    st.dataframe(tokens)

    choix = st.selectbox("Choisir un coin pour voir l’analyse", tokens["symbol"])
    token = tokens[tokens["symbol"] == choix].iloc[0]

    # 📊 Analyse détaillée
    details = analyze_token(token["id"])
    if details:
        st.markdown(f"""
        ### 📊 Analyse de **{token['symbol']}**
        - 💰 Prix actuel : **{details['price']} USD**
        - 📈 Volume 24h : **{details['volume_24h']}**
        - 💦 Liquidité : **{details['liquidity']}**
        - 🏷️ FDV : **{token['fdv']}**
        - ⭐ Score potentiel : **{token['score']}/10**
        """)

        # Graphique historique (⚠️ vide pour l’instant avec Dexscreener)
        if not details["history"].empty:
            fig = px.line(details["history"], x="time", y="price", title=f"Évolution de {token['symbol']}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Pas d’historique disponible via Dexscreener (limitation API).")
    else:
        st.warning("Impossible de récupérer l’analyse de ce token.")
