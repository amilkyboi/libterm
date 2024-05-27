from typing import Self

class Book:
    def __init__(self, title: str, author: str, isbn: str) -> None:
        self.title:  str = title
        self.author: str = author
        self.isbn:   str = isbn

    def __str__(self) -> str:
        return f'Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}'

    def to_dict(self) -> dict[str, str]:
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(title=data['title'], author=data['author'], isbn=data['isbn'])
