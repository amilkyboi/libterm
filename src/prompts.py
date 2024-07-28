# module prompts
"""
Contains various prompts for interacting with the CLI.
"""

from pathlib import Path

from rich.prompt import Confirm, Prompt

import convert
import helpers
from book import Book
from library import Library

def prompt_add(library: Library) -> None:
    """
    Prompts the user to add a book.
    """

    status: str | None = None

    while True:
        helpers.print_mode("Add")

        if status is not None:
            helpers.print_info(status)

        isbn: str = Prompt.ask("ISBN")

        if isbn.lower() == 'q':
            break

        book: Book | None = library.book_by_isbn(isbn)

        if book is not None:
            status = f"Title: {book.title}, ISBN: {book.isbn} already exists."
        else:
            title: str = Prompt.ask("Title")

            if title.lower() == 'q':
                break

            author: str = Prompt.ask("Author")

            if author.lower() == 'q':
                break

            add_more: bool = Confirm.ask("Would you like to add more details?", default=False)

            if add_more:
                category:   str = Prompt.ask("Category",   default="-")
                cover:      str = Prompt.ask("Cover",      default="-")
                edition:    str = Prompt.ask("Edition",    default="-")
                pages:      str = Prompt.ask("Pages",      default="-")
                publisher:  str = Prompt.ask("Publisher",  default="-")
                translator: str = Prompt.ask("Translator", default="-")
                volume:     str = Prompt.ask("Volume",     default="-")
                year:       str = Prompt.ask("Year",       default="-")

                library.add_book(Book(title, author, isbn, category, cover, edition, pages,
                                      publisher, translator, volume, year))
            else:
                library.add_book(Book(title, author, isbn))

            status = f"Title: {title}, ISBN: {isbn} added successfully."

        helpers.clear_screen()

def prompt_edit(library: Library) -> None:
    """
    Prompts the user to edit a book.
    """

    status: str | None = None

    while True:
        helpers.print_mode("Edit")

        if status is not None:
            helpers.print_info(status)

        old_isbn: str = Prompt.ask("Current ISBN")

        if old_isbn.lower() == 'q':
            break

        old_book: Book | None = library.book_by_isbn(old_isbn)

        if old_book is not None:
            new_isbn: str = Prompt.ask("New ISBN")

            if new_isbn.lower() == 'q':
                break

            if new_isbn in library.index_from_isbn:
                status = f"ISBN: {new_isbn} already taken."
            else:
                new_title: str = Prompt.ask("New title")

                if new_title.lower() == 'q':
                    break

                new_author: str = Prompt.ask("New author")

                if new_author.lower() == 'q':
                    break

                add_more: bool = Confirm.ask("Would you like to add more details?", default=False)

                if add_more:
                    category:   str = Prompt.ask("Category",   default="-")
                    cover:      str = Prompt.ask("Cover",      default="-")
                    edition:    str = Prompt.ask("Edition",    default="-")
                    pages:      str = Prompt.ask("Pages",      default="-")
                    publisher:  str = Prompt.ask("Publisher",  default="-")
                    translator: str = Prompt.ask("Translator", default="-")
                    volume:     str = Prompt.ask("Volume",     default="-")
                    year:       str = Prompt.ask("Year",       default="-")

                    new_book: Book = Book(new_title, new_author, new_isbn, category, cover, edition,
                                          pages, publisher, translator, volume, year)
                    library.edit_book(old_book, new_book)
                else:
                    new_book: Book = Book(new_title, new_author, new_isbn)
                    library.edit_book(old_book, new_book)

                status = f"Title: {new_title}, ISBN: {new_isbn} edited successfully."
        else:
            status = f"ISBN: {old_isbn} not found."

        helpers.clear_screen()

def prompt_remove(library: Library) -> None:
    """
    Prompts the user to remove a book.
    """

    status: str | None = None

    while True:
        helpers.print_mode("Remove")

        if status is not None:
            helpers.print_info(status)

        isbn: str = Prompt.ask("ISBN")

        if isbn.lower() == 'q':
            break

        book: Book | None = library.book_by_isbn(isbn)

        if book is not None:
            library.remove_book(book)

            status = f"Title: {book.title}, ISBN: {book.isbn} removed successfully."
        else:
            status = f"ISBN: {isbn} not found."

        helpers.clear_screen()

def prompt_list(library: Library) -> None:
    """
    Prompts the user to list the books.
    """

    books: list[Book] = library.books

    if books:
        helpers.create_interactive_table(books)
    else:
        helpers.print_info("No books in library.")

def prompt_search(library: Library) -> None:
    """
    Prompts the user to search the books.
    """

    query: str        = Prompt.ask("Search")
    books: list[Book] = library.search_fuzz(query)

    helpers.clear_screen()

    if books:
        helpers.create_interactive_table(books)
    else:
        helpers.print_info("No books found.")

def prompt_convert(library: Library) -> None:
    """
    Prompts the user to convert files.
    """

    choice: str = Prompt.ask(r"\[i]mport, \[e]xport, \[q]uit", choices=['i', 'e', 'q'])

    match choice:
        case 'i':
            file_name:      str  = Prompt.ask("CSV file name")
            file_path_csv:  Path = Path(f"../data/{file_name}.csv")
            file_path_json: Path = file_path_csv.with_suffix(".json")

            # If a JSON file with the selected name already exists, don't import the CSV
            if file_path_json.is_file():
                helpers.print_warn(f"File {file_path_json} already exists. File not imported.")
                return

            try:
                convert.csv_to_json(file_path_csv, file_path_json)

                # NOTE: 07/26/24 - when no JSON file with the default file path is located and a CSV
                #       is converted to a JSON with the default file path, ensure that the data is
                #       loaded into the library
                library.load_file(file_path_json)

                helpers.print_info(f"File {file_path_csv} imported to {file_path_json}.")
            except FileNotFoundError:
                helpers.print_warn(f"The {file_path_csv} file could not be located.")

        case 'e':
            file_name:      str  = Prompt.ask("JSON file name")
            file_path_csv:  Path = Path(f"../data/{file_name}.csv")
            file_path_json: Path = file_path_csv.with_suffix(".json")

            # If a CSV file with the selected name already exists, don't export the JSON
            if file_path_csv.is_file():
                helpers.print_warn(f"File {file_path_csv} already exists. File not exported.")
                return

            try:
                convert.json_to_csv(file_path_csv, file_path_json)
                helpers.print_info(f"File {file_path_json} exported to {file_path_csv}.")
            except FileNotFoundError:
                helpers.print_warn(f"The {file_path_json} file could not be located.")

def prompt_quit(library: Library, file_path: Path) -> None:
    """
    Prompts the user to quit the program.
    """

    save: bool = Confirm.ask("Save library", default=True)

    if save:
        helpers.print_info(library.update_file(file_path))
    else:
        helpers.print_info("Library not saved.")
