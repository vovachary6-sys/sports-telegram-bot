from telegram import Update

from parsers.super_espn_parser import (
    load_events,
    convert_time,
    get_stadium,
    period_name
)

from collections import defaultdict


def group_matches_by_date(events, sport):

    grouped = defaultdict(list)

    for e in events:

        dt, utc, msk = convert_time(e["date"])
        date_label = dt.strftime("%d.%m.%Y")

        comp = e["competitions"][0]
        teams = comp["competitors"]

        team1 = teams[0]["team"]["displayName"]
        team2 = teams[1]["team"]["displayName"]

        stadium = get_stadium(e)

        state = e["status"]["type"]["state"]

        clock = e["status"].get("displayClock", "")
        period = e["status"].get("period", "")

        word = period_name(sport)

        if state == "pre":

            text = (
                f"{team1} vs {team2}\n"
                f"🏟 {stadium}\n"
                f"{utc} UTC | {msk} МСК\n"
            )

        elif state == "in":

            text = (
                f"{team1} {teams[0]['score']}:{teams[1]['score']} {team2}\n"
                f"🏟 {stadium}\n"
                f"{clock} | {period} {word}\n"
            )

        elif state == "post":

            text = (
                f"{team1} {teams[0]['score']}:{teams[1]['score']} {team2}\n"
                f"🏟 {stadium}\n"
                f"{utc} UTC | {msk} МСК\n"
            )

        grouped[date_label].append(text)

    return grouped


async def send_schedule(update: Update, league: str):

    events, sport = load_events(league)

    if not events:

        await update.message.reply_text("В ближайшие дни матчей нет.")
        return

    grouped = group_matches_by_date(events, sport)

    text = f"🏟 Расписание {league}:\n\n"

    for date in sorted(grouped.keys()):

        text += f"📅 {date}\n\n"

        for match in grouped[date]:

            text += match + "\n"

    await update.message.reply_text(text)