import pandas as pd
import requests
import datetime
import random

BIRDEYE_URL = "https://public-api.birdeye.so/public/market/trending"
HEADERS = {"x-chain": "solana"}

def get_trending_tokens(min_liquidity=50, min_volume=1000):
    try:
        res = requests.get(BIRDEYE_URL, headers=HEADERS, timeout=10)
        data = res.json()

        tokens = []
        for t in data.get("data", []):
            tokens.append({
                "symbol": t.get("symbol", "N/A"),
                "address": t.get("address", ""),
                "liquidity": t.get("liquidity", 0),
                "volume_24h": t.get("v24hUSD", 0),
                "price": t.get("price", 0),
            })

        df = pd.DataFrame(tokens)

        # Filtrer selon les critères
        df = df[(df["liquidity"] >= min_liquidity) & (df["volume_24h"] >= min_volume)]

        return df

    except Exception as e:
        print("Erreur Birdeye:", e)
        return pd.DataFrame()


def analyze_token(address):
    """Fake historique (Birdeye n’a pas d’historique gratuit)"""
    history = []
    now = datetime.datetime.now()
    base_price = random.uniform(0.0001, 1.0)

    for i in range(24):
        history.append({
            "time": now - datetime.timedelta(hours=i),
            "price": base_price * (1 + random.uniform(-0.05, 0.05))
        })

    df_history = pd.DataFrame(history).sort_values("time")

    return {
        "price": base_price,
        "volume_24h": random.randint(1000, 50000),
        "liquidity": random.randint(500, 5000),
        "holders": random.randint(100, 5000),
        "history": df_history
    }
