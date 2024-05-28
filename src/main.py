import os
import json

from rich import box
from rich.table import Table
from rich import print as rprint
from rich.prompt import Prompt, Confirm

from book import Book
from library import Library

DEFAULT_FILE_PATH = '../data/library.json'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_add(library: Library):
    print('Add mode. Enter [q] to quit.')

    while True:
        title = Prompt.ask('Title')

        if title.lower() == 'q':
            break

        author = Prompt.ask('Author')

        if author.lower() == 'q':
            break

        isbn = Prompt.ask('ISBN')

        if isbn.lower() == 'q':
            break

        library.add_book(Book(title, author, isbn))

def prompt_remove(library: Library):
    print('Remove mode. Enter [q] to quit.')

    while True:
        isbn = Prompt.ask('ISBN')

        if isbn.lower() == 'q':
            break

        library.remove_book(isbn)

def prompt_list(library: Library):
    table = create_table()

    for book in library.books:
        table.add_row(book.title, book.author, book.isbn)

    rprint(table)

def prompt_search(library: Library):
    table = create_table()
    query = Prompt.ask('Search')

    books = library.books_by_title(query)

    for book in books:
        table.add_row(book.title, book.author, book.isbn)

    rprint(table)

def create_table():
    table = Table(box=box.HORIZONTALS, row_styles=['', 'dim'])

    table.add_column('Title', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Author', style='#74c7ec', header_style='#74c7ec')
    table.add_column('ISBN', style='#b4befe', header_style='#b4befe')

    return table

def run_app():
    library = Library()

    try:
        library.load_file(DEFAULT_FILE_PATH)
    except FileNotFoundError:
        print(f'The {DEFAULT_FILE_PATH} file could not be located.')

        while True:
            choice = Confirm.ask(f'Create a new {DEFAULT_FILE_PATH} file?')

            match choice:
                case True:
                    break
                case False:
                    return
    except json.JSONDecodeError as e:
        is_empty = os.stat(DEFAULT_FILE_PATH).st_size == 0

        if is_empty:
            print(f'Empty file {DEFAULT_FILE_PATH}, continuing.')
        else:
            print(f'ERROR: Error decoding JSON from file {DEFAULT_FILE_PATH}: {e}')
            return

    while True:
        user_input = Prompt.ask(r'\[a]dd, \[r]emove, \[l]ist, \[s]earch, \[q]uit',
                                choices=['a', 'r', 'l', 's', 'q'])

        match user_input:
            case 'a':
                clear_screen()
                prompt_add(library)
            case 'r':
                clear_screen()
                prompt_remove(library)
            case 'l':
                clear_screen()
                prompt_list(library)
            case 's':
                clear_screen()
                prompt_search(library)
            case 'q':
                library.update_file(DEFAULT_FILE_PATH)
                return

def main():
    run_app()

if __name__ == '__main__':
    main()
