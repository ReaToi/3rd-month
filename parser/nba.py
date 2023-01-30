from pprint import pprint

from bs4 import BeautifulSoup
import requests


NBA = 'https://www.nba.com/games?date=2023-02-01'


HEADERS = {
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/'
              'apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def get_html(url):
    req = requests.get(url)
    return req



def get_nba(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='GameCard_gc__UCI46 GameCardsMapper_gamecard__pz1rg')
    games = []
    for item in items:
        games.append({
            'time_game': item.find('section', class_='GameCard_gcMain__q1lUW').getText()

        })
    # games.append('sf')
    pprint(games)


html = get_html(NBA)
get_nba(html.text)