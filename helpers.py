import requests
import pandas as pd

DEX_URL = "https://api.dexscreener.com/latest/dex/search"

# 🔥 Récupère les tokens Solana en tendance
def get_trending_tokens(limit=20):
    url = f"{DEX_URL}?q=solana"
    r = requests.get(url)
    if r.status_code != 200:
        print("Erreur API Dexscreener:", r.text)
        return pd.DataFrame()

    pairs = r.json().get("pairs", [])[:limit]

    if not pairs:
        return pd.DataFrame()

    df = pd.DataFrame([{
        "symbol": p.get("baseToken", {}).get("symbol"),
        "id": p.get("baseToken", {}).get("address"),  # address du token
        "name": p.get("baseToken", {}).get("name"),
        "price": float(p.get("priceUsd")) if p.get("priceUsd") else None,
        "liquidity": p.get("liquidity", {}).get("usd"),
        "volume_24h": p.get("volume", {}).get("h24"),
        "fdv": p.get("fdv"),
        "score": round(
            (float(p.get("volume", {}).get("h24") or 0) / max(1, float(p.get("liquidity", {}).get("usd") or 1))) * 10,
            1
        )  # petit score maison : ratio volume/liquidité
    } for p in pairs])

    return df


# 📊 Analyse détaillée d’un token (via Dexscreener)
def analyze_token(token_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    r = requests.get(url)

    if r.status_code != 200:
        print("Erreur API Dexscreener (analyse):", r.text)
        return None

    pairs = r.json().get("pairs", [])
    if not pairs:
        return None

    p = pairs[0]  # on prend la première pool trouvée
    history = []  # Dexscreener n'a pas d'historique gratuit simple

    return {
        "price": float(p.get("priceUsd")) if p.get("priceUsd") else None,
        "volume_24h": p.get("volume", {}).get("h24"),
        "liquidity": p.get("liquidity", {}).get("usd"),
        "holders": None,  # pas dispo via Dexscreener
        "score": None,    # tu peux recalculer si tu veux
        "history": pd.DataFrame(history)  # vide pour l’instant
    }
