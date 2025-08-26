import os
import requests
import pandas as pd

API_KEY = os.getenv("BIRDEYE_API_KEY")
BASE_URL = "https://public-api.birdeye.so/defi"

HEADERS = {"X-API-KEY": API_KEY, "accept": "application/json"}


# 🔍 Récupère les tokens trending en direct
def get_trending_tokens(limit=20):
    url = f"{BASE_URL}/token_trending"
    params = {"sort_by": "volume24hUSD", "limit": limit}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print("Erreur API BirdEye:", response.text)
        return pd.DataFrame()

    data = response.json().get("data", {}).get("tokens", [])
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # 💡 Calculer un score potentiel sur 10
    df["score"] = (
        (df["v24hUSD"].astype(float) / df["v24hUSD"].astype(float).max()) * 4  # volume
        + (df["liquidity"].astype(float) / df["liquidity"].astype(float).max()) * 3  # liquidité
        + (df["holders"].astype(float) / df["holders"].astype(float).max()) * 3  # nombre de holders
    )

    df["score"] = df["score"].round(1).clip(0, 10)  # note finale sur 10

    return df[["symbol", "address", "liquidity", "v24hUSD", "holders", "score"]]


# 📈 Historique du prix pour un token
def get_price_history(address, interval="1h", limit=24):
    url = f"{BASE_URL}/price_history"
    params = {"address": address, "interval": interval, "limit": limit}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print("Erreur API BirdEye:", response.text)
        return pd.DataFrame()
