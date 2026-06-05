import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "ipl_match_stream",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)

print("Listening...\n")

for message in consumer:

    data = message.value

    print(
    f'Innings {data["innings"]} | '
    f'Over {data["over"]}.{data["ball"]} | '
    f'{data["batter"]} vs {data["bowler"]} | '
    f'Runs {data["total_runs"]}'
    )