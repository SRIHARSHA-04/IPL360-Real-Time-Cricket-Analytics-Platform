import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
CURATED_DIR = Path("data/curated")

CURATED_DIR.mkdir(parents=True, exist_ok=True)

matches = pd.read_parquet(
    PROCESSED_DIR / "processed_matches.parquet"
)

enrichment = pd.read_parquet(
    PROCESSED_DIR / "match_enrichment.parquet"
)
matches["match_id"] = matches["match_id"].astype(str)

enrichment["match_id"] = enrichment["match_id"].astype(str)

curated_matches = matches.merge(
    enrichment,
    on="match_id",
    how="left"
)

curated_matches.to_parquet(
    CURATED_DIR / "curated_matches.parquet",
    index=False
)

deliveries = pd.read_parquet(
    PROCESSED_DIR / "processed_deliveries.parquet"
)

deliveries.to_parquet(
    CURATED_DIR / "curated_deliveries.parquet",
    index=False
)

print("\n===== CURATED LAYER CREATED =====\n")

print("Matches:", len(curated_matches))
print("Deliveries:", len(deliveries))

print("\nColumns:")

print(curated_matches.columns.tolist())
