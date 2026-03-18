def encrypt(message, key):
    ciphertext = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(message):
            ciphertext[col] += message[pointer]
            pointer += key
    return ''.join(ciphertext)

def decrypt(message, key):
    import math
    num_cols = math.ceil(len(message) / key)
    num_rows = key
    num_shaded_boxes = (num_cols * num_rows) - len(message)
    plaintext = [''] * num_cols
    col = 0
    row = 0
    for symbol in message:
        plaintext[col] += symbol
        col += 1
        if (col == num_cols) or (col == num_cols - 1 and row >= num_rows - num_shaded_boxes):
            col = 0
            row += 1
    return ''.join(plaintext)

msg = input("Enter message: ")
k = int(input("Enter key (number): "))
choice = input("Encrypt or Decrypt (E/D): ").upper()

if choice == 'E':
    print("Result:", encrypt(msg, k))
elif choice == 'D':
    print("Result:", decrypt(msg, k))
else:
    print("Invalid Choice")
