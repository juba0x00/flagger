def oct_encode(plain: str) -> str:
    return ''.join([oct(ord(char))[2:] for char in plain])


def oct_decode(word: str) -> str:
    #oct to ascii 
    oct_to_ascii = []
    for i in range(0, len(word), 3): oct_to_ascii.append(str(int(word[i:i+3],8)))

    #ascii to string
    ascii_to_str = ''
    for i in oct_to_ascii: ascii_to_str += chr(int(i))

    return ascii_to_str