import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}


def search_team(team_name):
    url = f"{BASE_URL}/teams"

    params = {
        "search": team_name
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=20
    )

    data = response.json()
    teams = data.get("response", [])

    if not teams:
        return None

    return teams[0]["team"]["id"]


def get_last_10_form(team_id, league_id, season):
    url = f"{BASE_URL}/fixtures"

    params = {
        "team": team_id,
        "league": league_id,
        "season": season,
        "last": 10
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=20
    )

    data = response.json()

    print("API status:", response.status_code)
    print("API errors:", data.get("errors"))
    print("API results:", data.get("results"))

    fixtures = data.get("response", [])

    wins = 0
    draws = 0
    losses = 0

    print(f"Antal matcher hittade: {len(fixtures)}")

    for match in fixtures:
        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        home_name = match["teams"]["home"]["name"]
        away_name = match["teams"]["away"]["name"]

        home_goals = match["goals"]["home"]
        away_goals = match["goals"]["away"]

        print(f"{home_name} {home_goals}-{away_goals} {away_name}")

        if home_goals is None or away_goals is None:
            continue

        if home_goals == away_goals:
            draws += 1

        elif team_id == home_id:
            if home_goals > away_goals:
                wins += 1
            else:
                losses += 1

        elif team_id == away_id:
            if away_goals > home_goals:
                wins += 1
            else:
                losses += 1

    return f"{wins}-{draws}-{losses}"


if __name__ == "__main__":
    team_name = "Stevenage"

    team_id = search_team(team_name)

    print("Team ID:", team_id)

    form = get_last_10_form(
        team_id=team_id,
        league_id=41,
        season=2025
    )

    print(f"{team_name} senaste 10:")
    print(form)