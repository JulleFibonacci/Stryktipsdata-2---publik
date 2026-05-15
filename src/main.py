from collect_stryktips import update_stryktips_csv
import requests
from datetime import datetime, timezone

BASE_URL = "https://api.spela.svenskaspel.se/draw/1/stryktipset/draws"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


def parse_swedish_datetime(value):
    if not value:
        return None

    return datetime.fromisoformat(value)


def fetch_draw(draw_number):
    url = f"{BASE_URL}/{draw_number}"
    response = requests.get(url, headers=HEADERS, timeout=20)

    if response.status_code != 200:
        return None

    data = response.json()
    return data.get("draw")


def find_next_open_draw(start=4800, end=5300):
    now = datetime.now(timezone.utc)

    for draw_number in range(start, end + 1):
        draw = fetch_draw(draw_number)

        if not draw:
            continue

        events = draw.get("drawEvents", [])
        close_time_raw = draw.get("regCloseTime")
        close_time = parse_swedish_datetime(close_time_raw)

        if not close_time:
            continue

        close_time_utc = close_time.astimezone(timezone.utc)

        print(
            f"Testar {draw_number}: "
            f"{draw.get('drawState')} | "
            f"{close_time_raw} | "
            f"{len(events)} matcher"
        )

        if len(events) == 13 and close_time_utc > now:
            return {
                "draw_number": draw_number,
                "close_time": close_time_utc,
                "state": draw.get("drawState"),
                "comment": draw.get("drawComment"),
            }

    return None


if __name__ == "__main__":
    next_draw = find_next_open_draw()

    if not next_draw:
        raise Exception("Kunde inte hitta någon kommande Stryktipsomgång.")

    print()
    print("Vald omgång:")
    print(next_draw)

    update_stryktips_csv(next_draw["draw_number"])