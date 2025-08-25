import pandas as pd
import requests
import datetime
import random

BIRDEYE_URL = "https://public-api.birdeye.so/public/market/trending"
HEADERS = {"x-chain": "solana"}

def get_trending_tokens():
    try:
        res = requests.get(BIRDEYE_URL, headers=HEADERS, timeout=10)
        data = res.json()

        tokens = []
        for t in data.get("data", []):
            volume = t.get("v24hUSD", t.get("v24h", 0)) or 0
            liquidity = t.get("liquidity", 0) or 0
            price = t.get("price", 0) or 0

            # 🎯 Calcul d’une note de potentiel
            score = 0
            # Volume = moteur principal
            if volume > 1_000_000:
                score += 4
            elif volume > 100_000:
                score += 3
            elif volume > 10_000:
                score += 2
            else:
                score += 1

            # Liquidité = sécurité minimale
            if 50_000 <= liquidity <= 500_000:
                score += 3
            elif 10_000 <= liquidity < 50_000:
                score += 2
            elif liquidity < 10_000:
                score += 1

            # Prix bas (plus spéculatif)
            if price < 0.01:
                score += 2
            elif price < 1:
                score += 1

            tokens.append({
                "symbol": t.get("symbol", "N/A"),
                "address": t.get("address", ""),
                "liquidity": liquidity,
                "volume_24h": volume,
                "price": price,
                "score": score,  # ✅ Note finale
            })

        df = pd.DataFrame(tokens)
        df = df.sort_values("score", ascending=False)  # classé par potentiel

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
