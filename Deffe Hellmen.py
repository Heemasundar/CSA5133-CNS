
p = int(input("Enter prime number (p): "))
g = int(input("Enter primitive root (g): "))

a = int(input("Enter private key of User A: "))
b = int(input("Enter private key of User B: "))

A = (g ** a) % p
B = (g ** b) % p

print("\nPublic Key of User A:", A)
print("Public Key of User B:", B)

key_A = (B ** a) % p
key_B = (A ** b) % p

print("\nSecret Key calculated by User A:", key_A)
print("Secret Key calculated by User B:", key_B)

if key_A == key_B:
    print("\nKey Exchange Successful! Shared Secret Key is:", key_A)
else:
    print("\nKey Exchange Failed!")