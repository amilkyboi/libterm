# module prompts

import math

from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import print as rprint

import convert
import helpers
from book import Book
from library import Library

def prompt_add(library: Library) -> None:
    status: str | None = None

    # TODO: add secondary prompt where more details can be added

    while True:
        helpers.print_mode('Add')

        if status:
            helpers.print_info(status)

        isbn: str = Prompt.ask('ISBN')

        if isbn.lower() == 'q':
            break

        book: Book | None = library.book_by_isbn(isbn)

        if book:
            status = f'Title: {book.title}, ISBN: {book.isbn} already exists.'
        else:
            title: str = Prompt.ask('Title')

            if title.lower() == 'q':
                break

            author: str = Prompt.ask('Author')

            if author.lower() == 'q':
                break

            library.add_book(Book(title, author, isbn))

            status = f'Title: {title}, ISBN: {isbn} added successfully.'

        helpers.clear_screen()

def prompt_edit(library: Library) -> None:
    status: str | None = None

    # TODO: add secondary prompt where more details can be added

    while True:
        helpers.print_mode('Edit')

        if status:
            helpers.print_info(status)

        isbn: str = Prompt.ask('Current ISBN')

        if isbn.lower() == 'q':
            break

        book: Book | None = library.book_by_isbn(isbn)

        if book:
            new_isbn: str = Prompt.ask('New ISBN')

            if new_isbn.lower() == 'q':
                break

            if new_isbn in library.index_from_isbn:
                status = f'ISBN: {new_isbn} already taken.'
            else:
                new_title: str = Prompt.ask('New title')

                if new_title.lower() == 'q':
                    break

                new_author: str = Prompt.ask('New author')

                if new_author.lower() == 'q':
                    break

                library.edit_book(book, new_title, new_author, new_isbn)

                status = f'Title: {new_title}, ISBN: {new_isbn} edited successfully.'
        else:
            status = f'ISBN: {isbn} not found.'

        helpers.clear_screen()

def prompt_remove(library: Library) -> None:
    status: str | None = None

    while True:
        helpers.print_mode('Remove')

        if status:
            helpers.print_info(status)

        isbn: str = Prompt.ask('ISBN')

        if isbn.lower() == 'q':
            break

        book: Book | None = library.book_by_isbn(isbn)

        if book:
            library.remove_book(book)

            status = f'Title: {book.title}, ISBN: {book.isbn} removed successfully.'
        else:
            status = f'ISBN: {isbn} not found.'

        helpers.clear_screen()

def prompt_list(library: Library) -> None:
    books: list[Book] = library.books

    if books:
        page:      int = 0
        page_size: int = 5
        max_page:  int = math.ceil(len(books) / page_size)

        while True:
            table: Table = helpers.create_table_large()

            start: int = page_size * page
            end:   int = start + page_size

            end = min(end, len(books))

            for i in range(start, end):
                table.add_row(books[i].title, books[i].author, books[i].isbn, books[i].publisher,
                              books[i].cover, books[i].category, str(books[i].edition),
                              str(books[i].year), str(books[i].pages))

            rprint(Align(Panel(table, title=f'Page {page + 1} of {max_page}'), align='center'))

            if max_page > 1:
                prompt: str = Prompt.ask(r'\[n]ext, \[p]rev, \[g]oto, \[q]uit',
                                         choices=['n', 'p', 'g', 'q'])

                match prompt:
                    case 'n':
                        if end != len(books):
                            page += 1
                    case 'p':
                        if page != 0:
                            page -= 1
                    case 'g':
                        while True:
                            page_no: str = Prompt.ask('Page')

                            if page_no.isdigit():
                                page = int(page_no) - 1

                                if 0 <= page < max_page:
                                    break

                            helpers.print_error('Enter a valid page number.')
                    case 'q':
                        break

                helpers.clear_screen()
            else:
                break
    else:
        helpers.print_info('No books in library.')

def prompt_search(library: Library) -> None:
    query: str        = Prompt.ask('Search')
    books: list[Book] = library.search_fuzz(query)

    helpers.clear_screen()

    if books:
        page:      int = 0
        page_size: int = 5
        max_page:  int = math.ceil(len(books) / page_size)

        while True:
            table: Table = helpers.create_table_small()

            start: int = page_size * page
            end:   int = start + page_size

            end = min(end, len(books))

            for i in range(start, end):
                table.add_row(books[i].title, books[i].author, books[i].isbn)

            rprint(Align(Panel(table, title=f'Page {page + 1} of {max_page}'), align='center'))

            if max_page > 1:
                prompt: str = Prompt.ask(r'\[n]ext, \[p]rev, \[g]oto, \[q]uit',
                                         choices=['n', 'p', 'g', 'q'])

                match prompt:
                    case 'n':
                        if end != len(books):
                            page += 1
                    case 'p':
                        if page != 0:
                            page -= 1
                    case 'g':
                        while True:
                            page_no: str = Prompt.ask('Page')

                            if page_no.isdigit():
                                page = int(page_no) - 1

                                if 0 <= page < max_page:
                                    break

                            helpers.print_error('Enter a valid page number.')
                    case 'q':
                        break

                helpers.clear_screen()
            else:
                break
    else:
        helpers.print_info('No books found.')

def prompt_convert() -> None:
    # TODO: deal with file already existing
    # TODO: when no JSON file is located and a CSV is converted to a JSON, the program will delete
    #       it; this needs to be fixed

    choice: str = Prompt.ask(r'\[i]mport, \[e]xport, \[q]uit', choices=['i', 'e', 'q'])

    match choice:
        case 'i':
            file_name: str = Prompt.ask('CSV file name')

            try:
                convert.csv_to_json(file_name)
                helpers.print_info(f'File {file_name}.csv imported to {file_name}.json.')
            except FileNotFoundError:
                helpers.print_warn(f'The {file_name}.csv file could not be located.')
        case 'e':
            file_name: str = Prompt.ask('JSON file name')

            try:
                convert.json_to_csv(file_name)
                helpers.print_info(f'File {file_name}.json exported to {file_name}.csv.')
            except FileNotFoundError:
                helpers.print_warn(f'The {file_name}.json file could not be located.')
