from mongoengine import connect
from .models import Category, Book

mongo_connection = connect('books',
                            host="localhost",
                            username="root",
                            password="example")

def create_category(category_name: str):
    category = Category(name=category_name)
    category.save()
    return category

def create_book(book_title: str, category: Category):
    book = Book(title=book_title, category=category)
    book.save()
    return book
