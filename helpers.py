import pandas as pd
import requests

def get_trending_tokens(min_liquidity=50, min_volume=1000):
    url = "https://api.dexscreener.com/latest/dex/trending"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        print("=== DEBUG: Keys renvoyées par API ===")
        print(data.keys())   # Voir si 'pairs' existe bien

        tokens = []
        for t in data.get("pairs", []):
            # Filtrer uniquement Solana
            if t.get("chainId") != "solana":
                continue

            tokens.append({
                "symbol": t.get("baseToken", {}).get("symbol", "N/A"),
                "address": t.get("baseToken", {}).get("address", ""),
                "liquidity": t.get("liquidity", {}).get("usd", 0),
                "volume_24h": t.get("volume", {}).get("h24", 0),
                "price": float(t.get("priceUsd", 0) or 0)
            })

        df = pd.DataFrame(tokens)
        print(f"=== DEBUG: {len(df)} tokens trouvés avant filtre ===")

        if df.empty:
            return pd.DataFrame()

        # Filtrage
        df = df[(df["liquidity"] >= min_liquidity) & (df["volume_24h"] >= min_volume)]

        print(f"=== DEBUG: {len(df)} tokens après filtre ===")
        return df

    except Exception as e:
        print("Erreur Dexscreener:", e)
        return pd.DataFrame()


def analyze_token(address):
    # Pour l’instant on garde comme avant
    return {"price": 0, "volume_24h": 0, "liquidity": 0, "holders": 0, "history": pd.DataFrame()}
