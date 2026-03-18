def xor(a, b):
    return ''.join('0' if i == j else '1' for i, j in zip(a, b))

def split_block(block):
    mid = len(block) // 2
    return block[:mid], block[mid:]

def simple_round(left, right, key):
    new_right = xor(left, xor(right, key))
    return right, new_right

def simple_des_encrypt(plaintext, key, rounds=4):
    left, right = split_block(plaintext)

    for i in range(rounds):
        left, right = simple_round(left, right, key)

    return left + right

def simple_des_decrypt(ciphertext, key, rounds=4):
    left, right = split_block(ciphertext)

    for i in range(rounds):
        left, right = simple_round(left, right, key)

    return left + right


plaintext = "1010101010101010"
key = "11110000"

cipher = simple_des_encrypt(plaintext, key)
print("Ciphertext:", cipher)

plain = simple_des_decrypt(cipher, key)
print("Decrypted:", plain)
