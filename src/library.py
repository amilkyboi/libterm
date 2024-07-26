# module library
"""
Contains the implementation of the Library class.
"""

import os
import re
import json
from pathlib import Path
from re import Pattern, Match
from collections import defaultdict

from book import Book

class Library:
    """
    A library.
    """

    def __init__(self) -> None:
        self.books:             list[Book]                  = []
        self.index_from_title:  defaultdict[str, list[int]] = defaultdict(list)
        self.index_from_author: defaultdict[str, list[int]] = defaultdict(list)
        self.index_from_isbn:   dict[str, int]              = {}

    def add_book(self, book: Book) -> None:
        """
        Adds a book to the list and updates all dictionaries.
        """

        # NOTE: 05/30/24 - only called if the book doesn't exist; enforced in main.py

        self.books.append(book)

        book_index: int = len(self.books) - 1

        self.index_from_title[book.title].append(book_index)
        self.index_from_author[book.author].append(book_index)
        self.index_from_isbn[book.isbn] = book_index

    def edit_book(self, old_book: Book, new_book: Book) -> None:
        """
        Removes the old book and adds the new one.
        """

        # NOTE: 05/30/24 - only called if the book exists and the new ISBN isn't taken; enforced in
        #       main.py

        self.remove_book(old_book)
        self.add_book(new_book)

    def remove_book(self, book: Book) -> None:
        """
        Removes a book from the list and updates all dictionaries.
        """

        # NOTE: 05/30/24 - only called if the book exists; enforced in main.py

        isbn:       str = book.isbn
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

    def books_by_title(self, title: str) -> list[Book]:
        """
        Returns a list of books with the given title.
        """

        return [self.books[i] for i in self.index_from_title[title]]

    def books_by_author(self, author: str) -> list[Book]:
        """
        Returns a list of books with the given author.
        """

        return [self.books[i] for i in self.index_from_author[author]]

    def book_by_isbn(self, isbn: str) -> Book | None:
        """
        Returns the book with the given ISBN.
        """

        try:
            return self.books[self.index_from_isbn[isbn]]
        except KeyError:
            return None

    def search_list(self, query: str) -> list[Book]:
        """
        Returns a list of books matching the query. Searches the list of books using regex.
        """

        pattern = re.compile(re.escape(query), re.IGNORECASE)
        results = []

        for book in self.books:
            if (pattern.search(book.title) or pattern.search(book.author) or
                pattern.search(book.isbn)):
                results.append(book)

        return results

    def search_dict(self, query: str) -> list[Book]:
        """
        Returns a list of books matching the query. Searches the dictionaries using regex.
        """

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

    def search_fuzz(self, query: str) -> list[Book]:
        """
        Returns a list of books matching the query. Searches the dictionaries using fuzzy finding.
        """

        matched_indices: set = set()

        def fuzz(query: str, collection: dict) -> list[str]:
            # fuzzy finder adapted from: https://blog.amjith.com/fuzzyfinder-in-10-lines-of-python
            suggestions: list[tuple[int, int, str]] = []
            pattern:     str                        = ".*?".join(re.escape(query))
            regex:       Pattern[str]               = re.compile(pattern, re.IGNORECASE)

            for item in collection:
                match: Match[str] | None = regex.search(item)

                if match is not None:
                    suggestions.append((len(match.group()), match.start(), item))

            return [x for _, _, x in sorted(suggestions)]

        for title in fuzz(query, self.index_from_title):
            matched_indices.update(self.index_from_title[title])

        for author in fuzz(query, self.index_from_author):
            matched_indices.update(self.index_from_author[author])

        for isbn in fuzz(query, self.index_from_isbn):
            matched_indices.add(self.index_from_isbn[isbn])

        return [self.books[i] for i in matched_indices]

    def update_file(self, file_path: Path) -> str:
        """
        Creates, updates, or removes a JSON file containing information about each book.
        """

        existing_file: bool = file_path.is_file()

        books_data: list[dict] = [vars(book) for book in self.books]

        existing_data: list[dict] | None = None

        if existing_file:
            with open(file_path, 'r', encoding="utf-8") as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    existing_data = None

        if existing_data == books_data:
            if self.books:
                return f"File {file_path} already up-to-date. No changes made."

            os.remove(file_path)
            return f"File {file_path} already up-to-date and will be removed due to empty list."

        if self.books:
            with open(file_path, 'w', encoding="utf-8") as json_file:
                json.dump(books_data, json_file, indent=4)

            if existing_file:
                return f"Updated file {file_path} successfully."

            return f"Created file {file_path} successfully."

        if existing_file:
            os.remove(file_path)
            return f"Removed file {file_path} as the book list is empty."

        return "No books in list. File not created."

    def load_file(self, file_path: Path) -> str:
        """
        Loads an existing JSON file and adds the corresponding books into memory.
        """

        try:
            with open(file_path, 'r', encoding="utf-8") as json_file:
                books_data: list[dict] | list = json.load(json_file)

                for book_data in books_data:
                    self.add_book(Book(**book_data))

            return f"JSON data loaded from file {file_path}."
        except FileNotFoundError as e:
            raise e
        except json.JSONDecodeError as e:
            raise e
