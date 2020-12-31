import base64

from hashlib import md5
from Cryptodome.Cipher import AES

BLOCK_SIZE = 16

"""
Code used to replicate CryptoJS decryption
"""


def unpad(ciphertext: bytes) -> bytes:
    return ciphertext[
        : -(ciphertext[-1] if type(ciphertext[-1]) == int else ord(ciphertext[-1]))
    ]


def bytes_to_aes_key(data: bytes, salt: bytes, output=48) -> bytes:
    assert len(salt) == 8, len(salt)

    data += salt
    key = md5(data).digest()
    final_key = key

    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key

    return final_key[:output]


def decrypt(encrypted: bytes, passphrase: bytes) -> bytes:
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"

    salt = encrypted[8:16]
    key_iv = bytes_to_aes_key(passphrase, salt, 32 + 16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)

    return unpad(aes.decrypt(encrypted[16:]))
