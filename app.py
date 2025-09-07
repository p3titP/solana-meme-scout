import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import get_trending_tokens, analyze_token  # ✅ corrigé (plus utils !)

st.set_page_config(page_title="Solana Meme Scout", layout="wide")

st.title("🚀 Solana Meme Scout")
st.markdown("Style Phantom • Scanner les meme coins Solana avec graphiques + score potentiel.")


# 🔍 Récupération des tokens
tokens = get_trending_tokens(limit=15)

if tokens.empty:
    st.error("Aucun coin trouvé (erreur API ?)")
else:
    st.subheader("🔥 Meme Coins détectés avec Score")

    # affichage style "cards" avec logos
    for _, row in tokens.iterrows():
        cols = st.columns([1, 3, 2])
        with cols[0]:
            if row.get("logo"):
                st.image(row["logo"], width=60)
            else:
                st.write("🪙")
        with cols[1]:
            st.markdown(f"### {row['symbol']}")
            st.markdown(
                f"- 💰 Prix : **{row['price']:.6f} USD**\n"
                f"- 📈 Volume 24h : **{row['volume_24h']}**\n"
                f"- 💦 Liquidité : **{row['liquidity']}**"
            )
        with cols[2]:
            st.metric("⭐ Score", f"{row['score']}/10")

        st.divider()

    # sélection d’un token
    choix = st.selectbox("Choisir un coin pour voir l’analyse", tokens["symbol"])
    token = tokens[tokens["symbol"] == choix].iloc[0]

    details = analyze_token(token["address"])
    if details:
        st.markdown(f"""
        ## 📊 Analyse de **{token['symbol']}**
        - 💰 Prix actuel : **{details['price']} USD**
        - 📈 Volume 24h : **{details['volume_24h']}**
        - 💦 Liquidité : **{details['liquidity']}**
        - 👥 Holders (approx) : **{details['holders']}**
        - 🏷️ FDV : **{details['fdv']}**
        """)

        # Graphique historique (ici factice car DexScreener ne donne pas l’historique complet)
        if not details["history"].empty:
            fig = px.line(details["history"], x="time", y="price", title=f"Évolution de {token['symbol']}")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Impossible de récupérer l’analyse de ce token.")
