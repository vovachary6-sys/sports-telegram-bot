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
    "NBA": "basketball/nba",
    "NHL": "hockey/nhl"
}

CACHE = {}
CACHE_LIFETIME = 60


def get_cached(url):

    now = time.time()

    if url in CACHE:

        data, timestamp = CACHE[url]

        if now - timestamp < CACHE_LIFETIME:
            return data

    try:

        r = requests.get(url, timeout=30)

        data = r.json()

        CACHE[url] = (data, now)

        return data

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

    if sport in ["basketball", "hockey"]:

        start = (now - timedelta(days=3)).strftime("%Y%m%d")
        end = (now + timedelta(days=3)).strftime("%Y%m%d")

    else:

        start = (now - timedelta(days=7)).strftime("%Y%m%d")
        end = (now + timedelta(days=7)).strftime("%Y%m%d")

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


def get_goal_scorers(event, league):

    text = ""

    try:

        event_id = event.get("id")

        if not event_id:
            return ""

        path = LEAGUES.get(league)

        if not path:
            return ""

        url = (
            f"{BASE_URL}/{path}/summary?event={event_id}"
        )

        data = get_cached(url)

        if not data:
            return ""

        scoring_plays = data.get("scoringPlays", [])

        goals = []

        for play in scoring_plays:

            text_play = play.get("text", "")

            if text_play:

                goals.append(f"⚽ {text_play}")

        if goals:

            text = "\n".join(goals) + "\n"

    except:

        pass

    return text


def add_match_link(event, text):

    try:

        links = event.get("links", [])

        if links:

            for link in links:

                href = link.get("href", "")

                if "espn.com" in href:

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


def parse_finished(events, league):

    now = datetime.now(timezone.utc)

    limit = now - timedelta(days=7)

    matches = []

    for e in events:

        if e["status"]["type"]["state"] != "post":
            continue

        dt, utc, msk = convert_time(e["date"])

        if dt < limit:
            continue

        comp = e["competitions"][0]

        teams = comp["competitors"]

        team1 = teams[0]["team"]["displayName"]
        team2 = teams[1]["team"]["displayName"]

        score1 = teams[0]["score"]
        score2 = teams[1]["score"]

        stadium = get_stadium(e)

        date_label = dt.strftime("%d.%m.%Y")

        text = (
            f"{team1} {score1}:{score2} {team2}\n"
            f"🏟 {stadium}\n"
            f"{utc} UTC | {msk} МСК\n"
        )

        text += get_goal_scorers(e, league)

        text = add_match_link(e, text)

        text += "\n"

        matches.append({
            "date": date_label,
            "text": text
        })

    if not matches:
        return "В ближайшие дни матчей нет"

    return group_matches(matches)


def parse_live(events, sport, league):

    word = period_name(sport)

    text = "LIVE матчи\n\n"

    found = False

    for e in events:

        state = e["status"]["type"]["state"]

        if state not in ["in", "live"]:
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

        text += get_goal_scorers(e, league)

        text = add_match_link(e, text)

        text += "\n"

        found = True

    if not found:

        text += "LIVE матчей сейчас нет."

    return text


def parse_upcoming(events):

    now = datetime.now(timezone.utc)

    limit = now + timedelta(days=7)

    matches = []

    for e in events:

        if e["status"]["type"]["state"] != "pre":
            continue

        dt, utc, msk = convert_time(e["date"])

        if dt > limit:
            continue

        comp = e["competitions"][0]

        teams = comp["competitors"]

        team1 = teams[0]["team"]["displayName"]
        team2 = teams[1]["team"]["displayName"]

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
        return "В ближайшие дни матчей нет"

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

            text += get_goal_scorers(e, league)

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
        return "В ближайшие дни матчей нет"

    if mode == "finished":
        return parse_finished(events, league)

    if mode == "live":
        return parse_live(events, sport, league)

    if mode == "upcoming":
        return parse_upcoming(events)

    return "Ошибка"