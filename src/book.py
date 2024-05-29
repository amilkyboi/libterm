# module book

class Book:
    def __init__(self, title: str, author: str, isbn: str) -> None:
        self.title:  str = title
        self.author: str = author
        self.isbn:   str = isbn
