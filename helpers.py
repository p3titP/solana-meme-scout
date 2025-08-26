import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Charger .env
load_dotenv()

API_KEY = os.getenv("BIRDEYE_API_KEY")
BASE_URL = "https://public-api.birdeye.so"  # <-- on ne met pas /defi directement
HEADERS = {"X-API-KEY": API_KEY, "accept": "application/json"}

# 🔍 Récupère les tokens trending en direct
def get_trending_tokens(limit=20):
    url = f"{BASE_URL}/public/market/trending"
    params = {"sort_by": "volume24hUSD", "limit": limit}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print("Erreur API BirdEye:", response.status_code, response.text)
        return pd.DataFrame()

    raw = response.json()
    print("Réponse brute BirdEye:", raw)  # <-- DEBUG

    data = raw.get("data", {}).get("tokens") or raw.get("data", [])
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # 💡 Calculer un score potentiel
    df["score"] = (
        (df["v24hUSD"].astype(float) / df["v24hUSD"].astype(float).max()) * 4 +
        (df["liquidity"].astype(float) / df["liquidity"].astype(float).max()) * 3 +
        (df["holders"].astype(float) / df["holders"].astype(float).max()) * 3
    )

    df["score"] = df["score"].round(1).clip(0, 10)

    return df[["symbol", "address", "liquidity", "v24hUSD", "holders", "score"]]
