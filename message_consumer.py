import pika
import json
from db.store_in_db import create_book, create_category

credentials = pika.PlainCredentials('guest', 'guest')

connection= pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials= credentials))

channel= connection.channel()

def consume_books_for_category(ch, method, properties, body):
    category_book = json.loads(body)
    category_name = list(category_book.keys())[0]
    category = create_category(category_name)
    print(f'Recieved books for category {category_name}')
    for book in category_book.get(category_name):
        create_book(book, category)
        print(f'Saved {book} for category {category_name}')

channel.basic_consume(queue='category_books_queue', on_message_callback=consume_books_for_category, auto_ack=True)

print('Started listening to channel...')
channel.start_consuming()
