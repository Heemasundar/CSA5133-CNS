import string

def vigenere_cipher():
    alphabet = string.ascii_uppercase
    
    mode = input("Mode (e to encrypt, d to decrypt): ").lower()
    text = input("Message: ").upper()
    key = input("Key: ").upper()
    
    result = []
    key_index = 0
    
    for char in text:
        if char in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            if mode == 'd':
                shift = -shift
                
            new_pos = (alphabet.index(char) + shift) % 26
            result.append(alphabet[new_pos])
            key_index += 1
        else:
            result.append(char)
            
    print("Result:", "".join(result))

vigenere_cipher()
