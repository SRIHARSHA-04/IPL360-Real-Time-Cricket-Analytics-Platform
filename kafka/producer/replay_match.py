import json
import time
import pandas as pd

from kafka import KafkaProducer

MATCH_ID = "1426261"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

df = pd.read_parquet(
    "data/curated/curated_deliveries.parquet"
)

match_df = df[df["match_id"].astype(str) == MATCH_ID]

print(f"Streaming {len(match_df)} deliveries")

for _, row in match_df.iterrows():

    event = row.to_dict()

    producer.send(
        "ipl_match_stream",
        value=event
    )

    print(
        f"Over {row['over']} "
        f"Ball {row['ball']} "
        f"Runs {row['total_runs']}"
    )

    time.sleep(1)

producer.flush()

print("Streaming completed")