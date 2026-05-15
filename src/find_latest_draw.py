import requests

BASE_URL = "https://api.spela.svenskaspel.se/draw/1/stryktipset/draws"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

def check_draw(draw_number):
    url = f"{BASE_URL}/{draw_number}"
    response = requests.get(url, headers=headers, timeout=20)

    if response.status_code != 200:
        return None

    data = response.json()
    draw = data.get("draw")

    if not draw:
        return None

    return {
        "drawNumber": draw.get("drawNumber"),
        "drawState": draw.get("drawState"),
        "regCloseTime": draw.get("regCloseTime"),
        "comment": draw.get("drawComment"),
        "events": len(draw.get("drawEvents", []))
    }

def find_latest(start=4800, end=5600):
    latest = None

    for draw_number in range(start, end + 1):
        result = check_draw(draw_number)

        if result:
            latest = result
            print(result)

    return latest

if __name__ == "__main__":
    latest = find_latest()
    print()
    print("Senaste hittade omgång:")
    print(latest)