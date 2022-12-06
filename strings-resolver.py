#!/usr/bin/env python3
from os import popen
from argparse import ArgumentParser
from colorama import Fore
import base64
import binascii
# Forensics Strings resolver


def parse_arguments():
    parser = ArgumentParser(description='Search for the flag in strings output')
    parser.add_argument('-f', '--flag-format', help='Specify beginning of flag format (Ex: TUCTF)')
    parser.add_argument('-n', '--file-name', help='Specify the file name')
    parser.add_argument('-d', '--debug', action='store_true', help='Don\'t ask for input and Auto fill them')  # this option is used to make the testing easier
    return parser.parse_args()


def check_plain_flag(data):
    found = False

    for line in data:
        if flag_format in line:
            print(f"{Fore.RED}{line}{Fore.RESET}")
            found = True
    return found


def check_base16_flag(data):
    found = False
    for line in data:
        base16_flag = base64.b16encode(flag_format.encode('ascii')).decode('ascii')

        if base16_flag in line:
            print(f"{Fore.RED}{line} -> {base64.b16decode(line.encode('ascii')).decode('ascii')}{Fore.RESET}")
            found = True
    return found


def check_base32_flag(data):
    found = False
    for line in data:
        base32_flag = base64.b32encode(flag_format.encode('ascii')).decode('ascii').replace('=', '')
        base32_flag = base32_flag[:len(base32_flag) - 1]  # to avoid the last digit unmatching

        if line.startswith(base32_flag):
            print(f"{Fore.RED}{line} -> {base64.b32decode(line.encode('ascii')).decode('ascii')}{Fore.RESET}")
            found = True
    return found


def check_base64_flag(data):
    found = False
    for line in data:
        base64_flag = base64.b64encode(flag_format.encode('ascii')).decode('ascii').replace('=', '')
        base64_flag = base64_flag[:len(base64_flag)-1]  # to avoid the last digit unmatching

        if base64_flag in line:
            print(f"{Fore.RED}{line} -> {base64.b64decode(line.encode('ascii')).decode('ascii')}{Fore.RESET}")
            found = True
    return found


def check_base85_flag(data):
    found = False
    for line in data:
        base85_flag = base64.b85encode(flag_format.encode('ascii')).decode('ascii').replace('=', '')
        base85_flag = base85_flag[:len(base85_flag)-1]  # to avoid the last digit unmatching

        if line.startswith(base85_flag):
            print(f"{Fore.RED}{line} -> {base64.b85decode(line.encode('ascii')).decode('ascii')}{Fore.RESET}")
            found = True
    return found


def check_binary_flag(data):
    found = False
    for line in data:
        try:
            bint = int(line, 2) # binary int
            bnumber = bint.bit_length() + 7 // 8
            barry = bint.to_bytes(bnumber, "big")
            text = barry.decode()

            if flag_format in text:
                print(f"{Fore.RED}{line} -> {text}{Fore.RESET}")
                found = True
        except ValueError as e:
            # print(e)
            pass
    return found


if __name__ == '__main__':
    args = parse_arguments()
    if args.debug:
        file_name = 'image.png'
        flag_format = 'TUCTF'
    else:
        file_name = args.file_name
        flag_format = args.flag_format

    strings_output = popen(f'strings "{file_name}"').read()
    lines = strings_output.split('\n')

    print(f'{Fore.GREEN}no plain-text flag found{Fore.RESET}') if not check_plain_flag(lines[:]) else None
    print(f'{Fore.GREEN}no base16 (hexadecimal) flag found{Fore.RESET}') if not check_base16_flag(lines[:]) else None
    print(f'{Fore.GREEN}no base32 flag found{Fore.RESET}') if not check_base32_flag(lines[:]) else None
    print(f'{Fore.GREEN}no base64 flag found{Fore.RESET}') if not check_base64_flag(lines[:]) else None
    print(f'{Fore.GREEN}no base85 flag found{Fore.RESET}') if not check_base85_flag(lines[:]) else None
    print(f'{Fore.GREEN}no binary flag found{Fore.RESET}') if not check_binary_flag(lines[:]) else None
