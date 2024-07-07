from argparse import ArgumentParser, Namespace
from requests import get
from PIL import Image
from os import walk, path
from re import match
from shutil import rmtree
import colorama
from typing import Callable
from time import perf_counter


COLORS = {
    "ERR": f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}",
    "INFO": f"{colorama.Style.DIM}{colorama.Fore.YELLOW}",
    "FLAG": f"{colorama.Fore.RED}{colorama.Fore.GREEN}",
    "ENC_FLAG": f"{colorama.Fore.RED}{colorama.Fore.BLUE}",
    "RESET": colorama.Style.RESET_ALL,
}


def online() -> bool:
    urls = ['https://google.com', 'https://www.nitrxgen.net']
    try:
        for url in urls:
            if get(url):
                return True
        else:
            return False
    except Exception as e:
        return False


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description='Search for the flag in strings output')
    parser.add_argument('-f', '--flag-format', help='Specify beginning of flag format (Ex: TUCTF)')
    parser.add_argument('-n', '--file-name', help='Specify the file name')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-s', '--silent', action='store_true', help='print flags only')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='ignore case sensitivity')
    parser.add_argument('-nr', '--no-rot', action='store_true', help='Disable rotation')
    parser.add_argument('-t', '--threads', type=int, help='Number of threads to use', default=10)
    parser.add_argument('-p', '--parallel-process', type=int, help='Number of parallel processes to use', default=10)
    parser.add_argument('-l', '--length', type=int, help='maximum length of the flag', default=40)
    #! Future options
        #TODO --crack
        #TODO --steg
    return parser.parse_args()


def is_png(file_path: str) -> bool:
    try:
        with Image.open(file_path) as image:
            return image.format == 'PNG'
    except IOError:
        return False
    

def get_valid_files(directory: str) -> list:
    valid_files = []
    for root, _, files in walk(directory):
        if match(r".*_rotates$", root):
            rmtree(root)
        else:
            for file in files:
                valid_files.append(path.join(root, file))
            
    return valid_files


def timeit(func: Callable):
    def wrapper():
        st = perf_counter()
        func()
        print(f'{func.__name__} took {(perf_counter() - st)} sec')
    return wrapper
