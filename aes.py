from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib
import os

def aes_encrypt(msg):
    # Generate a random 256-bit (32-byte) key
    key = os.urandom(32)
    BLOCK_SIZE = 16
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    private_key = hashlib.sha256(key).digest()
    msg = pad(msg)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    encrypted = base64.b64encode(iv + cipher.encrypt(msg))
    return encrypted

def aes_decrypt(ciphertext, key):
    # Use the provided key for decryption
    private_key = hashlib.sha256(key).digest()
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext[16:]))
    return decrypted.decode()
