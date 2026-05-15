import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    raise Exception("API_FOOTBALL_KEY saknas i .env")

url = "https://v3.football.api-sports.io/status"

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(
    url,
    headers=headers,
    timeout=20
)

print("Status code:", response.status_code)
print(response.text)