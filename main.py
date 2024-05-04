import requests
from bs4 import BeautifulSoup
import pika
import json

url = 'https://books.toscrape.com/'

credentials = pika.PlainCredentials('guest', 'guest')

connection= pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials= credentials))

channel= connection.channel()
channel.queue_declare(queue= 'category_books_queue')


def get_book_categories():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # {'History': 'https://books.toscrape.com/catalogue/category/books/history_32/index.html'}
    category_link_dict = dict()

    for element in soup.select('.nav-list li ul li a'):
        category_name = element.text.strip()
        category_link = element['href']
        category_link_dict.update({category_name : category_link})
    return category_link_dict

# ('History', 'catalogue/category/books/history_32/index.html')
def get_books_by_category(category: tuple):
    category_url = f'{url}/{category[1]}'
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'lxml')

    books_list = []
    for element in soup.select('.product_pod h3 a'):
        # 'Travel': ['It's Only the Himalayas']
        books_list.append(element.text.strip())
    return (category[0], books_list)

# {'Travel': ['It's Only the Himalayas', 'Full Moon over Noahâs']}

category_book_dict = dict()
categories = get_book_categories()
for category in categories.items():
    result = get_books_by_category(category)
    category_book = json.dumps({result[0] : result[1]})
    print(f'Sending info for category {result[0]}')
    channel.basic_publish(exchange='', routing_key='category_books_queue', body=category_book)
    print(f'Info for category {result[0]} sent.')


print(category_book_dict)

channel.close()
