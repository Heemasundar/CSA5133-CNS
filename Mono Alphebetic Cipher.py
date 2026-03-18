import string
def monoalphabetic_cipher():
    alphabet = string.ascii_uppercase
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    encrypt_map = dict(zip(alphabet, key))
    decrypt_map = dict(zip(key, alphabet))
    
    def encrypt(plaintext):
        return ''.join(encrypt_map.get(char, char) for char in plaintext.upper())

    def decrypt(ciphertext):
        return ''.join(decrypt_map.get(char, char) for char in ciphertext.upper())
    msg = "HELLO WORLD"
    encrypted = encrypt(msg)
    decrypted = decrypt(encrypted)
    
    print(f"Original: {msg}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
    monoalphabetic_cipher()
