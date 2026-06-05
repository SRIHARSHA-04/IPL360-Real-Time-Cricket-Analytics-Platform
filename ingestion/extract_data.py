import json
import pandas as pd
from pathlib import Path

SOURCE_DIR = Path("data/source/ipl_json")
RAW_DIR = Path("data/raw")

RAW_DIR.mkdir(parents=True, exist_ok=True)

matches = []
deliveries = []
players = set()

json_files = list(SOURCE_DIR.glob("*.json"))

print(f"Found {len(json_files)} match files")

for file in json_files:

    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        info = data["info"]

        match_id = file.stem

        teams = info.get("teams", [])

        winner = None
        outcome = info.get("outcome", {})

        if "winner" in outcome:
            winner = outcome["winner"]

        matches.append(
            {
                "match_id": match_id,
                "date": str(info.get("dates", [""])[0]),
                "venue": info.get("venue"),
                "team1": teams[0] if len(teams) > 0 else None,
                "team2": teams[1] if len(teams) > 1 else None,
                "winner": winner,
            }
        )

        innings_data = data.get("innings", [])

        for innings_no, innings in enumerate(innings_data, start=1):

            team_name = innings.get("team")
            overs = innings.get("overs", [])

            for over in overs:

                over_no = over.get("over")

                for ball_no, delivery in enumerate(
                    over.get("deliveries", []),
                    start=1
                ):

                    batter = delivery.get("batter")
                    bowler = delivery.get("bowler")

                    if batter:
                        players.add(batter)

                    if bowler:
                        players.add(bowler)

                    batter_runs = delivery.get("runs", {}).get(
                        "batter", 0
                    )

                    extras = delivery.get("runs", {}).get(
                        "extras", 0
                    )

                    total_runs = delivery.get("runs", {}).get(
                        "total", 0
                    )

                    wicket = 0

                    if "wickets" in delivery:
                        wicket = 1

                    deliveries.append(
                        {
                            "match_id": match_id,
                            "innings": innings_no,
                            "batting_team": team_name,
                            "over": over_no,
                            "ball": ball_no,
                            "batter": batter,
                            "bowler": bowler,
                            "batter_runs": batter_runs,
                            "extras": extras,
                            "total_runs": total_runs,
                            "wicket": wicket,
                        }
                    )

    except Exception as e:
        print(f"Error processing {file.name}: {e}")

matches_df = pd.DataFrame(matches)

deliveries_df = pd.DataFrame(deliveries)

players_df = pd.DataFrame(
    sorted(players),
    columns=["player_name"]
)

matches_df.to_csv(
    RAW_DIR / "matches.csv",
    index=False
)

deliveries_df.to_csv(
    RAW_DIR / "deliveries.csv",
    index=False
)

players_df.to_csv(
    RAW_DIR / "players.csv",
    index=False
)

print("Files created successfully")
print(f"Matches: {len(matches_df)}")
print(f"Deliveries: {len(deliveries_df)}")
print(f"Players: {len(players_df)}")