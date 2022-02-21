import requests
import re
import json5 as json


def get_wpa(date, home_team, dh, season):
    url = f"https://www.fangraphs.com/wins.aspx?date={date}&team={home_team}&dh={dh}&season={season}"
    resp = requests.get(url)
    if not resp.ok:
        print("Yikes!")
        return
    html = resp.text
    away_team = re.search("var awaytext.+>(.+)</style>", html).group(1)
    charts = get_charts(html)
    wpa_data = charts[0]
    output = {"date": date, "season": season, "dh": dh, "home": home_team, "away": away_team, "wpa": [
        {"text": d['name'], "value": d['y']} for d in wpa_data]}

    return output


def get_charts(html):
    charts_1_2 = re.search("(var chart.+)", html).group(1)
    charts = []
    for chart_data in charts_1_2.split("data: ")[1:]:
        data = re.search("(\[\{.+?\}\]),?", chart_data).group(1)
        js = json.loads(data)
        charts.append(js)
    return charts


if __name__ == "__main__":
    dt = "2021-10-03"
    team = "Astros"
    dh = 0
    season = 2021

    wpa = get_wpa(dt, team, dh, season)
    print(wpa)
