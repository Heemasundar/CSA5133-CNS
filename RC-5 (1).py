def rotate_left(x, y):
    return ((x << y) & 0xffffffff) | (x >> (32 - y))

def rotate_right(x, y):
    return (x >> y) | ((x << (32 - y)) & 0xffffffff)

def rc5_encrypt(A, B, key, rounds=6):
    for i in range(rounds):
        A = rotate_left(A ^ B, B % 32) + key
        B = rotate_left(B ^ A, A % 32) + key
    return A, B

def rc5_decrypt(A, B, key, rounds=6):
    for i in range(rounds):
        B = rotate_right(B - key, A % 32) ^ A
        A = rotate_right(A - key, B % 32) ^ B
    return A, B


# Sample Input
A = 123
B = 456
key = 10

cipher = rc5_encrypt(A, B, key)
print("Cipher:", cipher)

plain = rc5_decrypt(cipher[0], cipher[1], key)
print("Decrypted:", plain)
