import numpy as np

def mod_inv(a):
    a = a % 26
    for i in range(26):
        if (a * i) % 26 == 1:
            return i
    return -1

def get_key():
    print("Enter 9 values for 3x3 key matrix (row-wise):")
    values = list(map(int, input().split()))
    if len(values) != 9:
        print("Enter exactly 9 numbers")
        exit()
    key = np.array(values).reshape(3,3)
    return key

def encrypt(msg, key):
    msg = msg.upper().replace(" ", "")
    
    while len(msg) % 3 != 0:
        msg += "X"
        
    result = ""
    
    for i in range(0, len(msg), 3):
        block = [ord(msg[i]) - 65,
                 ord(msg[i+1]) - 65,
                 ord(msg[i+2]) - 65]
        
        res = np.dot(key, block) % 26
        
        for num in res:
            result += chr(int(num) + 65)
            
    return result

def decrypt(cipher, key):
    det = int(round(np.linalg.det(key))) % 26
    inv_det = mod_inv(det)

    if inv_det == -1:
        return "Key not invertible"

    cof = np.zeros((3,3))

    for r in range(3):
        for c in range(3):
            minor = np.delete(np.delete(key, r, axis=0), c, axis=1)
            cof[r][c] = ((-1)**(r+c)) * int(round(np.linalg.det(minor)))

    adj = cof.T
    inv_key = (inv_det * adj) % 26

    result = ""

    for i in range(0, len(cipher), 3):
        block = [ord(cipher[i]) - 65,
                 ord(cipher[i+1]) - 65,
                 ord(cipher[i+2]) - 65]

        res = np.dot(inv_key, block) % 26

        for num in res:
            result += chr(int(num) + 65)

    return result

key = get_key()
msg = input("Enter Message: ")

cipher = encrypt(msg, key)
print("Encrypted:", cipher)

plain = decrypt(cipher, key)
print("Decrypted:", plain)
