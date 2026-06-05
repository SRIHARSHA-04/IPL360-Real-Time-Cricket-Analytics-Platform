import pandas as pd
from db import engine


def top_run_scorers():

    query = """
    SELECT batter,
           SUM(batter_runs) AS runs
    FROM fact_deliveries
    GROUP BY batter
    ORDER BY runs DESC
    LIMIT 20
    """

    return pd.read_sql(query, engine)


def top_wicket_takers():

    query = """
    SELECT bowler,
           SUM(wicket) AS wickets
    FROM fact_deliveries
    GROUP BY bowler
    ORDER BY wickets DESC
    LIMIT 20
    """

    return pd.read_sql(query, engine)


def team_wins():

    query = """
    SELECT winner,
           COUNT(*) AS wins
    FROM dim_matches
    WHERE winner <> 'NaN'
    GROUP BY winner
    ORDER BY wins DESC
    """

    return pd.read_sql(query, engine)


def venue_analysis():

    query = """
    SELECT venue,
           COUNT(*) AS matches
    FROM dim_matches
    GROUP BY venue
    ORDER BY matches DESC
    LIMIT 20
    """

    return pd.read_sql(query, engine)