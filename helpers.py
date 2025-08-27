import requests
import pandas as pd


# 🔍 Récupère les tokens "meme" trending (DexScreener)
def get_trending_tokens(limit=20):
    url = "https://api.dexscreener.com/latest/dex/tokens/trending"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erreur API DexScreener:", response.text)
        return pd.DataFrame()

    data = response.json().get("pairs", [])
    if not data:
        return pd.DataFrame()

    # transformer en DataFrame
    df = pd.DataFrame(data)

    # certaines colonnes peuvent ne pas exister → on sécurise
    df["symbol"] = df.get("baseToken", {}).apply(lambda x: x.get("symbol") if isinstance(x, dict) else None)
    df["address"] = df.get("baseToken", {}).apply(lambda x: x.get("address") if isinstance(x, dict) else None)
    df["liquidity"] = df["liquidity"].apply(lambda x: x.get("usd") if isinstance(x, dict) else None)
    df["v24hUSD"] = df["volume"].apply(lambda x: x.get("h24") if isinstance(x, dict) else None)

    # rajout logo si dispo
    if "info" in df.columns:
        df["logo"] = df["info"].apply(lambda x: x.get("imageUrl") if isinstance(x, dict) else None)
    else:
        df["logo"] = None

    # Score basique : volume + liquidité
    df["score"] = (
        (df["v24hUSD"].astype(float) / df["v24hUSD"].astype(float).max()) * 5
        + (df["liquidity"].astype(float) / df["liquidity"].astype(float).max()) * 5
    )
    df["score"] = df["score"].round(1).clip(0, 10)

    return df[["symbol", "address", "liquidity", "v24hUSD", "score", "logo"]].head(limit)


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

    d = data[0]  # première paire
    details = {
        "price": float(d["priceUsd"]) if d.get("priceUsd") else None,
        "volume_24h": float(d["volume"]["h24"]) if "volume" in d else None,
        "liquidity": float(d["liquidity"]["usd"]) if "liquidity" in d else None,
        "fdv": float(d["fdv"]) if d.get("fdv") else None,
        "holders": d["txns"]["h24"] if "txns" in d else None,  # approximation
        "score": None,
    }

    # historique fictif pour l’instant (DexScreener ne donne pas direct)
    history = pd.DataFrame([{"time": 0, "price": float(d["priceUsd"])}]) if d.get("priceUsd") else pd.DataFrame()
    details["history"] = history

    return details
