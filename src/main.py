# module main
"""
Contains the main loop for running the CLI.
"""

import os
import json

from rich.prompt import Confirm, Prompt

import helpers
import prompts
from library import Library

DEFAULT_FILE_PATH: str = "../data/library.json"

def run_cli() -> None:
    """
    Runs the interactive CLI until terminated by the user.
    """

    library: Library = Library()

    helpers.clear_screen()

    try:
        helpers.print_info(library.load_file(DEFAULT_FILE_PATH))

    except FileNotFoundError:
        helpers.print_warn(f"The {DEFAULT_FILE_PATH} file could not be located.")

        while True:
            choice: bool = Confirm.ask(f"Create a new {DEFAULT_FILE_PATH} file?")

            match choice:
                case True:
                    break
                case False:
                    return

    except json.JSONDecodeError as e:
        is_empty: bool = os.stat(DEFAULT_FILE_PATH).st_size == 0

        if is_empty:
            helpers.print_info(f"Empty file {DEFAULT_FILE_PATH}, continuing.")
        else:
            helpers.print_error(f"Could not decode JSON from file {DEFAULT_FILE_PATH}: {e}")
            return

    while True:
        user_input: str = Prompt.ask(r"\[a]dd, \[e]dit, \[r]emove, \[l]ist, \[s]earch, \[c]onvert, \[q]uit",
                                     choices=['a', 'e', 'r', 'l', 's', 'c', 'q'])

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
                helpers.clear_screen()
            case 's':
                helpers.clear_screen()
                prompts.prompt_search(library)
                helpers.clear_screen()
            case 'c':
                helpers.clear_screen()
                prompts.prompt_convert()
            case 'q':
                helpers.clear_screen()
                prompts.prompt_quit(library, DEFAULT_FILE_PATH)
                return

def main() -> None:
    """
    Runs the program.
    """

    run_cli()

if __name__ == "__main__":
    main()
