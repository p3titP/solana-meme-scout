import streamlit as st
from helpers import get_trending_tokens, analyze_token

st.set_page_config(page_title="Solana Meme Scout", layout="wide")

st.title("🚀 Solana Meme Scout (Meme Coins Style)")

tokens = get_trending_tokens()

if tokens.empty:
    st.error("Aucun coin trouvé (erreur API ?).")
else:
    st.subheader("🔥 Meme Coins en tendance")

    # --- AFFICHAGE LISTE STYLE CARTES ---
    for _, row in tokens.iterrows():
        with st.container():
            cols = st.columns([1, 3, 3, 3, 2])
            with cols[0]:
                if row["logo"]:
                    st.image(row["logo"], width=40)
                else:
                    st.text("🚀")
            with cols[1]:
                st.markdown(f"**{row['symbol']}**")
                st.caption(row["name"])
            with cols[2]:
                st.markdown(f"💰 **Prix :** ${row['price']:.6f}" if row['price'] else "💰 Prix : N/A")
                st.markdown(f"📈 **Volume 24h :** ${row['volume_24h']:,}" if row['volume_24h'] else "📈 Volume : N/A")
            with cols[3]:
                st.markdown(f"💦 **Liquidité :** ${row['liquidity']:,}" if row['liquidity'] else "💦 Liquidité : N/A")
                st.markdown(f"🏷️ **FDV :** ${row['fdv']:,}" if row['fdv'] else "🏷️ FDV : N/A")
            with cols[4]:
                score = row["score"]
                color = "🟢" if score > 7 else "🟡" if score > 4 else "🔴"
                st.markdown(f"⭐ **Score : {color} {score}/10**")

        st.markdown("---")  # ligne de séparation

    # --- Sélecteur pour analyse détaillée ---
    choix = st.selectbox("🔎 Choisir un coin pour voir l’analyse détaillée", tokens["symbol"])
    token = tokens[tokens["symbol"] == choix].iloc[0]

    details = analyze_token(token["id"])
    if details:
        st.markdown(f"""
        ## 📊 Analyse de **{token['symbol']}**
        - 💰 Prix actuel : **{details['price']} USD**
        - 📈 Volume 24h : **{details['volume_24h']}**
        - 💦 Liquidité : **{details['liquidity']}**
        - 🏷️ FDV : **{details['fdv']}**
        - ⭐ Score potentiel : **{token['score']}/10**
        """)

        if details["logo"]:
            st.image(details["logo"], width=100, caption=token["name"])
    else:
        st.warning("Impossible de récupérer l’analyse de ce token.")
