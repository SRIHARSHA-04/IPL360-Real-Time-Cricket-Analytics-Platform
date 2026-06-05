import pandas as pd

from sqlalchemy import text

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

    return pd.read_sql(
        query,
        engine
    )


def top_wicket_takers():

    query = """
    SELECT bowler,
           SUM(wicket) AS wickets
    FROM fact_deliveries
    GROUP BY bowler
    ORDER BY wickets DESC
    LIMIT 20
    """

    return pd.read_sql(
        query,
        engine
    )


def team_wins():

    query = """
    SELECT winner,
           COUNT(*) AS wins
    FROM dim_matches
    WHERE winner <> 'NaN'
    GROUP BY winner
    ORDER BY wins DESC
    """

    return pd.read_sql(
        query,
        engine
    )


def venue_analysis():

    query = text("""
    SELECT
        CASE
            WHEN venue ILIKE '%Wankhede%'
                THEN 'Wankhede Stadium'

            WHEN venue ILIKE '%Chidambaram%'
                THEN 'MA Chidambaram Stadium'

            WHEN venue ILIKE '%M Chinnaswamy%'
                THEN 'M Chinnaswamy Stadium'

            WHEN venue ILIKE '%Arun Jaitley%'
                THEN 'Arun Jaitley Stadium'

            WHEN venue ILIKE '%Narendra Modi%'
                THEN 'Narendra Modi Stadium'

            ELSE venue

        END AS venue,

        COUNT(*) AS matches

    FROM dim_matches

    GROUP BY 1

    ORDER BY matches DESC

    LIMIT 20
    """)

    with engine.connect() as conn:

        return pd.read_sql(
            query,
            conn
        )


def batting_average():

    query = """
    SELECT batter,

           SUM(batter_runs) AS runs,

           SUM(wicket) AS dismissals,

           ROUND(
               SUM(batter_runs)::numeric
               /
               NULLIF(
                   SUM(wicket),
                   0
               ),
               2
           ) AS average

    FROM fact_deliveries

    GROUP BY batter

    HAVING SUM(batter_runs) > 1000

    ORDER BY average DESC

    LIMIT 20
    """

    return pd.read_sql(
        query,
        engine
    )


def strike_rate():

    query = """
    SELECT batter,

           ROUND(
               SUM(batter_runs) * 100.0
               /
               COUNT(*),
               2
           ) AS strike_rate

    FROM fact_deliveries

    GROUP BY batter

    HAVING COUNT(*) > 500

    ORDER BY strike_rate DESC

    LIMIT 20
    """

    return pd.read_sql(
        query,
        engine
    )