# module library

import os
import re
import json
from re import Pattern
from collections import defaultdict

from book import Book

class Library:
    def __init__(self) -> None:
        self.books:             list[Book]                  = []
        self.index_from_title:  defaultdict[str, list[int]] = defaultdict(list)
        self.index_from_author: defaultdict[str, list[int]] = defaultdict(list)
        self.index_from_isbn:   dict[str, int]              = {}

    def add_book(self, book: Book, suppress_output: bool = False) -> None:
        if self.book_by_isbn(book.isbn):
            print(f'Title: {book.title}, ISBN: {book.isbn} already exists.')
        else:
            self.books.append(book)

            book_index: int = len(self.books) - 1

            self.index_from_title[book.title].append(book_index)
            self.index_from_author[book.author].append(book_index)
            self.index_from_isbn[book.isbn] = book_index

            if not suppress_output:
                print(f'Title: {book.title}, ISBN: {book.isbn} added successfully.')

    def remove_book(self, isbn: str) -> None:
        book: Book | None = self.book_by_isbn(isbn)

        if book:
            book_index: int = self.index_from_isbn[isbn]

            del self.books[book_index]

            self.index_from_title[book.title].remove(book_index)
            if not self.index_from_title[book.title]:
                del self.index_from_title[book.title]

            self.index_from_author[book.author].remove(book_index)
            if not self.index_from_author[book.author]:
                del self.index_from_author[book.author]

            del self.index_from_isbn[isbn]

            for title in self.index_from_title:
                self.index_from_title[title] = [i - 1 if i > book_index else i for i in
                                                self.index_from_title[title]]

            for author in self.index_from_author:
                self.index_from_author[author] = [i - 1 if i > book_index else i for i in
                                                  self.index_from_author[author]]

            for isbn_key, idx in self.index_from_isbn.items():
                if idx > book_index:
                    self.index_from_isbn[isbn_key] -= 1

            print(f'Title: {book.title}, ISBN: {isbn} removed successfully.')
        else:
            print(f'ISBN: {isbn} not found.')

    def books_by_title(self, title: str) -> list[Book]:
        return [self.books[i] for i in self.index_from_title[title]]

    def books_by_author(self, author: str) -> list[Book]:
        return [self.books[i] for i in self.index_from_author[author]]

    def book_by_isbn(self, isbn: str) -> Book | None:
        try:
            return self.books[self.index_from_isbn[isbn]]
        except KeyError:
            return None

    def search_list(self, query: str) -> list[Book]:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        results = []

        for book in self.books:
            if (pattern.search(book.title) or pattern.search(book.author)or
                pattern.search(book.isbn)):
                results.append(book)

        return results

    def search_dict(self, query: str) -> list[Book]:
        pattern:         Pattern[str] = re.compile(re.escape(query), re.IGNORECASE)
        matched_indices: set          = set()

        for title, indices in self.index_from_title.items():
            if pattern.search(title):
                matched_indices.update(indices)

        for author, indices in self.index_from_author.items():
            if pattern.search(author):
                matched_indices.update(indices)

        for isbn, index in self.index_from_isbn.items():
            if pattern.search(isbn):
                matched_indices.add(index)

        return [self.books[i] for i in matched_indices]

    def update_file(self, file_path: str) -> None:
        existing_file: bool = os.path.isfile(file_path)

        books_data: list[dict[str, str]] = [vars(book) for book in self.books]

        existing_data: list[dict[str, str]] | None = None

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

    def load_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                books_data: list[dict[str, str]] | list = json.load(json_file)

                for book_data in books_data:
                    self.add_book(Book(**book_data), suppress_output=True)

            print(f'JSON data loaded from file {file_path}.')
        except FileNotFoundError as e:
            raise e
        except json.JSONDecodeError as e:
            raise e
