#!/usr/bin/env python3

##### global imports #####
from os import popen, path, mkdir, listdir
from re import findall
from threading import Thread
from requests import get
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

##### local imports ####
from flagger.modules import utils
from flagger.encoding.encoding_checker import EncodingChecker
from flagger.modules.binwalker import BinWalker


class Flagger(EncodingChecker):
    online = utils.online()  # check if online
    flag_format: str  # flag format for all instances
    verbose: bool  # unified verbose for all instances
    silent: bool  # unified silent for all instances

    def __init__(self, filename, no_rot, walk=True):
        super().__init__()
        valid_files = []
        if path.exists(filename):
            if path.isdir(filename):  # get all the valid files in the directory
                valid_files = utils.get_valid_files(filename)
                for file in valid_files:
                    Process(target=Flagger, args=(file, no_rot)).start()
                return None  # don't fetch flags for the directory itself
            elif walk:
                walker = BinWalker(filename)
                if walker.extracted:
                    files = listdir(walker.extract_dir)
                    with ProcessPoolExecutor() as executor:
                        executor.map(Flagger, [f'{walker.extract_dir}/{extracted_file}' for extracted_file in files],
                                     [False] * len(files), [False] * len(files))
                    # for extracted_file in files:
                    #     Process(target=Flagger, args=(f'{walker.extract_dir}/{extracted_file}', False, False)).start()

        else:
            print('File Not Found :(')
            exit(0)

        self.file_name = filename
        self.no_rot = no_rot

        self.strings_output = popen(
            f'strings "{self.file_name}" | sort -u ').read()  # didn't use readlines() to remove \n in the following line
        self.strings_lines = self.strings_output.split('\n')

        # del self.strings_output
        self.__fetch()

    @staticmethod
    def echo(encoding, encoded_flag, decoded_flag):
        """
        Print colored encoded and decoded flag
        """
        if Flagger.silent:
            print(
                f"{utils.COLORS['FLAG']}{decoded_flag}{utils.COLORS['RESET']}")
        else:
            print(
                f"[{encoding}] {utils.COLORS['ENC_FLAG']}{encoded_flag} -> {utils.COLORS['FLAG']}{decoded_flag}{utils.COLORS['RESET']}")

    @staticmethod
    def rotator(data, key):
        rotated_lines = []
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
            rotated_lines.append(''.join(deciphered))
        return rotated_lines

    def rotate(self, key):
        #  rotate and check after rotation
        with open(f'{self.file_name}_rotates/rot{key}', 'w') as saving_file:
            saving_file.writelines(f'{line}\n' for line in Flagger.rotator(self.strings_lines[:], key))
            # ? saving_file.writelines(f'{line}\n' for line in rotated_lines, key))

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
            try:
                for encoding, encoded, decoded in check(self.strings_output, Flagger.flag_format):
                    Flagger.echo(encoding, encoded, decoded)
            except ValueError as e:
                print(f'Error in {check.__name__}: {e}')

    def check_all_rotations(self):
        if not self.no_rot:
            if not path.exists(f'{self.file_name}_rotates'):
                mkdir(f'{self.file_name}_rotates')
            with ThreadPoolExecutor() as executor:
                executor.map(self.rotate, range(1, 26))
            # for key in range(1, 26):
            #     Thread(target=self.rotate, args=(key,)).start()

            with ProcessPoolExecutor() as executor:
                executor.map(self.rotate, range(1, 26))
            # Process(target=Flagger, args=(f'{self.file_name}_rotates/', True)).start()  # don't rotate, avoid infinite loop

    def check_all_shifts(self):
        with ThreadPoolExecutor() as executor:
            executor.map(self.shift, [self.strings_lines[:]] * 24, range(2, 26))

        # for shifts in range(2, 26):
        #     Thread(target=self.shift, args=[self.strings_lines[:], shifts]).start() if not self.no_rot else None

    def check_all_hashes(self):
        if Flagger.online:
            for line in self.strings_lines[:]:
                Thread(target=self.crack_md5, args=[line]).start()

    def __fetch(self):
        print(f'{"_" * 10} searching in {self.file_name} {"_" * 10}')
        self.check_all_bases()

        # self.check_all_rotations()
        #
        # self.check_all_shifts()
        #
        # self.check_all_hashes()

