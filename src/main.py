# module main

import os
import json

from rich import box
from rich.table import Table
from rich import print as rprint
from rich.prompt import Prompt, Confirm

from book import Book
from library import Library
from export import json_to_csv

DEFAULT_FILE_PATH: str = '../data/library.json'

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_add(library: Library) -> None:
    print('Add mode. Enter [q] to quit.')

    while True:
        title: str = Prompt.ask('Title')

        if title.lower() == 'q':
            break

        author: str = Prompt.ask('Author')

        if author.lower() == 'q':
            break

        isbn: str = Prompt.ask('ISBN')

        if isbn.lower() == 'q':
            break

        library.add_book(Book(title, author, isbn))

def prompt_remove(library: Library) -> None:
    print('Remove mode. Enter [q] to quit.')

    while True:
        isbn: str = Prompt.ask('ISBN')

        if isbn.lower() == 'q':
            break

        library.remove_book(isbn)

def prompt_list(library: Library) -> None:
    table: Table = create_table()

    for book in library.books:
        table.add_row(book.title, book.author, book.isbn)

    rprint(table)

def prompt_search(library: Library) -> None:
    table: Table = create_table()
    query: str   = Prompt.ask('Search')

    books: list[Book] = library.search_fuzz(query)

    for book in books:
        table.add_row(book.title, book.author, book.isbn)

    rprint(table)

def prompt_export() -> None:
    # TODO: deal with file already existing

    do_export = Confirm.ask('Convert the saved JSON to CSV?')

    if do_export:
        csv_file_path = json_to_csv(DEFAULT_FILE_PATH)
        print(f'File {DEFAULT_FILE_PATH} exported to {csv_file_path}.')

def create_table() -> Table:
    table: Table = Table(box=box.HORIZONTALS, row_styles=['', 'dim'])

    table.add_column('Title', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Author', style='#74c7ec', header_style='#74c7ec')
    table.add_column('ISBN', style='#b4befe', header_style='#b4befe')

    return table

def run_app() -> None:
    library: Library = Library()

    try:
        library.load_file(DEFAULT_FILE_PATH)
    except FileNotFoundError:
        print(f'The {DEFAULT_FILE_PATH} file could not be located.')

        while True:
            choice: bool = Confirm.ask(f'Create a new {DEFAULT_FILE_PATH} file?')

            match choice:
                case True:
                    break
                case False:
                    return
    except json.JSONDecodeError as e:
        is_empty: bool = os.stat(DEFAULT_FILE_PATH).st_size == 0

        if is_empty:
            print(f'Empty file {DEFAULT_FILE_PATH}, continuing.')
        else:
            print(f'ERROR: Error decoding JSON from file {DEFAULT_FILE_PATH}: {e}')
            return

    while True:
        user_input: str = Prompt.ask(r'\[a]dd, \[r]emove, \[l]ist, \[s]earch, \[e]xport, \[q]uit',
                                     choices=['a', 'r', 'l', 's', 'e', 'q'])

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
            case 'e':
                clear_screen()
                prompt_export()
            case 'q':
                library.update_file(DEFAULT_FILE_PATH)
                return

def main() -> None:
    run_app()

if __name__ == '__main__':
    main()
