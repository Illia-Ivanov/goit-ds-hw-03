import requests
from bs4 import BeautifulSoup
import json
import re
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://db_name:password_from_db@cluster_name.unao38c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)
db = client.book


# Збираю авторів та через цикл починаю парсити дані
def scrape_authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    authors = soup.find_all('small', class_='author')
    authors_data = []

    for auth in authors:
        author_name = auth.text
        relative_url = 'author/' + re.sub(r'-+', '-', author_name.replace(' ', '-').replace('.', '-')).replace('é', 'e')
        full_url = 'https://quotes.toscrape.com/' + relative_url
        author_data = scrape_authors_info(full_url)
        if author_data not in authors_data:
            authors_data.append(author_data)

    return authors_data


# Збираю внутрішню інформацію про авторів та віддаю словник у цикл який знаходиться у функції scrape_authors,а там він вже додає інформацію про автора у словник з усіма авторами
def scrape_authors_info(full_url):
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fullname = soup.find('h3', class_='author-title').text.strip()
    born_date = soup.find('span', class_='author-born-date').get_text(strip=True)
    born_location = soup.find('span', class_='author-born-location').get_text(strip=True)
    description = soup.find('div', class_='author-description').get_text(strip=True)

    author_data = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

    return author_data


# Роблю парсинг опису фраз,автору і тег до них
def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')

    quotes_data = []

    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]

        quotes_data.append({
            "quote": text,
            "author": author,
            "tags": tags
        })

    return quotes_data


url = 'https://quotes.toscrape.com/'

quotes = scrape_quotes(url)
authors_data = scrape_authors(url)

# Вище оброблюю результати та зберігаю усе це в json файл
with open('quotes.json', 'w', encoding='UTF-8') as quotes_file:
    json.dump(quotes, quotes_file, indent=4)

with open('authors.json', 'w', encoding='UTF-8') as authors_file:
    json.dump(authors_data, authors_file, indent=4)

with open('quotes.json', 'r', encoding='UTF-8') as quotes_file:
    quotes_data = json.load(quotes_file)
    result_quotes = db.quotes.insert_many(quotes_data)

with open('authors.json', 'r', encoding='UTF-8') as authors_file:
    authors_data = json.load(authors_file)
    result_authors = db.authors.insert_many(authors_data)

print("Дані було успішно записано у файли quotes.json та authors.json")
