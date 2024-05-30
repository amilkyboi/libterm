# module main

import os
import json

from rich.prompt import Confirm, Prompt

import helpers
import prompts
from library import Library

DEFAULT_FILE_PATH: str = '../data/library.json'

def run_app() -> None:
    library: Library = Library()

    helpers.clear_screen()

    try:
        helpers.print_info(library.load_file(DEFAULT_FILE_PATH))
    except FileNotFoundError:
        helpers.print_warn(f'The {DEFAULT_FILE_PATH} file could not be located.')

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
            helpers.print_info(f'Empty file {DEFAULT_FILE_PATH}, continuing.')
        else:
            helpers.print_error(f'Could not decode JSON from file {DEFAULT_FILE_PATH}: {e}')
            return

    while True:
        user_input: str = Prompt.ask(r'\[a]dd, \[e]dit, \[r]emove, \[l]ist, \[s]earch, e\[x]port, \[q]uit',
                                     choices=['a', 'e', 'r', 'l', 's', 'x', 'q'])

        match user_input:
            case 'a':
                helpers.clear_screen()
                prompts.prompt_add(library)
                helpers.clear_screen()
            case 'e':
                helpers.clear_screen()
                prompts.prompt_edit(library)
                helpers.clear_screen()
            case 'r':
                helpers.clear_screen()
                prompts.prompt_remove(library)
                helpers.clear_screen()
            case 'l':
                helpers.clear_screen()
                prompts.prompt_list(library)
            case 's':
                helpers.clear_screen()
                prompts.prompt_search(library)
            case 'x':
                helpers.clear_screen()
                prompts.prompt_export(DEFAULT_FILE_PATH)
            case 'q':
                helpers.print_info(library.update_file(DEFAULT_FILE_PATH))
                return

def main() -> None:
    run_app()

if __name__ == '__main__':
    main()
