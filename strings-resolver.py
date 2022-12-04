#!/usr/bin/env python3
from os import popen
from argparse import ArgumentParser
from colorama import Fore
import base64
base64.b
# Forensics Strings resolver


def parse_arguments():
    parser = ArgumentParser(description='Search for the flag in strings output')
    parser.add_argument('-f', '--flag-format')
    parser.add_argument('-d', '--debug', action='store_true') # this option is used to make the testing easier
    return parser.parse_args()


def check_plain_flag(data):
    for line in data:
        if flag_format in line:
            print(f"{Fore.RED}{line}{Fore.RESET}")
            return True


def check_base64_flag(data):
    for line in data:
        base64_flag = base64.b64encode(flag_format.encode('ascii')).decode('ascii').replace('=', '')
        base64_flag = base64_flag[:len(base64_flag)-1] # to avoid the last digit unmatching

        if line.startswith(base64_flag):
            print(f"{Fore.RED}{line} -> {base64.b64decode(line.encode('ascii')).decode('ascii')}{Fore.RESET}")
            return True


if __name__ == '__main__':
    args = parse_arguments()
    if args.debug:
        file_name = 'image.png'
        flag_format = 'TUCTF'
    else:
        file_name = input('Enter the file name: ')
        flag_format = input('Enter the flag format')

    strings_output = popen(f'strings "{file_name}"').read()
    lines = strings_output.split('\n')

    print(f'{Fore.GREEN}no plain-text flag found{Fore.RESET}') if not check_plain_flag(lines[:]) else None
    print(f'{Fore.GREEN}no base64 flag found{Fore.RESET}') if not check_base64_flag(lines[:]) else None