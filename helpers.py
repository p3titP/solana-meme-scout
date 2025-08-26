import requests
import pandas as pd

BASE_URL = "https://api.coingecko.com/api/v3"

# 🔍 Tokens tendances
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
        "id": c["item"]["id"],   # CoinGecko ID
        "name": c["item"]["name"],
        "score": c["item"]["score"],
        "market_cap_rank": c["item"].get("market_cap_rank")
    } for c in data])

    return df


# 📊 Analyse d’un token
def analyze_token(token_id):
    # Données principales
    url = f"{BASE_URL}/coins/{token_id}?localization=false&market_data=true&community_data=true&sparkline=false"
    r = requests.get(url)
    if r.status_code != 200:
        print("Erreur API CoinGecko:", r.text)
        return None

    data = r.json()
    market_data = data.get("market_data", {})

    # Historique (7 jours en USD)
    hist_url = f"{BASE_URL}/coins/{token_id}/market_chart?vs_currency=usd&days=7&interval=hourly"
    rh = requests.get(hist_url)
    history = []
    if rh.status_code == 200:
        for point in rh.json().get("prices", []):
            history.append({"time": pd.to_datetime(point[0], unit="ms"), "price": point[1]})

    return {
        "price": market_data.get("current_price", {}).get("usd"),
        "volume_24h": market_data.get("total_volume", {}).get("usd"),
        "liquidity": market_data.get("market_cap"),  # proxy
        "holders": data.get("community_data", {}).get("twitter_followers"),  # proxy
        "score": data.get("coingecko_score"),
        "history": pd.DataFrame(history)
    }
