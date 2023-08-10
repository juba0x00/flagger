#!/usr/bin/env python3
#  global imports
from os import popen, path, mkdir, listdir, walk
from colorama import Fore
from base64 import b16encode, b16decode, b32encode, b32decode, b64encode, b64decode, b85encode, b85decode
from base45 import b45encode, b45decode
from re import findall
from threading import Thread
from requests import get
#  local imports
from modules import oct
from modules import utils
from modules.binwalker import BinWalker


class Flagger:
    encoded_color = Fore.BLUE
    flag_color = Fore.GREEN
    online = utils.online()
    flag_format: str
    verbose: bool
    silent: bool

    def __init__(self, filename, no_rot):
        self.file_name = filename
        self.no_rot = no_rot
        self.check_functions = [
            self.__check_plain_flag,
            self.__check_binary_flag,
            self.__check_base8_flag,
            self.__check_base16_flag,
            self.__check_base32_flag,
            self.__check_base45_flag,
            self.__check_base64_flag,
            self.__check_base85_flag
        ]
        self.strings_output = popen(
            f'strings "{self.file_name}" | sort | uniq').read()  # didn't use readlines() to remove \n in the following line
        self.strings_lines = self.strings_output.split('\n')
        del self.strings_output

    @staticmethod
    def echo(encoding, encoded_flag, decoded_flag):
        """
        Print colored encoded and decoded flag
        """
        if Flagger.silent:
            print(
                f"{Flagger.flag_color}{decoded_flag}{Fore.RESET}")
        else:
            print(
                f"[{encoding}] {Flagger.encoded_color}{encoded_flag} -> {Flagger.flag_color}{decoded_flag}{Fore.RESET}")

    @staticmethod
    def __check_plain_flag(data):
        for line in data:
            if Flagger.flag_format.lower() in line.lower():
                Flagger.echo('plain', '', line)

    @staticmethod
    def __check_binary_flag(data):
        for line in data:
            try:
                bint = int(line, 2)  # binary int
                bnumber = bint.bit_length() + 7 // 8
                barry = bint.to_bytes(bnumber, "big")
                text = barry.decode()

                if Flagger.flag_format.lower() in text.lower():
                    Flagger.echo('binary', line, text)
            except Exception as e:
                pass

    @staticmethod
    def __check_base8_flag(data):
        base8_flag = oct.oct_encode(Flagger.flag_format)
        for line in data:
            matches = findall(r'\b0[0-7]+', line)
            for match in matches:
                if base8_flag in match:
                    Flagger.echo('octal', line, match.oct_decode(line))

    @staticmethod
    def __check_base16_flag(data):
        base16_flag = b16encode(Flagger.flag_format.encode('ascii')).decode('ascii')
        for line in data:
            matches = findall(r'\b[0-9A-Fa-f]+', line)
            for match in matches:
                if base16_flag.lower() in match.lower():
                    Flagger.echo('hexadecimal', encoded_flag=line,
                                   decoded_flag=b16decode(match.upper()).decode('ascii').replace('\n', ''))
                    #  .upper() to avoid hexdecimal decoding errors (ABC..., instead of abc..ABC..., instead of abc....)

    @staticmethod
    def __check_base32_flag(data):
        base32_flag = b32encode(Flagger.flag_format.encode('ascii')).decode('ascii').replace('=', '')
        base32_flag = base32_flag[:len(base32_flag) - 1]  # to avoid the last digit unmatching
        for line in data:
            matches = findall(r'\b[A-Z2-7]+=*', line)
            for match in matches:
                if base32_flag in match:
                    Flagger.echo('base32', line, b32decode(match.encode('ascii')).decode('ascii'))

    @staticmethod
    def __check_base45_flag(data):
        base45_flag = b45encode(Flagger.flag_format.encode('ascii')).decode('ascii').replace('=', '')
        base45_flag = base45_flag[:len(base45_flag) - 2]  # to avoid the last digit unmatching
        for line in data:
            matches = findall(r'\b[A-Z0-9 $%*+\-.\/:]+', line)
            for match in matches:
                if base45_flag in match:
                    Flagger.echo('base45', line, b45decode(match.encode('ascii')).decode('ascii'))

    @staticmethod
    def __check_base64_flag(data):
        base64_flag = b64encode(Flagger.flag_format.encode('ascii')).decode('ascii').replace('=', '')

        base64_flag = base64_flag[:len(base64_flag) - 1]  # to avoid the last digit unmatchinglf.__check_base16_flag,
        for line in data:
            matches = findall(r'\b[A-Za-z0-9+/]{4,}(?:==?|=\n)?', line)
            for match in matches:
                if base64_flag in match:
                    Flagger.echo('base64', line, b64decode(match.encode('ascii')).decode('ascii'))

    @staticmethod
    def __check_base85_flag(data):
        base85_flag = b85encode(Flagger.flag_format.encode('ascii')).decode('ascii').replace('=', '')
        base85_flag = base85_flag[:len(base85_flag) - 1]  # to avoid the last digit unmatching
        for line in data:
            matches = findall(r'\b[!-u]+', line)
            for match in matches:
                if base85_flag in match:
                    Flagger.echo('base85', match, b85decode(line.encode('ascii')).decode('ascii'))

    def rotator(self, data, key):
        for line in data:
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't',
                        'u', 'v', 'w', 'x', 'y', 'z']
            shifted_alphabet = [''] * len(alphabet)

            # Fill shifted_alphabet
            for i in range(len(alphabet)):
                shifted_alphabet[i] = alphabet[(i + key) % len(alphabet)]

            # Substitution
            deciphered = [''] * len(line)
            exists = False

            for i in range(len(line)):
                for j in range(len(shifted_alphabet)):
                    if line[i].casefold() == alphabet[j].casefold():
                        deciphered[i] = shifted_alphabet[j]
                        exists = True
                        break
                    else:
                        exists = False

                if not exists:
                    deciphered[i] = line[i]

            # Put the result in a string
            rotated = ''.join(deciphered)
            with open(f'{self.file_name}_rotates/rot{key}', 'w') as saving_file:
                if Flagger.flag_format.lower() in rotated:
                    Flagger.echo('rot', f"ROT{key}", rotated)
                else:
                    saving_file.write(f'{rotated}\n')

    def rotate(self):
        if not path.exists(f'{self.file_name}_rotates'):
            mkdir(f'{self.file_name}_rotates')

        #  rotate and check after rotation
        for rot in range(1, 26):
            self.rotator(self.strings_lines[:], rot)


    @staticmethod
    def shift(text, shifts):
        shifted_back = ""
        shifted_forward = ""
        for line in text:
            if line == "":
                #  skip empty lines
                continue
            for char in line:
                try:  # avoid out of range code
                    shifted_back += chr(ord(char) - shifts)
                    shifted_forward += chr(ord(char) + shifts)


                except Exception as e:
                    pass

            if Flagger.flag_format in shifted_back:
                Flagger.echo(f'shift{shifts}', line, shifted_back)

            elif Flagger.flag_format in shifted_forward:
                Flagger.echo(f'shift{shifts}', line, shifted_forward)
            shifted_back = ""
            shifted_forward = ""

    @staticmethod
    def crack_md5(line):
        if hashes := findall(r"([a-fA-F\d]{32})", line):  # extract MD5 hashes from the line
            for hash in hashes:
                try:
                    print(f'{hash} -> md5 hash detected') if Flagger.verbose else None
                    result = get(f"https://www.nitrxgen.net/md5db/{hash}").text
                    Flagger.echo('md5', hash, result) if result != '' else None

                except Exception as e:
                    pass

    def check_all_bases(self):
        for check in self.check_functions:
            Thread(target=check, args=[self.strings_lines[:]]).start()

    def check_all_rotations(self):
        if not self.no_rot:
            self.rotate()
            for file in listdir(f'{self.file_name}_rotates/'):
                flag_fetcher = Flagger(filename=f'{self.file_name}_rotates/{file}', no_rot=True)  # don't rotate
                flag_fetcher.fetch()

    def check_all_shifts(self):
        for shifts in range(2, 26):
            Thread(target=self.shift, args=[self.strings_lines[:], shifts]).start() if not self.no_rot else None

    def check_all_hashes(self):
        if Flagger.online:
            for line in self.strings_lines[:]:
                Thread(target=self.crack_md5, args=[line]).start()

    def fetch(self):
        print(f'{"_" * 10} searching in {self.file_name} {"_" * 10}')
        self.check_all_bases()

        self.check_all_rotations()

        self.check_all_shifts()

        self.check_all_hashes()


def main():
    args = utils.parse_arguments()
    valid_files = []
    if path.exists(args.file_name):
        if path.isdir(args.file_name):  # get all the valid files in the directory
            for root, dirs, files in walk(args.file_name):
                for file in files:
                    valid_files.append(path.join(root, file))
        else:  # only this file
            valid_files.append(args.file_name)
    else:
        print('File Not Found :(')
        exit(0)
    Flagger.flag_format = args.flag_format  # set the flag format for the class (all the instances)
    # I added the previous line here to be executed at the first instance only
    # , if it's in the constructor it will be executed in each instance creation
    Flagger.verbose = args.verbose
    Flagger.silent = args.silent

    for file in valid_files:  # iterate over all the valid files and fetch the flag
        flag_fetcher = Flagger(filename=file, no_rot=args.no_rot)
        flag_fetcher.fetch()
        walker = BinWalker(flag_fetcher.file_name)
        if walker.extracted:
            files = listdir(f'{flag_fetcher.file_name}.extracted')
            for extracted_file in files:
                child_flag_fetcher = Flagger(filename=f'{flag_fetcher.file_name}.extracted/{extracted_file}',
                                               no_rot=False)
                child_flag_fetcher.fetch()


if __name__ == '__main__':
    main()
