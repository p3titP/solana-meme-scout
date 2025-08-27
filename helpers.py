import requests
import pandas as pd

DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens"

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
        token_info = {
            "symbol": d["baseToken"]["symbol"],
            "name": d["baseToken"]["name"],
            "address": d["baseToken"]["address"],
            "price": float(d["priceUsd"]) if d.get("priceUsd") else None,
            "volume_24h": float(d["volume"]["h24"]) if d.get("volume") else None,
            "liquidity": float(d["liquidity"]["usd"]) if d.get("liquidity") else None,
            "fdv": float(d["fdv"]) if d.get("fdv") else None,
            "logo": d["info"].get("imageUrl") if "info" in d else None,  # 👈 Logo ajouté
        }
        tokens.append(token_info)

    df = pd.DataFrame(tokens)

    # Score sur 10
    df["score"] = (
        (df["volume_24h"].fillna(0) / df["volume_24h"].max()) * 4
        + (df["liquidity"].fillna(0) / df["liquidity"].max()) * 3
        + (df["fdv"].fillna(0) / df["fdv"].max()) * 3
    ).round(1).clip(0, 10)

    return df
