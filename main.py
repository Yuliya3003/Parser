from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import csv
import re


def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        title = bsObj.body.i.text
    except AttributeError as e:
        return None
    return title


def getAuthor(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
    except AttributeError as e:
        return None

    full_html = str(bsObj)
    # Регулярное выражение для поиска имени автора
    pattern = r'"name":"([^"]+)"'

    # Ищем совпадения в HTML-коде
    matches = re.search(pattern, full_html)

    if matches:
        author_name = matches.group(1)
        return author_name
    else:
        return None


def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


urls = ["https://cyberleninka.ru/article/n/mikroservisnaya-arhitektura",
        "https://cyberleninka.ru/article/n/mikroservisnaya-arhitektura-na-frontend",
        "https://cyberleninka.ru/article/n/problema-tselostnosti-dannyh-v-mikroservisnoy-arhitekture",
        "https://cyberleninka.ru/article/n/vygody-perehoda-ot-monolitnoy-k-mikroservisnoy-arhitekture-prilozheniya",
        "https://cyberleninka.ru/article/n/mikroservisnaya-arhitektura-pri-razrabotke-frontend-prilozheniy",
        "https://cyberleninka.ru/article/n/analiz-arhitektur-informatsionnyh-sistem-monolitnaya-i-mikroservisnaya",
        "https://cyberleninka.ru/article/n/issledovanie-mikroservisnoy-arhitektury-dlya-veb-prilozheniya"]

titles = []
authors = []

for url in urls:

    title = getTitle(url)
    if title == None:
        print(f"for url '{url}' title could not be found")
    else:
        titles.append(title)

    author = getAuthor(url)
    if author == None:
        print(f"for url '{url}' author could not be found")
    else:
        authors.append(author)

data = ["url,author,article_title".split(",")]
for index in range(len(urls)):
    data.append([urls[index], authors[index], titles[index]])

path = "output.csv"
csv_writer(data, path)
