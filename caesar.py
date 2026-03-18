def caesar_cipher(text, k, mode):
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    for char in text:
        if char in uppercase:
            position = uppercase.index(char)
            if mode == "e":
                new_position = (position + k) % 26
            else:  
                new_position = (position - k) % 26
            result += uppercase[new_position]

        elif char in lowercase:
            position = lowercase.index(char)
            if mode == "e":
                new_position = (position + k) % 26
            else: 
                new_position = (position - k) % 26
            result += lowercase[new_position]

        else:
            result += char 

    return result
text = input("Enter text: ")
k = int(input("Enter key: "))
choice = input("Enter 'e' for encryption or 'd' for decryption: ")

output = caesar_cipher(text, k, choice)
print("Result:", output)
