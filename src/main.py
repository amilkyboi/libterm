import os
import json

from rich.table import Table
from rich import print as rprint

from book import Book
from library import Library

DEFAULT_FILE_PATH = '../data/library.json'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_add(library: Library):
    while True:
        title = input('Title: ')

        if title.lower() == 'q':
            break

        author = input('Author: ')

        if author.lower() == 'q':
            break

        isbn = input('ISBN: ')

        if isbn.lower() == 'q':
            break

        library.add_book(Book(title, author, isbn))

        break

def prompt_remove(library: Library):
    while True:
        isbn = input('ISBN: ')

        if isbn.lower() == 'q':
            break

        library.remove_book(isbn)

        break

def prompt_list(library: Library):
    table = Table(title='Library')

    table.add_column('Title')
    table.add_column('Author')
    table.add_column('ISBN')

    for book in library.list_books():
        table.add_row(book.title, book.author, book.isbn)

    rprint(table)

def run_app():
    library = Library()

    clear_screen()

    try:
        library.load_file(DEFAULT_FILE_PATH)
    except FileNotFoundError:
        print(
            f'The {DEFAULT_FILE_PATH} file could not be located. '
            f'Create a new {DEFAULT_FILE_PATH} file?'
        )

        while True:
            choice = input('[y]es, [q]uit: ')

            match choice:
                case 'y':
                    # let the main loop handle the file: if book(s) are created, then a new
                    # library.json file is made, otherwise the main loop will exit without anything
                    # being saved
                    break
                case 'q':
                    return
    except json.JSONDecodeError:
        # once here, we know a file exists
        is_empty = os.stat(DEFAULT_FILE_PATH).st_size == 0

        if is_empty:
            # act on the file normally if the contents are completely empty
            pass
        else:
            return

    clear_screen()

    while True:
        user_input = input('[a]dd, [r]emove, [l]ist, [q]uit: ')

        match user_input:
            case 'q':
                library.update_file(DEFAULT_FILE_PATH)
                return
            case 'a':
                clear_screen()
                prompt_add(library)
            case 'r':
                clear_screen()
                prompt_remove(library)
            case 'l':
                clear_screen()
                prompt_list(library)

def main():
    run_app()

if __name__ == '__main__':
    main()
