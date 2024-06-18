# module book
"""
Contains the implementation of the Book class.
"""

class Book:
    """
    A book.
    """

    def __init__(self, title: str, author: str, isbn: str, publisher: str = "not_set",
                 cover: str = "not_set", category: str = "not_set", edition: str = "not_set",
                 year: str = "not_set", pages: str = "not_set") -> None:
        self.title:     str = title
        self.author:    str = author
        self.isbn:      str = isbn
        self.publisher: str = publisher
        self.cover:     str = cover
        self.category:  str = category
        self.edition:   str = edition
        self.year:      str = year
        self.pages:     str = pages
