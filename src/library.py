import json

from book import Book

class Library:
    def __init__(self) -> None:
        self.books: list[Book] = []

    def add_book(self, book: Book) -> None:
        # NOTE: Adding books requires all fields in the Book class to be filled out

        if self.book_by_isbn(book.isbn):
            print('Book already exists.')
        else:
            self.books.append(book)
            print('Book added successfully.')

    def remove_book(self, isbn: str) -> None:
        # NOTE: Removing a book only requires the ISBN, assuming that no two books share the same
        #       ISBN

        book = self.book_by_isbn(isbn)

        if book:
            self.books.remove(book)
            print('Book removed successfully.')
        else:
            print('Book not found.')

    def list_books(self) -> list[Book] | None:
        if self.books:
            for book in self.books:
                print(book)

        return None

    def book_by_isbn(self, isbn: str) -> Book | None:
        for book in self.books:
            if book.isbn == isbn:
                return book

        return None

    def books_by_author(self, author):
        return [book for book in self.books if book.author == author]

    def save_books(self, file_path: str):
        books_data = [book.to_dict() for book in self.books]

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(books_data, json_file)
        
        print(f'JSON data saved to file {file_path}.')

    def load_books(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                books_data = json.load(json_file)

                # TODO: Suppress output from books being added via JSON read
                for book_data in books_data:
                    self.add_book(Book.from_dict(book_data))

            print(f'JSON data loaded from file {file_path}.')
        except FileNotFoundError:
            # TODO: Prompt the user to either create a new file or exit the program
            print(f'ERROR: File {file_path} not found.')
        except json.JSONDecodeError:
            print(f'ERROR: Error decoding JSON from file {file_path}.')
