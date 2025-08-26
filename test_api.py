import os
from dotenv import load_dotenv

load_dotenv()

print("Clé BirdEye:", os.getenv("BIRDEYE_API_KEY"))
