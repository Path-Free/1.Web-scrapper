import requests
from bs4 import BeautifulSoup
import json
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    # добавь больше User-Agent, если нужно
]


def get_html(url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Произошла ошибка при отправке запроса: {e}")
        return None
    else:
        return response.text


def parse_html(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        print(f"Произошла ошибка при анализе HTML: {e}")
        return None
    else:
        return soup


def save_data(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Произошла ошибка при сохранении данных: {e}")


def extract_data(soup):
    data = []
    sections = soup.find_all('div', {"class": "section"})
    for section in sections:
        floors = section.find_all('div', class_='floor')
        floors = [div for div in floors if 'm-size-free' not in div.get('class', [])]
        for floor in floors:
            cells = floor.find_all('div', {"class": "floor__cell"})
            for cell in cells:
                if cell.find('div', {"class": "m-cell-empty"}):
                    continue
                else:
                    if cell.find('a', class_="cell-supertag__link"):
                        title = cell.find('a', class_="cell-supertag__link").text
                    elif cell.find('span', class_="cell-main-photo__size"):
                        title = cell.find('span', class_="cell-main-photo__size").text
                    elif cell.find('span', class_="cell-video__title"):
                        title = cell.find('span', class_="cell-video__title").text
                    elif cell.find('span', class_="cell-media-cover__title"):
                        title = cell.find('span', class_="cell-media-cover__title").text
                    elif cell.find('span', class_="cell-photo__title"):
                        title = cell.find('span', class_="cell-photo__title").text
                    elif cell.find('span', class_="cell-carousel__item-title"):
                        title = cell.find('span', class_="cell-carousel__item-title").text
                    else:
                        title = None
                    cover_image_link = cell.find('img')['src'] if cell.find('img') else None
                    if cell.find('span', class_="cell__controls-date").find('span'):
                        publication_date = cell.find('span', class_="cell__controls-date").find('span').text
                    else:
                        publication_date = None

                    # print(title)
                    # print(cover_image_link)
                    # print(publication_date)
                    # print()
                    # print(cell)

                    data.append({
                        'title': title,
                        'publication_date': publication_date,
                        'cover_image_link': cover_image_link
                    })
    return data


url = 'https://sputnik.by/'
html = get_html(url)
if html is not None:
    soup = parse_html(html)
    if soup is not None:
        data = extract_data(soup)
        if data is not None:
            save_data(data, 'data.json')
