import pandas as pd
import requests

def get_trending_tokens(min_liquidity=50, min_volume=1000):
    # Endpoint spécifique à Solana
    url = "https://api.dexscreener.com/latest/dex/pairs/solana"
    try:
        res = requests.get(url, timeout=10)
print("Status code:", res.status_code)
print("Texte brut:", res.text[:500])  # affiche les 500 premiers caractères

        tokens = []
        for t in data.get("pairs", []):
            tokens.append({
                "symbol": t.get("baseToken", {}).get("symbol", "N/A"),
                "address": t.get("baseToken", {}).get("address", ""),
                "liquidity": t.get("liquidity", {}).get("usd", 0),
                "volume_24h": t.get("volume", {}).get("h24", 0),
                "price": float(t.get("priceUsd", 0) or 0)
            })

        df = pd.DataFrame(tokens)

        if df.empty:
            print("⚠️ Aucun token récupéré depuis l’API.")
            return pd.DataFrame()

        # Filtrage
        df = df[(df["liquidity"] >= min_liquidity) & (df["volume_24h"] >= min_volume)]

        return df

    except Exception as e:
        print("Erreur Dexscreener:", e)
        return pd.DataFrame()


def analyze_token(address):
    # Historique fictif (à améliorer après)
    import datetime, random
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
