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

def encrypt_doc(text, MK):
    keyword_index = MD5.new()
    keyword_index.update(str(text).encode('utf-8'))
    MK = MK.encode('utf-8')
    MK_length = len(MK)
    if MK_length < 16:
        MK += bytes(16 - MK_length)
    ECB_cipher = AES.new(MK, AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())

cleaned_doc = sys.argv[1]
password = sys.argv[2]
encrypted_stuff = encrypt_doc(cleaned_doc, password)
print(encrypted_stuff)