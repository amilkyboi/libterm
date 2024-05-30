# module helpers

import os
import math

from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import print as rprint

from book import Book

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_mode(message: str) -> None:
    rprint(rf'[green]MODE: {message}. Press \[q] to exit.[/green]')

def print_info(message: str) -> None:
    rprint(f'[blue]INFO: {message}[/blue]')

def print_warn(message: str) -> None:
    rprint(f'[yellow]WARN: {message}[/yellow]')

def print_error(message: str) -> None:
    rprint(f'[red]ERROR: {message}[/red]')

def initialize_small_table() -> Table:
    table: Table = Table(box=box.HORIZONTALS, row_styles=['', 'dim'])

    table.add_column('Title', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Author', style='#74c7ec', header_style='#74c7ec')
    table.add_column('ISBN', style='#b4befe', header_style='#b4befe')

    return table

def initialize_large_table() -> Table:
    table: Table = Table(box=box.HORIZONTALS, row_styles=['', 'dim'])

    table.add_column('Title', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Author', style='#74c7ec', header_style='#74c7ec')
    table.add_column('ISBN', style='#b4befe', header_style='#b4befe')
    table.add_column('Publisher', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Cover', style='#74c7ec', header_style='#74c7ec')
    table.add_column('Category', style='#b4befe', header_style='#b4befe')
    table.add_column('Edition', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Year', style='#74c7ec', header_style='#74c7ec')
    table.add_column('Pages', style='#b4befe', header_style='#b4befe')

    return table

def create_interactive_table(books: list[Book], table_type: str = 'small') -> None:
    page:      int = 0
    page_size: int = 5
    max_page:  int = math.ceil(len(books) / page_size)

    while True:
        start: int = page_size * page
        end:   int = start + page_size

        end = min(end, len(books))

        match table_type:
            case 'small':
                table: Table = initialize_small_table()
                for i in range(start, end):
                    table.add_row(books[i].title, books[i].author, books[i].isbn)
            case 'large':
                table: Table = initialize_large_table()
                for i in range(start, end):
                    table.add_row(books[i].title, books[i].author, books[i].isbn,
                                    books[i].publisher, books[i].cover, books[i].category,
                                    str(books[i].edition), str(books[i].year),
                                    str(books[i].pages))

        rprint(Align(Panel(table, title=f'Page {page + 1} of {max_page}'), align='center'))

        # TODO: remove next, prev, and goto options for tables that only have one page

        prompt: str = Prompt.ask(r'\[n]ext, \[p]rev, \[g]oto, \[t]oggle details, \[q]uit',
                                    choices=['n', 'p', 'g', 't', 'q'])

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

                    print_error('Enter a valid page number.')
            case 't':
                if table_type == 'small':
                    table_type = 'large'
                else:
                    table_type = 'small'
            case 'q':
                break

        clear_screen()
