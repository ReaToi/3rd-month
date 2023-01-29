from pprint import pprint

from bs4 import BeautifulSoup
import requests


URL = 'https://enter.kg/videokarty_bishkek'


HEADERS = {
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/'
              'apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def get_html(url):
    req = requests.get(url)
    return req


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product vm-col vm-col-1')
    news = []
    for item in items:
        news.append({
            'photo': item.find('img'),
            'link': item.get('href'),
            'title': item.find('div', class_='rows').getText(),
            'price': item.find('td', width='260').getText(),
            'vendor_code': item.find('td', width='110').getText()
                    })
    return news


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        news = []
        html = get_html(f'{URL}')
        current_page = get_data(html.text)
        news.extend(current_page)
        # return news
        pprint(news)
    else:
        raise Exception('Error in parser')


parser()
