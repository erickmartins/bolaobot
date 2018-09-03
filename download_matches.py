def download_matches(date):
    from bs4 import BeautifulSoup

    import requests

    if date == "":
        return 0
    else:
        url = make_url(date)
        # print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup.prettify())
        matches = parse_soup(soup)

        return matches


def parse_soup(soup):
    import pandas as pd
    matchtext = soup.find_all("div", class_="match_line")
    team1 = []
    team2 = []
    league = []
    date = []
    time = []
    # print(matchtext)
    for match in matchtext:
        team2.append(match['data-away-team'])
        team1.append(match['data-home-team'])
        league.append(match['data-country-name'] +
                      " " + match['data-league-name'])
        time.append(match['data-ko'])
        date.append(match['data-matchday'])
    matches = pd.DataFrame(
        {'home': team1, 'away': team2, 'league': league, 'time:': time, 'date': date}
    )
    

    return matches


def detect_next_saturday(today):
    sat = ""
    sun = ""
    if today != "":
        from datetime import datetime, timedelta
        d = datetime.strptime(today, '%Y%m%d')
        t = timedelta((12 - d.weekday()) % 7)
        if (t.days == 0):
            t = timedelta(days=7)

        sat = (d + t).strftime("%Y%m%d")
        t2 = timedelta(days=1)
        sun = (d + t + t2).strftime("%Y%m%d")
    return sat, sun


def get_today():
    import datetime
    x = datetime.datetime.now()
    currdate = x.strftime("%Y%m%d")
    return currdate


def make_url(date):
    url = "https://www.xscores.com/soccer/livescores/"
    url = url + date[6:8] + "-" + date[4:6]
    return url


def test_empty_date():
    date = ""
    assert download_matches(date) == 0


def test_any_date():
    date = "20180902"
    assert download_matches(date).empty is False


def test_make_url():
    date = "20180905"
    assert make_url(date) == "https://www.xscores.com/soccer/livescores/05-09"


def test_monday():
    today = "20180903"
    assert detect_next_saturday(today) == ("20180908", "20180909")


def test_saturday():
    today = "20180908"
    assert detect_next_saturday(today) == ("20180915", "20180916")


def test_empty_date_day():
    today = ""
    assert detect_next_saturday(today) == ("", "")


if __name__ == "__main__":
    date = detect_next_saturday("20180908")
    print(date)
    download_matches(date)
    print(download_matches(date))
