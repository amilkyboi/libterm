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
    publisher: str = "not_set"
    cover:     str = "not_set"
    category:  str = "not_set"
    edition:   str = "not_set"
    year:      str = "not_set"
    pages:     str = "not_set"
