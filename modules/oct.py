#!/usr/bin/env python3

'''
OCTAL ENCODER/DECODER

encode: str --> ascii --> oct
decode: oct --> ascii --> str

example1: '124125103124106' <--> 'TUCTF'
example2: '124125103124106173164150151163137151163137157143164141154175' <--> TUCTF{this_is_octal}
'''

#---- ENCODE ----#
def oct_encode(word):
    return ''.join([oct(ord(char))[2:] for char in plain])

#---- DECODE ----# 
def oct_decode(word):
    #oct to ascii 
    oct_to_ascii = []
    for i in range(0, len(word), 3): oct_to_ascii.append(str(int(word[i:i+3],8)))

    #ascii to string
    ascii_to_str = ''
    for i in oct_to_ascii: ascii_to_str += chr(int(i))

    return ascii_to_str

# --- TEST --- #
#print(oct_encode('TUCTF'))
#print(oct_decode('124125103124106173164150151163137151163137157143164141154175'))
