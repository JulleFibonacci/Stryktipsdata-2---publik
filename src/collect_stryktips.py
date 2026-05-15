import requests
import pandas as pd

BASE_URL = "https://api.spela.svenskaspel.se/draw/1/stryktipset/draws"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

COLUMNS = [
    "Match", "Home", "Away",
    "Odds1", "OddsX", "Odds2",
    "Folk1", "FolkX", "Folk2",
    "League", "Round",
    "AI_Sim1", "AI_SimX", "AI_Sim2",
    "xG_For", "xG_Against", "xG_Diff",
    "HomeForm", "AwayForm"
]


def fetch_draw(draw_number):
    url = f"{BASE_URL}/{draw_number}"
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.json()


def parse_draw(data):
    draw = data["draw"]
    events = draw["drawEvents"]

    rows = []

    for event in events:
        participants = event["match"]["participants"]

        home = next(p for p in participants if p["type"] == "home")
        away = next(p for p in participants if p["type"] == "away")

        league = event["match"]["league"]["name"]

        start_odds = event.get("startOdds") or {}
        folk = event.get("svenskaFolket") or {}

        rows.append({
            "Match": event.get("eventNumber"),
            "Home": home.get("name", ""),
            "Away": away.get("name", ""),
            "Odds1": start_odds.get("one", ""),
            "OddsX": start_odds.get("x", ""),
            "Odds2": start_odds.get("two", ""),
            "Folk1": folk.get("one", ""),
            "FolkX": folk.get("x", ""),
            "Folk2": folk.get("two", ""),
            "League": league,
            "Round": draw.get("drawNumber", ""),
            "AI_Sim1": "",
            "AI_SimX": "",
            "AI_Sim2": "",
            "xG_For": "",
            "xG_Against": "",
            "xG_Diff": "",
            "HomeForm": "",
            "AwayForm": ""
        })

    return pd.DataFrame(rows, columns=COLUMNS)


def update_stryktips_csv(draw_number):
    data = fetch_draw(draw_number)
    df = parse_draw(data)
    df.to_csv("stryktips.csv", index=False)
    print(f"CSV uppdaterad med omgång {draw_number}")