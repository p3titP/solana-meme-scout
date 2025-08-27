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
                logo = row.get("logo", None)  # 🔑 évite KeyError
                if logo:
                    st.image(logo, width=40)
                else:
                    st.text("🚀")
            with cols[1]:
                st.markdown(f"**{row.get('symbol', '?')}**")
                st.caption(row.get("name", ""))
            with cols[2]:
                st.markdown(f"💰 **Prix :** ${row.get('price', 0):.6f}" if row.get("price") else "💰 Prix : N/A")
                st.markdown(f"📈 **Volume 24h :** ${row.get('volume_24h', 0):,}" if row.get("volume_24h") else "📈 Volume : N/A")
            with cols[3]:
                st.markdown(f"💦 **Liquidité :** ${row.get('liquidity', 0):,}" if row.get("liquidity") else "💦 Liquidité : N/A")
                st.markdown(f"🏷️ **FDV :** ${row.get('fdv', 0):,}" if row.get("fdv") else "🏷️ FDV : N/A")
            with cols[4]:
                score = row.get("score", 0)
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
        - 💰 Prix actuel : **{details.get('price', 'N/A')} USD**
        - 📈 Volume 24h : **{details.get('volume_24h', 'N/A')}**
        - 💦 Liquidité : **{details.get('liquidity', 'N/A')}**
        - 🏷️ FDV : **{details.get('fdv', 'N/A')}**
        - ⭐ Score potentiel : **{token.get('score', 'N/A')}/10**
        """)

        if details.get("logo"):
            st.image(details["logo"], width=100, caption=token["name"])
    else:
        st.warning("Impossible de récupérer l’analyse de ce token.")

