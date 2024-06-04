# module book

class Book:
    def __init__(self, title: str, author: str, isbn: str, publisher: str = 'not_set',
                 cover: str = 'not_set', category: str = 'not_set', edition: int = 0, year: int = 0,
                 pages: int = 0) -> None:
        self.title:     str = title
        self.author:    str = author
        self.isbn:      str = isbn
        self.publisher: str = publisher
        self.cover:     str = cover
        self.category:  str = category
        self.edition:   int = edition
        self.year:      int = year
        self.pages:     int = pages
