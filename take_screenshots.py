from playwright.sync_api import sync_playwright
import time

BASE_URL = "http://localhost:8501"

pages = [
    ("home", BASE_URL),
    ("player_analytics", BASE_URL + "/Player_Analytics"),
    ("team_analytics", BASE_URL + "/Team_Analytics"),
    ("venue_analytics", BASE_URL + "/Venue_Analytics"),
    ("fantasy_xi", BASE_URL + "/Fantasy_XI"),
    ("live_match_center", BASE_URL + "/Live_Match_Center"),
]

with sync_playwright() as p:

    browser = p.chromium.launch()

    page = browser.new_page(
        viewport={
            "width": 1600,
            "height": 900
        }
    )

    for name, url in pages:

        print(f"Capturing {name}")

        page.goto(url)

        page.wait_for_timeout(4000)

        page.screenshot(
            path=f"screenshots/{name}.png",
            full_page=True
        )

    browser.close()

print("\nDone")