import requests
import json

url = "https://api.sofascore.com/api/v1/search/all"

params = {
    "q": "Stevenage"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, params=params)

print("Status:", response.status_code)

try:
    data = response.json()
    print(json.dumps(data, indent=2)[:4000])

except Exception:
    print(response.text[:4000])