import pandas as pd

squads = pd.read_csv(
    "ml/fantasy/current_squads.csv"
)

print(
    sorted(
        squads["team"].unique()
    )
)