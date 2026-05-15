import requests
import json

URL = "https://api.spela.svenskaspel.se/draw/1/stryktipset/draws/4800"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

response = requests.get(URL, headers=headers, timeout=20)

print("Status code:", response.status_code)
print("Content-Type:", response.headers.get("content-type"))
print()

try:
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False)[:8000])
except Exception:
    print(response.text[:8000])