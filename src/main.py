import os

from book import Book
from library import Library

library = Library()
file_path = '../data/test.json'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_add():
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

def prompt_remove():
    while True:
        isbn = input('ISBN: ')

        if isbn.lower() == 'q':
            break

        library.remove_book(isbn)

        break

def prompt_list():
    library.list_books()

def main():
    clear_screen()

    # TODO: Prompt the user to either create a new file or exit
    library.load_books(file_path)

    while True:
        user_input = input('[a]dd, [r]emove, [l]ist, [q]uit: ')

        match user_input:
            case 'q':
                # TODO: Add a separate prompt to save the book list to prevent accidental overwrites
                library.save_books(file_path)
                break
            case 'a':
                clear_screen()
                prompt_add()
            case 'r':
                clear_screen()
                prompt_remove()
            case 'l':
                clear_screen()
                prompt_list()

if __name__ == '__main__':
    main()
