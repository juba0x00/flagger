# Flagger
Search any flag format in `strings` output

![demo](./demo.png)

## Todo List 

- [x] Search for the plain-text flag 
- [ ] Search for the bases of the flag (base64, 42, ...)
  - [x] base64 
  - [x] base45
  - [x] base16 (hex)
  - [ ] base8 (octal)
  - [x] base2 (binary)
  - [x] base32
  - [x] base85
- [x] Search for the ROT13 of the flag (ROT1, ROT2, ... ROT26)
- [x] fix not found flags (merged between text)
  - ![fix](fix.png)
  
  
  ## Notes

- [ ] Rotator function doesn't have to create a folder, instead it can do all the possible rotates (1-25) then check for the flag format that was entered (ex: -f TUCTF), and then output the flag if found.
- [ ] We shall check for all bases (2, 8, 16, 32, 42, 45, 58, 62, 64, 85).
- [ ] Double decoding could be implemented lately.
