import requests
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import time

BASE_URL = "https://site.api.espn.com/apis/site/v2/sports"

LEAGUES = {
    "Premier League": "soccer/eng.1",
    "La Liga": "soccer/esp.1",
    "Bundesliga": "soccer/ger.1",
    "Serie A": "soccer/ita.1",
    "Ligue 1": "soccer/fra.1",
    "Championship": "soccer/eng.2",
    "Eredivisie": "soccer/ned.1",
    "Liga Portugal": "soccer/por.1",
    "Saudi Pro League": "soccer/ksa.1",
    "UEFA Champions League": "soccer/uefa.champions",
    "UEFA Europa League": "soccer/uefa.europa",

    "🌍 World Cup 2026": "soccer/fifa.world",

    "NBA": "basketball/nba",
    "NHL": "hockey/nhl"
}


def get_cached(url):

    try:

        url = f"{url}&_t={int(time.time())}"

        r = requests.get(

            url,

            headers={

                "Cache-Control": "no-cache",

                "Pragma": "no-cache",

                "Expires": "0"

            },

            timeout=15

        )

        return r.json()

    except:

        return None


def detect_sport(path):

    if "soccer" in path:
        return "soccer"

    if "basketball" in path:
        return "basketball"

    if "hockey" in path:
        return "hockey"

    return "other"


def period_name(sport):

    if sport == "soccer":
        return "тайм"

    if sport == "basketball":
        return "четверть"

    if sport == "hockey":
        return "период"

    return "период"


def load_events(league):

    path = LEAGUES.get(league)

    if not path:
        return [], None

    sport = detect_sport(path)

    now = datetime.utcnow()

    if league == "🌍 World Cup 2026":

        start = "20260601"
        end = "20260731"

    else:

        start = (now - timedelta(days=30)).strftime("%Y%m%d")
        end = (now + timedelta(days=30)).strftime("%Y%m%d")

    url = f"{BASE_URL}/{path}/scoreboard?dates={start}-{end}&limit=1000"

    data = get_cached(url)

    if not data:
        return [], sport

    return data.get("events", []), sport


def convert_time(date_string):

    dt = datetime.fromisoformat(
        date_string.replace("Z", "+00:00")
    )

    utc = dt.strftime("%H:%M")

    msk = (dt + timedelta(hours=3)).strftime("%H:%M")

    return dt, utc, msk


def get_stadium(event):

    try:
        return event["competitions"][0]["venue"]["fullName"]

    except:
        return "Стадион неизвестен"


def add_match_link(event, text):

    try:

        links = event.get("links", [])

        if links:

            for link in links:

                href = link.get("href", "")

                if href.startswith("https://www.espn.com"):

                    text += f"📺 {href}\n"

                    return text

    except:

        pass

    return text


def group_matches(matches):

    grouped = defaultdict(list)

    for m in matches:

        grouped[m["date"]].append(m["text"])

    result = ""

    for date in sorted(grouped.keys()):

        result += f"📅 {date}\n\n"

        for match in grouped[date]:

            result += match

        result += "\n"

    return result


def parse_recent(events):

    matches = []

    for e in events:

        state = e["status"]["type"]["state"]

        if state not in ["post", "pre"]:
            continue

        dt, utc, msk = convert_time(e["date"])

        comp = e["competitions"][0]

        teams = comp["competitors"]

        team1 = teams[0]["team"]["displayName"]
        team2 = teams[1]["team"]["displayName"]

        stadium = get_stadium(e)

        date_label = dt.strftime("%d.%m.%Y")

        if state == "post":

            score1 = teams[0]["score"]
            score2 = teams[1]["score"]

            text = (
                f"{team1} {score1}:{score2} {team2}\n"
                f"🏟 {stadium}\n"
                f"{utc} UTC | {msk} МСК\n"
            )

        else:

            text = (
                f"{team1} vs {team2}\n"
                f"🏟 {stadium}\n"
                f"{utc} UTC | {msk} МСК\n"
            )

        text = add_match_link(e, text)

        text += "\n"

        matches.append({
            "date": date_label,
            "text": text
        })

    if not matches:
        return "Матчи не найдены."

    return group_matches(matches)


def parse_live(events, sport):

    word = period_name(sport)

    text = "LIVE матчи\n\n"

    found = False

    for e in events:

        state = e["status"]["type"]["state"]

        if state not in ["in", "live", "halftime"]:
            continue

        comp = e["competitions"][0]

        teams = comp["competitors"]

        team1 = teams[0]["team"]["displayName"]
        team2 = teams[1]["team"]["displayName"]

        score1 = teams[0]["score"]
        score2 = teams[1]["score"]

        clock = e["status"].get("displayClock", "")
        period = e["status"].get("period", "")

        stadium = get_stadium(e)

        text += (
            f"{team1} {score1}:{score2} {team2}\n"
            f"🏟 {stadium}\n"
            f"{clock} | {period} {word}\n"
        )

        text = add_match_link(e, text)

        text += "\n"

        found = True

    if not found:

        text += "LIVE матчей сейчас нет."

    return text


def get_tour_matches(league, tour):

    events, sport = load_events(league)

    matches = []

    for e in events:

        week = (
            e.get("week", {})
            .get("number", 0)
        )

        if week != tour:
            continue

        comp = e["competitions"][0]

        teams = comp["competitors"]

        team1 = teams[0]["team"]["displayName"]
        team2 = teams[1]["team"]["displayName"]

        dt, utc, msk = convert_time(e["date"])

        stadium = get_stadium(e)

        date_label = dt.strftime("%d.%m.%Y")

        text = (
            f"{team1} vs {team2}\n"
            f"🏟 {stadium}\n"
            f"{utc} UTC | {msk} МСК\n"
        )

        text = add_match_link(e, text)

        text += "\n"

        matches.append({
            "date": date_label,
            "text": text
        })

    if not matches:
        return "Матчи тура не найдены."

    return group_matches(matches)


def search_team(team_name):

    team_name = team_name.lower()

    all_matches = []

    for league in LEAGUES:

        events, sport = load_events(league)

        for e in events:

            comp = e["competitions"][0]

            teams = comp["competitors"]

            team1 = teams[0]["team"]["displayName"]
            team2 = teams[1]["team"]["displayName"]

            if (
                team_name not in team1.lower()
                and team_name not in team2.lower()
            ):
                continue

            dt, utc, msk = convert_time(e["date"])

            stadium = get_stadium(e)

            status = e["status"]["type"]["state"]

            date_label = dt.strftime("%d.%m.%Y")

            if status == "post":

                score = f"{teams[0]['score']}:{teams[1]['score']}"

            elif status in ["in", "live"]:

                score = (
                    f"LIVE "
                    f"{teams[0]['score']}:{teams[1]['score']}"
                )

            else:

                score = "vs"

            text = (
                f"{team1} {score} {team2}\n"
                f"🏟 {stadium}\n"
                f"{utc} UTC | {msk} МСК\n"
            )

            text = add_match_link(e, text)

            text += "\n"

            all_matches.append({
                "date": date_label,
                "text": text
            })

    if not all_matches:

        return "Команда не найдена или матчей нет."

    return group_matches(all_matches)


def get_matches(league, mode):

    events, sport = load_events(league)

    if not events:
        return "Матчи не найдены."

    if mode == "recent":
        return parse_recent(events)

    if mode == "live":
        return parse_live(events, sport)

    return "Ошибка"
def get_tour_matches(league, tour_number):

    events, sport = load_events(league)

    if not events:
        return "Матчи не найдены"

    matches = []

    for e in events:

        try:

            season_type = (
                e["season"]["type"]
            )

            if season_type != tour_number:
                continue

        except:
            continue

        comp = e["competitions"][0]

        teams = comp["competitors"]

        team1 = teams[0]["team"]["displayName"]
        team2 = teams[1]["team"]["displayName"]

        status = e["status"]["type"]["state"]

        dt, utc, msk = convert_time(e["date"])

        date_label = dt.strftime("%d.%m.%Y")

        stadium = get_stadium(e)

        if status == "post":

            score = (
                f"{teams[0]['score']}:{teams[1]['score']}"
            )

        elif status in ["in", "live"]:

            score = (
                f"LIVE "
                f"{teams[0]['score']}:{teams[1]['score']}"
            )

        else:

            score = "vs"

        text = (
            f"{team1} {score} {team2}\n"
            f"🏟 {stadium}\n"
            f"{utc} UTC | {msk} МСК\n"
        )

        text = add_match_link(e, text)

        text += "\n"

        matches.append({
            "date": date_label,
            "text": text
        })

    if not matches:
        return "Матчи тура не найдены."

    return group_matches(matches)