import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

BIRDEYE_API = os.getenv("BIRDEYE_API_KEY")

def fetch_top_meme_coins(limit=10):
    url = f"https://public-api.birdeye.so/public/tokenlist?sort=volume&chain=solana&limit={limit}"
    headers = {"x-api-key": BIRDEYE_API}
    try:
        r = requests.get(url, headers=headers).json()
        data = r.get("data", [])
        df = pd.DataFrame(data)
        return df[["symbol", "address", "liquidity", "price", "volume24h"]]
    except Exception as e:
        print("Erreur fetch_top_meme_coins:", e)
        return pd.DataFrame()

def fetch_price_history(address):
    url = f"https://public-api.birdeye.so/public/ohlcv?address={address}&type=1h&chain=solana"
    headers = {"x-api-key": BIRDEYE_API}
    try:
        r = requests.get(url, headers=headers).json()
        candles = r.get("data", [])
        df = pd.DataFrame(candles)
        if not df.empty:
            df["time"] = pd.to_datetime(df["unixTime"], unit="s")
            df.rename(columns={"o": "open", "c": "price"}, inplace=True)
        return df
    except Exception as e:
        print("Erreur fetch_price_history:", e)
        return pd.DataFrame()
