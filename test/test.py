# module test

import timeit

setup_code = '''
import sys

sys.path.append('../src')

from book import Book
from library import Library

library = Library()

for i in range(1000):
    library.add_book(Book(f'title {i}', f'author {i % 100}', f'{i:013d}'))

query = 'title 50'
'''

search_list = '''
library.search_list(query)
'''

search_dict = '''
library.search_dict(query)
'''

search_fuzz = '''
library.search_fuzz(query)
'''

num_runs = 5
num_exec = 1000

list_time = timeit.Timer(stmt=search_list, setup=setup_code).repeat(num_runs, num_exec)
dict_time = timeit.Timer(stmt=search_dict, setup=setup_code).repeat(num_runs, num_exec)
fuzz_time = timeit.Timer(stmt=search_fuzz, setup=setup_code).repeat(num_runs, num_exec)

print(f'Searching 1000 books {num_exec} times over {num_runs} runs took:')
print(f'List-based: {min(list_time) / num_exec:.8f} seconds')
print(f'Dict-based: {min(dict_time) / num_exec:.8f} seconds')
print(f'Fuzz-based: {min(fuzz_time) / num_exec:.8f} seconds')
