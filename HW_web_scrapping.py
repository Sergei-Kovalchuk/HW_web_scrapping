import requests
import bs4
from pprint import pprint
from requests_html import HTMLSession
import re

url = "https://habr.com/ru/all/"
# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
KEYWORDS = set(word.lower() for word in KEYWORDS)

session = HTMLSession()
try:
    response = session.get(url)
except requests.exceptions.RequestException as err:
    raise SystemExit('Что-то пошло не так!',err)


soup = bs4.BeautifulSoup(response.html.html, features = 'html.parser')
articles = soup.find_all('article')
for article in articles:
    hubs = article.find_all(attrs={"class":"tm-article-snippet__hubs-item-link"})
    hubs = set(hub.find('span').text.lower() for hub in hubs)
    if KEYWORDS & hubs:
        date = article.find(class_ = 'tm-article-snippet__datetime-published').find('time').text
        title = article.find(class_ = 'tm-article-snippet__title-link').find('span').text
        url_=re.search("[^\/]+\/\/[^\/]+", url).group()                                             # https://habr.com
        link = url_ + article.find(class_ = 'tm-article-snippet__title-link').attrs['href']
        print(f'{date}: {title}; {link}')
