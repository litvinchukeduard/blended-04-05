from db.store_in_db import Category, Book
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host='localhost', password='my-password', port='6379')
cache = RedisLRU(client)

@cache
def get_books_by_category(category_name: str):
    category = Category.objects(name=category_name).first()
    books = Book.objects(category=category).all()
    return [book.title for book in books]

@cache
def get_book_by_title(book_title: str):
    return Book.objects(title=book_title).first()

while True:
    print('Welcome to our bookstore')
    command, search = input('>>> ').strip().split() # category History | book Under the Tuscan Sun | exit
    if command == 'category':
        print()
        print(f'All books in category {search}:')
        print()
        for book in get_books_by_category(search):
            print(book)
    elif command == 'book':
        print(get_book_by_title(search))
    elif command == 'exit':
        print('Goodbye!')
        break
    else:
        print('Invalid command')
