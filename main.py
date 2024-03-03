import requests
from bs4 import BeautifulSoup
import re


def get_html(url):
    response = requests.get(url)
    return response.text


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


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
soup = parse_html(html)
data = extract_data(soup)
print(data)
