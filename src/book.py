# module book
"""
Contains the implementation of the Book class.
"""

from dataclasses import dataclass

@dataclass
class Book:
    """
    A book.
    """

    title:     str
    author:    str
    isbn:      str

    category:   str = "-"
    cover:      str = "-"
    edition:    str = "-"
    pages:      str = "-"
    publisher:  str = "-"
    translator: str = "-"
    volume:     str = "-"
    year:       str = "-"
