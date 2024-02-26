import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


url = 'https://sputnik.by/'
html = get_html(url)
soup = parse_html(html)
print(soup.prettify()[:500])
