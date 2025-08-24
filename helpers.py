import pandas as pd
import random
import datetime

# Simule la récupération de tokens "meme" depuis Solana
def get_trending_tokens(min_liquidity=500, min_volume=10000):
    # ⚠️ Ici c’est du FAKE DATA pour la démo
    # Plus tard on pourra connecter à Dexscreener ou Jupiter API
    
    fake_data = []
    for i in range(10):
        fake_data.append({
            "symbol": f"MEME{i}",
            "liquidity": random.randint(100, 5000),
            "volume_24h": random.randint(1000, 50000),
            "price": round(random.uniform(0.0001, 1.0), 6)
        })

    df = pd.DataFrame(fake_data)

    # Filtrer selon les critères
    df = df[(df["liquidity"] >= min_liquidity) & (df["volume_24h"] >= min_volume)]
    return df

# Analyse détaillée d’un token
def analyze_token(symbol):
    try:
        # Fake historique pour la démo
        history = []
        now = datetime.datetime.now()
        price = round(random.uniform(0.0001, 1.0), 6)

        for i in range(24):
            history.append({
                "time": now - datetime.timedelta(hours=i),
                "price": price * (1 + random.uniform(-0.1, 0.1))
            })

        df_history = pd.DataFrame(history).sort_values("time")

        return {
            "price": price,
            "volume_24h": random.randint(1000, 50000),
            "liquidity": random.randint(500, 5000),
            "holders": random.randint(100, 5000),
            "history": df_history
        }
    except Exception:
        return None
