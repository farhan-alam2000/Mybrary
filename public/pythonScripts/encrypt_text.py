import pandas as pd
import numpy as np
import time
import string
from nltk.corpus import stopwords
import csv
import sys
import PyPDF2
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import math
from fuzzygeneration import addFuzzy
# from cryptography.fernet import Fernet
from Cryptodome.Cipher import AES
from Cryptodome.Hash import MD5
from Cryptodome.Random import random
from Cryptodome.Random import get_random_bytes
import pyaes, pbkdf2, binascii, os, secrets

def encrypt_doc(text, MK):
    # MK="hello"
    MK = MK.encode('utf-8')
    MK_length = len(MK)
    if MK_length>16:
        MK = MK[:16]
    if MK_length < 16:
        MK += bytes(16 - MK_length)
    iv = 112915530833849023049749033005636095837785094513880771218920184288349877773586
    # iv = secrets.randbits(256)
    # plaintext = "Secret Data"
    aes = pyaes.AESModeOfOperationCTR(MK, pyaes.Counter(iv))
    ciphertext = aes.encrypt(text)
    return ciphertext.hex()
    # print('Encrypted Text:', binascii.hexlify(ciphertext))

cleaned_doc = sys.argv[1]
password = sys.argv[2]
encrypted_stuff = encrypt_doc(cleaned_doc, password)
print(encrypted_stuff)