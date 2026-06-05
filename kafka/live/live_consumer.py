import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "ipl_match_stream",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)

current_innings = None

score = 0
wickets = 0
legal_balls = 0

print("Live Consumer Started")

for message in consumer:

    data = message.value

    innings = int(data["innings"])

    if current_innings is None:
        current_innings = innings

    if innings != current_innings:

        current_innings = innings

        score = 0
        wickets = 0
        legal_balls = 0

    score += int(data["total_runs"])

    wickets += int(data["wicket"])

    legal_balls += 1

    completed_overs = legal_balls // 6
    balls_in_over = legal_balls % 6

    state = {
        "innings": innings,
        "score": score,
        "wickets": wickets,
        "legal_balls": legal_balls,
        "display_over": f"{completed_overs}.{balls_in_over}",
        "overs_float": round(legal_balls / 6, 2),
        "batter": data["batter"],
        "bowler": data["bowler"],
        "runs": data["total_runs"]
    }

    with open(
        "dashboard/live/live_match_state.json",
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )

    print(state)