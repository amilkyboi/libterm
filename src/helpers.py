# module helpers

import os

from rich import box
from rich.table import Table
from rich import print as rprint

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

def create_table_small() -> Table:
    table: Table = Table(box=box.HORIZONTALS, row_styles=['', 'dim'])

    table.add_column('Title', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Author', style='#74c7ec', header_style='#74c7ec')
    table.add_column('ISBN', style='#b4befe', header_style='#b4befe')

    return table

def create_table_large() -> Table:
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
