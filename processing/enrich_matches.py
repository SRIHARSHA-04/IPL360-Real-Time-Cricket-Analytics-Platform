import json
import pandas as pd
from pathlib import Path

SOURCE_DIR = Path("data/source/ipl_json")
PROCESSED_DIR = Path("data/processed")

records = []

for file in SOURCE_DIR.glob("*.json"):

    try:

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        info = data["info"]

        toss = info.get("toss", {})

        player_of_match = None

        pom = info.get("player_of_match", [])

        if pom:
            player_of_match = pom[0]

        records.append({
            "match_id": file.stem,
            "season": info.get("season"),
            "city": info.get("city"),
            "match_type": info.get("match_type"),
            "toss_winner": toss.get("winner"),
            "toss_decision": toss.get("decision"),
            "player_of_match": player_of_match
        })

    except Exception as e:
        print(f"Error: {file.name} -> {e}")

enrichment_df = pd.DataFrame(records)

enrichment_df["season"] = (
    enrichment_df["season"]
    .astype(str)
)

enrichment_df["city"] = (
    enrichment_df["city"]
    .fillna("Unknown")
    .astype(str)
)

enrichment_df["match_type"] = (
    enrichment_df["match_type"]
    .fillna("Unknown")
    .astype(str)
)

enrichment_df["toss_winner"] = (
    enrichment_df["toss_winner"]
    .fillna("Unknown")
    .astype(str)
)

enrichment_df["toss_decision"] = (
    enrichment_df["toss_decision"]
    .fillna("Unknown")
    .astype(str)
)

enrichment_df["player_of_match"] = (
    enrichment_df["player_of_match"]
    .fillna("Unknown")
    .astype(str)
)

enrichment_df.to_parquet(
    PROCESSED_DIR / "match_enrichment.parquet",
    index=False
)

print(enrichment_df.head())
print()
print("Records:", len(enrichment_df))