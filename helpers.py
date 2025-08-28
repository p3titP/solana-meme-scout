import requests
import pandas as pd


# 🔍 Trending tokens sur Solana
def get_trending_tokens(limit=20):
    url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erreur API DexScreener:", response.text)
        return pd.DataFrame()

    data = response.json().get("pairs", [])
    if not data:
        return pd.DataFrame()

    tokens = []
    for d in data[:limit]:
        tokens.append({
            "symbol": d["baseToken"]["symbol"],
            "address": d["baseToken"]["address"],
            "price": float(d["priceUsd"]) if d.get("priceUsd") else None,
            "volume_24h": float(d["volume"]["h24"]) if "volume" in d else None,
            "liquidity": float(d["liquidity"]["usd"]) if "liquidity" in d else None,
            "fdv": float(d["fdv"]) if d.get("fdv") else None,
            "logo": d["info"].get("imageUrl") if "info" in d else None,
        })

    df = pd.DataFrame(tokens)

    # Score simple
    df["score"] = (
        (df["volume_24h"].fillna(0) / df["volume_24h"].max()) * 5 +
        (df["liquidity"].fillna(0) / df["liquidity"].max()) * 5
    ).round(1).clip(0, 10)

    return df


# 📊 Analyse détaillée d’un token
def analyze_token(address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erreur analyse token:", response.text)
        return None

    data = response.json().get("pairs", [])
    if not data:
        return None

    d = data[0]
    details = {
        "price": float(d["priceUsd"]) if d.get("priceUsd") else None,
        "volume_24h": float(d["volume"]["h24"]) if "volume" in d else None,
        "liquidity": float(d["liquidity"]["usd"]) if "liquidity" in d else None,
        "fdv": float(d["fdv"]) if d.get("fdv") else None,
        "holders": d["txns"]["h24"] if "txns" in d else None,
    }

    # petit historique factice (DexScreener ne donne pas directement)
    details["history"] = pd.DataFrame(
        [{"time": 0, "price": details["price"]}]
    ) if details["price"] else pd.DataFrame()

    return details

