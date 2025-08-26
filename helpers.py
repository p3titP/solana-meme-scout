import requests
import pandas as pd
import random
import datetime

# --- Récupération brute des tokens depuis Dexscreener ---
def get_trending_tokens():
    try:
        url = "https://api.dexscreener.com/latest/dex/tokens/solana"
        response = requests.get(url)
        data = response.json()

        if "pairs" not in data:
            return pd.DataFrame()

        tokens = []
        for pair in data["pairs"][:20]:  # on prend juste les 20 premiers
            tokens.append({
                "symbol": pair.get("baseToken", {}).get("symbol", "N/A"),
                "address": pair.get("baseToken", {}).get("address", "N/A"),
                "liquidity": pair.get("liquidity", {}).get("usd", 0),
                "volume_24h": pair.get("volume", {}).get("h24", 0),
                "price": pair.get("priceUsd", 0),
                # Score aléatoire pour démo
                "score": random.randint(1, 10)
            })

        return pd.DataFrame(tokens)

    except Exception as e:
        print("Erreur API :", e)
        return pd.DataFrame()


# --- Analyse d’un token ---
def analyze_token(symbol):
    try:
        now = datetime.datetime.now()
        history = []
        price = round(random.uniform(0.0001, 1.0), 6)

        for i in range(24):
            history.append({
                "time": now - datetime.timedelta(hours=i),
                "price": price * (1 + random.uniform(-0.15, 0.15))
            })

        df_history = pd.DataFrame(history).sort_values("time")

        return {
            "price": price,
            "volume_24h": random.randint(1000, 50000),
            "liquidity": random.randint(500, 5000),
            "holders": random.randint(50, 5000),
            "score": random.randint(1, 10),
            "history": df_history
        }
    except:
        return None
