# module prompts

from rich.prompt import Confirm, Prompt

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
        helpers.create_interactive_table(books)
    else:
        helpers.print_info('No books in library.')

def prompt_search(library: Library) -> None:
    query: str        = Prompt.ask('Search')
    books: list[Book] = library.search_fuzz(query)

    helpers.clear_screen()

    if books:
        helpers.create_interactive_table(books)
    else:
        helpers.print_info('No books found.')

def prompt_convert() -> None:
    # TODO: deal with file already existing

    # FIXME: when no JSON file with the default file path is located and a CSV is converted to a
    #        JSON with the default file path, the program will delete the newly created JSON file on
    #        exit, even when save is selected; this needs to be fixed

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

def prompt_quit(library: Library, file_path: str) -> None:
    save: bool = Confirm.ask('Save library', default=True)

    if save:
        helpers.print_info(library.update_file(file_path))
    else:
        helpers.print_info('Library not saved.')
