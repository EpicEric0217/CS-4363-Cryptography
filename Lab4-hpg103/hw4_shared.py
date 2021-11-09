# Chat Encryption Helper - ch9_crypto_chat.py
import os, base64, json
# from Crypto.Cipher import PKCS1_OAEP, AES
# from Crypto.PublicKey import RSA, ECC
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode


# encryption method used by all calls
def encrypt(message, usePKI, useDH, dhSecret):
    em = customEncrypt(message, dhSecret, 1)
    return em


# decryption method used by all calls
def decrypt(message, usePKI, useDH, dhSecret):
    dm = customEncrypt(message, dhSecret, -1)
    return dm


# decrypt using RSA (for future reference, not needed for this homework)
# def decrypt_rsa(ciphertext):
#    return ciphertext

# encrypt using RSA (for future reference, not needed for this homework)
# def encrypt_rsa(message):
#    return message

# check client commands (for future reference, not needed for this homework)
def check_client_command(data):
    return 1


# check server commands (for future reference, not needed for this homework)
def check_server_command(data):
    return 1


def reversed_string(a_string):
    return a_string[::-1]


def customEncrypt(inputText, N, D):
    encryptedText = ""
    inputText = inputText[::-1]
    for words in inputText:
        if D == +1:
            if words.isupper():
                pos_u = ord(words) - ord("A")
                val = ((pos_u + N) % 26) + int(ord("A"))
                wordsnew = chr(val)
            elif words.islower():
                pos_1 = ord(words) - ord("a")
                val = ((pos_1 + N) % 26) + ord("a")
                wordsnew = chr(val)
            elif words.isdigit():
                val = (int(words) - N) % 10
                wordsnew = str(val)

        elif D == -1:
            if words.isupper():
                pos_u = ord(words) - ord("A")
                val = ((pos_u - N) % 26) + ord("A")
                wordsnew = chr(val)
            elif words.islower():
                pos_1 = ord(words) - ord("a")
                val = ((pos_1 - N) % 26) + ord("a")
                wordsnew = chr(val)
            elif words.isdigit():
                val = (int(words) + N) % 10
                wordsnew = str(val)
        encryptedText += wordsnew
    return (encryptedText)
