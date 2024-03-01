#!/usr/bin/env python3
# global imports
from os import popen, path, mkdir, listdir
from base64 import b16encode, b16decode, b32encode, b32decode, b64encode, b64decode, b85encode, b85decode
from base45 import b45encode, b45decode
from re import findall
from threading import Thread
from requests import get
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# local imports
from modules import oct
from modules import utils
from modules.binwalker import BinWalker
import modules.banner


class Flagger:
    online = utils.online() # check if online
    flag_format: str # flag format for all instances
    verbose: bool # verbose for all instances
    silent: bool # silent for all instances
    processes: int # number of processes for all instances
    threads: int # number of threads for all instances

    def __init__(self, filename, no_rot, walk=False):
        valid_files = []
        if path.exists(filename):
            if path.isdir(filename):  # get all the valid files in the directory
                valid_files = utils.get_valid_files(filename)
                for file in valid_files:
                    Process(target=Flagger, args=(file, no_rot)).start()
                return None # don't fetch flags for the directory itself
            elif walk:
                    walker = BinWalker(filename)
                    if walker.extracted:
                        files = listdir(walker.extract_dir)
                        # with ProcessPoolExecutor(max_workers=Flagger.processes) as executor:
                            # executor.map(Flagger, [f'{walker.extract_dir}/{extracted_file}' for extracted_file in files], [False] * len(files), [False] * len(files))
                        for extracted_file in files:
                            Process(target=Flagger, args=(f'{walker.extract_dir}/{extracted_file}', False, False)).start()

        else:
            print('File Not Found :(')
            exit(0)
        
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
            f'strings "{self.file_name}" | sort -u ').read()  # didn't use readlines() to remove \n in the following line
        self.strings_lines = self.strings_output.split('\n')
        del self.strings_output
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
        base64_flag = base64_flag[:len(base64_flag) - 1]  # to avoid the last digit unmatching
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
            #? saving_file.writelines(f'{line}\n' for line in rotated_lines, key))
    
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
        # with ThreadPoolExecutor(max_workers=Flagger.threads) as executor:
            # executor.map(self.check_functions, [self.strings_lines[:]] * len(self.check_functions))
        for check in self.check_functions:
            # print(f'checking {check}')
            with ThreadPoolExecutor(max_workers=Flagger.threads) as executor:
                executor.submit(check, self.strings_lines[:])
            
            # Thread(target=check, args=[self.strings_lines[:]]).start()

    def check_all_rotations(self):
        if not self.no_rot:
            if not path.exists(f'{self.file_name}_rotates'):
                mkdir(f'{self.file_name}_rotates')

            for key in range(1, 26):
                with ThreadPoolExecutor(max_workers=Flagger.threads) as executor:
                    executor.submit(self.rotate, key)
                # Thread(target=self.rotate, args=(key,)).start()

            # with ProcessPoolExecutor(Flagger.processes) as executor:
                # executor.submit(Flagger, f'{self.file_name}_rotates/', True)
            Process(target=Flagger, args=(f'{self.file_name}_rotates/', True)).start()  # don't rotate, avoid infinite loop

    def check_all_shifts(self):

        with ThreadPoolExecutor(max_workers=Flagger.threads) as executor:
            # executor.map(self.shift, [self.strings_lines[:]] * 24, range(2, 26))
            for shifts in range(2, 26):
                executor.submit(self.shift, self.strings_lines[:], shifts)
        #     Thread(target=self.shift, args=[self.strings_lines[:], shifts]).start() if not self.no_rot else None
            
    def check_all_hashes(self):
        if Flagger.online:
            with ThreadPoolExecutor(max_workers=Flagger.threads) as executor:
                executor.map(self.crack_md5, self.strings_lines[:])
            # for line in self.strings_lines[:]:
                # Thread(target=self.crack_md5, args=[line]).start()

    def __fetch(self):
        # print(f'{"_" * 10} searching in {self.file_name} {"_" * 10}')
        self.check_all_bases()
        
        self.check_all_rotations()
        
        self.check_all_shifts()
        
        self.check_all_hashes()


def main():
    args = utils.parse_arguments()
    Flagger.flag_format = args.flag_format  # set the flag format for the class (all the instances)
    # I added the previous line here to be executed at the first instance only
    # , if it's in the constructor it will be executed in each instance initiation
    Flagger.verbose = args.verbose
    Flagger.silent = args.silent
    Flagger.processes = args.processes
    Flagger.threads = args.threads

    
    with ProcessPoolExecutor(max_workers=Flagger.processes) as executor:
        executor.submit(Flagger, args.file_name, args.no_rot, walk=True)
        
    # Process(target=Flagger, args=(args.file_name, args.no_rot)).start()  # create an instance of the class


if __name__ == '__main__':
    main()
