import requests


async def get_world_cup_matches():

    url = (
        "https://site.api.espn.com/apis/site/v2/"
        "sports/soccer/fifa.world/scoreboard"
    )

    r = requests.get(url)

    data = r.json()

    matches = []

    for e in data.get("events", []):

        comp = e["competitions"][0]

        teams = comp["competitors"]

        home = teams[0]["team"]["displayName"]
        away = teams[1]["team"]["displayName"]

        home_score = teams[0]["score"]
        away_score = teams[1]["score"]

        venue = (
            comp.get("venue", {})
            .get("fullName", "Unknown stadium")
        )

        status = (
            e["status"]["type"]["description"]
        )

        time = e["status"].get(
            "displayClock",
            "Not started"
        )

        link = ""

        for l in e.get("links", []):

            if l.get("rel") == ["summary"]:

                link = l.get("href", "")

        matches.append({

            "home": home,
            "away": away,

            "home_score": home_score,
            "away_score": away_score,

            "venue": venue,
            "status": status,
            "time": time,

            "scorers": "⚽ Goal scorers unavailable",

            "link": link

        })

    return matches