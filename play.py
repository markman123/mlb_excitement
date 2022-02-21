import pandas as pd
from helper import convert_name_mlb_to_fangraphs
from wpa import get_wpa
import statsapi
import logging

logger = logging.getLogger("statsapi")
logger.setLevel(logging.DEBUG)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)8s - %(name)s(%(thread)s) - %(message)s"
)
ch.setFormatter(formatter)
rootLogger.addHandler(ch)


def double_header_status(game, sched):
    games_by_team = [g for g in sched if g["home_name"] == game["home_name"]]
    if len(games_by_team) == 1:
        return 0

    for idx, g in enumerate(games_by_team):
        if g["game_id"] == game["game_id"]:
            return idx

    return


def get_wpa_for_day(date):
    output = []
    sched = statsapi.schedule(start_date=date, end_date=date)
    for game in sched:
        double_header_flag = double_header_status(game, sched)
        home_team = convert_name_mlb_to_fangraphs(game["home_name"])
        season = date.split("/")[-1]
        wpa = get_wpa(game["game_date"], home_team, double_header_flag, season)
        output.append({"mlb_game": game, "wpa": wpa})
    return output


def create_df(game_data):
    output = []
    for game in game_data:
        wpa = game["wpa"]
        match_name = (
            f"{game['mlb_game']['away_name']} @ {game['mlb_game']['home_name']}"
        )
        for log in wpa["wpa"]:
            output.append({**log, "match": match_name})
    return pd.DataFrame(output)


if __name__ == "__main__":
    data = get_wpa_for_day("10/03/2021")
    create_df(data).to_excel("wpa.xlsx")
