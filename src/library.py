import os
import json

from book import Book

class Library:
    def __init__(self) -> None:
        self.books: list[Book] = []

    def add_book(self, book: Book) -> None:
        if self.book_by_isbn(book.isbn):
            print('Book already exists.')
        else:
            self.books.append(book)
            print('Book added successfully.')

    def remove_book(self, isbn: str) -> None:
        book = self.book_by_isbn(isbn)

        if book:
            self.books.remove(book)
            print('Book removed successfully.')
        else:
            print('Book not found.')

    def list_books(self) -> list[Book]:
        return self.books

    def book_by_isbn(self, isbn: str) -> Book | None:
        for book in self.books:
            if book.isbn == isbn:
                return book

        return None

    def books_by_author(self, author):
        return [book for book in self.books if book.author == author]

    def update_file(self, file_path: str):
        existing_file = os.path.isfile(file_path)

        books_data = [vars(book) for book in self.books]

        existing_data = None

        if existing_file:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    existing_data = None

        if existing_data == books_data:
            if self.books:
                print(f'File {file_path} already up-to-date. No changes made.')
            else:
                os.remove(file_path)
                print(f'File {file_path} already up-to-date and will be removed due to empty list.')
        else:
            if self.books:
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(books_data, json_file, indent=4)

                if existing_file:
                    print(f'Updated file {file_path} successfully.')
                else:
                    print(f'Created file {file_path} successfully.')
            else:
                if existing_file:
                    os.remove(file_path)
                    print(f'Removed file {file_path} as the book list is empty.')
                else:
                    print('No books in list. File not created.')

    def load_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                books_data = json.load(json_file)

                # TODO: Suppress output from books being added via JSON read
                for book_data in books_data:
                    self.add_book(Book(**book_data))

            print(f'JSON data loaded from file {file_path}.')
        except FileNotFoundError as e:
            raise e
        except json.JSONDecodeError as e:
            raise e
