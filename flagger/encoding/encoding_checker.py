from re import findall, escape
from time import perf_counter
from base64 import b16encode, b16decode, b32encode, b32decode, b64encode, b64decode, a85encode, a85decode
from base45 import b45encode, b45decode
MAX_LEN = 300

from flagger.encoding import oct

class EncodingChecker:
    def __init__(self):
        self.check_functions = [
            self.check_plain_flag,
            self.check_binary_flag,
            self.check_base8_flag,
            self.check_base16_flag,
            self.check_base32_flag,
            self.check_base45_flag,
            self.check_base64_flag,
            self.check_base85_flag
        ]

    @staticmethod
    def check_plain_flag(data: str, flag: str):
        matches = findall(rf"{escape(flag)}.{{0,{MAX_LEN}}}", data)
        for match in matches:
            yield 'plain', match, match

    @staticmethod
    def check_binary_flag(data: str, flag: str):
        binary_flag = bin(int.from_bytes(flag.encode('ascii'), 'big'))[2:]
        matches = findall(rf"{escape(binary_flag)}.{{0,{MAX_LEN}}}", data)
        for match in matches:
            decoded_match = int(match, 2).to_bytes((len(match) + 7) // 8, 'big').decode('utf-8')
            yield 'binary', match, decoded_match

    @staticmethod
    def check_base8_flag(data: str, flag: str):
        base8_flag = oct.oct_encode(flag)
        matches = findall(r'\b0[0-7]+', data)
        for match in matches:
            if base8_flag in match:
                yield 'octal', match, oct.oct_decode(match)

    @staticmethod
    def check_base16_flag(data: str, flag: str):
        base16_flag = b16encode(flag.encode('ascii')).decode('ascii')
        matches = findall(rf"{escape(base16_flag)}.{{0,{MAX_LEN}}}", data)
        for match in matches:
                yield 'hexadecimal', match, b16decode(match.upper()).decode('ascii').replace('\n', '')

    @staticmethod
    def check_base32_flag(data: str, flag: str):
        base32_flag = b32encode(flag.encode('ascii')).decode('ascii').replace('=', '')
        base32_flag = base32_flag[:len(base32_flag) - 1]  # to avoid the last digit unmatching
        matches = findall(rf"{escape(base32_flag)}.{{0,{MAX_LEN}}}", data)
        for match in matches:
            yield 'base32', match, b32decode(match.encode('ascii')).decode('ascii')

    @staticmethod
    def check_base45_flag(data: str, flag: str):
        base45_flag = b45encode(flag.encode('ascii')).decode('ascii').replace('=', '')
        base45_flag = base45_flag[:len(base45_flag) - 2]  # to avoid the last digit unmatching

        matches = findall(rf"{escape(base45_flag)}.{{0,{MAX_LEN}}}", data)
        for match in matches:
            yield 'base45', match, b45decode(match.encode('ascii')).decode('ascii')

    @staticmethod
    def check_base64_flag(data: str, flag: str):
        base64_flag = b64encode(flag.encode('ascii')).decode('ascii').replace('=', '')
        base64_flag = base64_flag[:len(base64_flag) - 1]  # to avoid the last digit unmatching
        matches = findall(rf"{escape(base64_flag)}.{{0,{MAX_LEN}}}", data)
        for match in matches:
            yield 'base64', match, b64decode(match.encode('ascii')).decode('ascii')

    @staticmethod
    def check_base85_flag(data: str, flag: str):
        base85_flag = a85encode(flag.encode('ascii')).decode('ascii')
        base85_flag = base85_flag[:len(base85_flag) - 1]  # to avoid the last digit unmatching
        matches = findall(rf"{escape(base85_flag)}.{{0,{MAX_LEN}}}", data)
        for match in matches:
            yield 'base85', match, a85decode(match.encode('ascii')).decode('ascii')
