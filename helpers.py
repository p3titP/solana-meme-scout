import requests
import pandas as pd

BASE_URL = "https://api.coingecko.com/api/v3"

# 🔍 Récupère les tokens trending en direct (CoinGecko)
def get_trending_tokens(limit=20):
    url = f"{BASE_URL}/search/trending"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erreur API CoinGecko:", response.text)
        return pd.DataFrame()

    data = response.json().get("coins", [])[:limit]

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame([{
        "symbol": c["item"]["symbol"],
        "address": c["item"]["id"],   # CoinGecko ID
        "score": c["item"]["score"],  # score natif
        "market_cap_rank": c["item"].get("market_cap_rank"),
        "name": c["item"]["name"]
    } for c in data])

    return df


# 📊 Analyse d’un token (via CoinGecko)
def analyze_token(token_id):
    url = f"{BASE_URL}/coins/{token_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erreur API CoinGecko:", response.text)
        return None

    data = response.json()
    market_data = data.get("market_data", {})

    # Exemple d’analyse simplifiée
    return {
        "price": market_data.get("current_price", {}).get("usd"),
        "volume_24h": market_data.get("total_volume", {}).get("usd"),
        "liquidity": market_data.get("market_cap"),  # proxy car CoinGecko ne donne pas "liquidity"
        "holders": data.get("community_data", {}).get("twitter_followers"),  # proxy aussi
        "score": data.get("coingecko_score"),
        "history": pd.DataFrame([{
            "time": h[0],
            "price": h[1]
        } for h in market_data.get("sparkline_7d", {}).get("price", []) for h in []])  # placeholder
    }
