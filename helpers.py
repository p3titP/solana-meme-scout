import pandas as pd
import requests
import datetime

def get_trending_tokens(min_liquidity=500, min_volume=10000):
    url = "https://api.dexscreener.com/latest/dex/trending"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        tokens = []
        for t in data.get("pairs", []):
            if t.get("chainId") != "solana":  # garder uniquement Solana
                continue

            token = {
                "symbol": t.get("baseToken", {}).get("symbol", "N/A"),
                "address": t.get("baseToken", {}).get("address", ""),
                "liquidity": t.get("liquidity", {}).get("usd", 0),
                "volume_24h": t.get("volume", {}).get("h24", 0),
                "price": float(t.get("priceUsd", 0))
            }
            tokens.append(token)

        df = pd.DataFrame(tokens)
        df = df[(df["liquidity"] >= min_liquidity) & (df["volume_24h"] >= min_volume)]

        return df

    except Exception as e:
        print("Erreur Dexscreener:", e)
        return pd.DataFrame()

# 📈 Analyse d’un token (historique de prix depuis Dexscreener)
def analyze_token(address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        pairs = data.get("pairs", [])
        if not pairs:
            return None

        token = pairs[0]

        # Historique simplifié (Dexscreener ne donne pas les bougies → on simule à partir du prix actuel)
        price = float(token.get("priceUsd", 0))
        history = []
        now = datetime.datetime.now()

        for i in range(24):
            history.append({
                "time": now - datetime.timedelta(hours=i),
                "price": price * (1 + (0.02 * ((i % 5) - 2)))  # variations factices ±2%
            })

        df_history = pd.DataFrame(history).sort_values("time")

        return {
            "price": price,
            "volume_24h": token.get("volume", {}).get("h24", 0),
            "liquidity": token.get("liquidity", {}).get("usd", 0),
            "holders": token.get("txns", {}).get("h24", 0),  # approximation
            "history": df_history
        }

    except Exception as e:
        print("Erreur analyse token:", e)
        return None
