import pgpy
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryt, 2048)

uid = pgpy.PGPUID.new('Alice', email='alice@example.com')
key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256],
            ciphers=[SymmetricKeyAlgorithm.AES256],
            compression=[CompressionAlgorithm.ZLIB])

pub_key = key.pubkey

message_text = "This is a highly secret PGP message."
message = pgpy.PGPMessage.new(message_text)

encrypted_message = pub_key.encrypt(message)
print(f"--- Encrypted Message ---\n{str(encrypted_message)}\n")

decrypted_message = key.decrypt(encrypted_message).message
print(f"--- Decrypted Content ---\n{decrypted_message}")
