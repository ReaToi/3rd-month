from pprint import pprint
from bs4 import BeautifulSoup
import requests


# URL = 'https://www.nba.com/'
URL = 'https://kaktus.media/?lable=8&date=2022-10-10&order=time'

HEADERS = {
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def get_html(url):
    req = requests.get(url)
    return req


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    # items = soup.find_all('div', class_='ArticleItem--data ArticleItem--data--withImage')
    items = soup.find_all('div', class_="Tag--article")
    news =[]
    for item in items:
        news.append({
            'title': item.find_all('a'),

        })
    pprint(news)


html = get_html(URL)
get_data(html.text)

