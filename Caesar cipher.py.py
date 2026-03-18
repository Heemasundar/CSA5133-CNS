def caesar_cipher(text, k, mode):
    shift = k if mode == 'e' else -k
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

text = input("Enter text: ")
k = int(input("Enter key: "))
choice = input("Enter 'e' for encryption or 'd' for decryption: ")
print("Result:", caesar_cipher(text, k, choice))