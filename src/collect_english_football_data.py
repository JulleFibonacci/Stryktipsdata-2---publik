import pandas as pd
from pathlib import Path

OUTPUT_FILE = "english_football_data.csv"

SEASONS = [
    "1213",
    "1314",
    "1415",
    "1516",
    "1617",
    "1718",
    "1819",
    "1920",
    "2021",
    "2122",
    "2223",
    "2324",
    "2425",
    "2526",
]

DIVISIONS = {
    "E0": "Premier League",
    "E1": "Championship",
    "E2": "League One",
    "E3": "League Two",
}


def get_season_label(season_code):
    start_year = int("20" + season_code[:2])
    end_year = int("20" + season_code[2:])
    return f"{start_year}/{end_year}"


def get_outcome(result):
    if result == "H":
        return "1"

    if result == "D":
        return "X"

    if result == "A":
        return "2"

    return ""


def first_existing_column(row, columns):
    for column in columns:
        if column in row and pd.notna(row[column]):
            return row[column]

    return None


def collect_data():
    all_rows = []

    for season in SEASONS:
        for division_code, division_name in DIVISIONS.items():
            url = f"https://www.football-data.co.uk/mmz4281/{season}/{division_code}.csv"

            print(f"Hämtar {division_name} {get_season_label(season)}")

            try:
                df = pd.read_csv(url)
            except Exception as error:
                print(f"Hoppar över {url}: {error}")
                continue

            for _, row in df.iterrows():
                if pd.isna(row.get("HomeTeam")) or pd.isna(row.get("AwayTeam")):
                    continue

                full_time_result = row.get("FTR")

                odds_home = first_existing_column(
                    row,
                    ["AvgH", "B365H", "MaxH", "PSH", "WHH"]
                )

                odds_draw = first_existing_column(
                    row,
                    ["AvgD", "B365D", "MaxD", "PSD", "WHD"]
                )

                odds_away = first_existing_column(
                    row,
                    ["AvgA", "B365A", "MaxA", "PSA", "WHA"]
                )

                all_rows.append({
                    "Season": get_season_label(season),
                    "DivisionCode": division_code,
                    "Division": division_name,
                    "Date": row.get("Date", ""),
                    "Home": row.get("HomeTeam", ""),
                    "Away": row.get("AwayTeam", ""),
                    "HomeGoals": row.get("FTHG", ""),
                    "AwayGoals": row.get("FTAG", ""),
                    "ResultRaw": full_time_result,
                    "Outcome": get_outcome(full_time_result),
                    "Odds1": odds_home,
                    "OddsX": odds_draw,
                    "Odds2": odds_away,
                    "HomeShots": row.get("HS", ""),
                    "AwayShots": row.get("AS", ""),
                    "HomeShotsTarget": row.get("HST", ""),
                    "AwayShotsTarget": row.get("AST", ""),
                    "HomeCorners": row.get("HC", ""),
                    "AwayCorners": row.get("AC", ""),
                    "HomeFouls": row.get("HF", ""),
                    "AwayFouls": row.get("AF", ""),
                    "HomeYellowCards": row.get("HY", ""),
                    "AwayYellowCards": row.get("AY", ""),
                    "HomeRedCards": row.get("HR", ""),
                    "AwayRedCards": row.get("AR", ""),
                })

    result_df = pd.DataFrame(all_rows)

    result_df = result_df.drop_duplicates(
        subset=["Season", "DivisionCode", "Date", "Home", "Away"],
        keep="last"
    )

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("Klar.")
    print(f"Antal matcher: {len(result_df)}")
    print(f"Sparad till: {OUTPUT_FILE}")


if __name__ == "__main__":
    collect_data()