import requests
import pandas as pd
from pathlib import Path
from time import sleep

BASE_URL = "https://api.spela.svenskaspel.se/draw/1/stryktipset/draws"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

OUTPUT_FILE = "historical_data.csv"

START_DRAW = 4000
END_DRAW = 4299


def fetch_draw(draw_number):
    url = f"{BASE_URL}/{draw_number}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code != 200:
            return None

        data = response.json()
        return data.get("draw")

    except Exception as error:
        print(f"Fel vid hämtning av {draw_number}: {error}")
        return None


def get_outcome(home_goals, away_goals):
    if home_goals in ["", None] or away_goals in ["", None]:
        return ""

    try:
        home_goals = int(home_goals)
        away_goals = int(away_goals)
    except ValueError:
        return ""

    if home_goals > away_goals:
        return "1"

    if home_goals == away_goals:
        return "X"

    return "2"


def parse_draw(draw):
    rows = []

    draw_number = draw.get("drawNumber", "")
    draw_state = draw.get("drawState", "")
    reg_close_time = draw.get("regCloseTime", "")
    draw_comment = draw.get("drawComment", "")

    events = draw.get("drawEvents", [])

    for event in events:
        match = event.get("match", {})
        participants = match.get("participants", [])

        home = next(
            (p for p in participants if p.get("type") == "home"),
            {}
        )

        away = next(
            (p for p in participants if p.get("type") == "away"),
            {}
        )

        home_goals = home.get("result", "")
        away_goals = away.get("result", "")

        league = match.get("league", {}).get("name", "")
        country = match.get("league", {}).get("country", {}).get("name", "")

        start_odds = event.get("startOdds") or {}
        folk = event.get("svenskaFolket") or {}

        rows.append({
            "DrawNumber": draw_number,
            "DrawState": draw_state,
            "DrawComment": draw_comment,
            "RegCloseTime": reg_close_time,
            "Match": event.get("eventNumber", ""),
            "Home": home.get("name", ""),
            "Away": away.get("name", ""),
            "HomeGoals": home_goals,
            "AwayGoals": away_goals,
            "Outcome": get_outcome(home_goals, away_goals),
            "Odds1": start_odds.get("one", ""),
            "OddsX": start_odds.get("x", ""),
            "Odds2": start_odds.get("two", ""),
            "Folk1": folk.get("one", ""),
            "FolkX": folk.get("x", ""),
            "Folk2": folk.get("two", ""),
            "League": league,
            "Country": country,
            "MatchDate": match.get("matchStart", ""),
            "Status": match.get("status", "")
        })

    return rows


def load_existing_data():
    if not Path(OUTPUT_FILE).exists():
        return pd.DataFrame()

    return pd.read_csv(OUTPUT_FILE)


def build_historical_database():
    existing_df = load_existing_data()

    new_rows = []

    if not existing_df.empty:
        existing_keys = set(
            zip(
                existing_df["DrawNumber"].astype(str),
                existing_df["Match"].astype(str)
            )
        )
    else:
        existing_keys = set()

    for draw_number in range(START_DRAW, END_DRAW + 1):
        print(f"Hämtar omgång {draw_number}...")

        draw = fetch_draw(draw_number)

        if not draw:
            print(f"Hoppar över {draw_number}: ingen data")
            continue

        rows = parse_draw(draw)

        if not rows:
            print(f"Hoppar över {draw_number}: inga matcher")
            continue

        added_count = 0

        for row in rows:
            key = (
                str(row["DrawNumber"]),
                str(row["Match"])
            )

            if key in existing_keys:
                continue

            new_rows.append(row)
            existing_keys.add(key)
            added_count += 1

        print(f"Lade till {added_count} nya matcher från omgång {draw_number}")

        sleep(0.2)

    new_df = pd.DataFrame(new_rows)

    if existing_df.empty:
        final_df = new_df
    elif new_df.empty:
        final_df = existing_df
    else:
        final_df = pd.concat(
            [existing_df, new_df],
            ignore_index=True
        )

    if not final_df.empty:
        final_df = final_df.drop_duplicates(
            subset=["DrawNumber", "Match"],
            keep="last"
        )

        final_df = final_df.sort_values(
            by=["DrawNumber", "Match"]
        )

    final_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("Klar.")
    print(f"Nya rader: {len(new_df)}")
    print(f"Totalt antal rader: {len(final_df)}")
    print(f"Sparad till: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_historical_database()