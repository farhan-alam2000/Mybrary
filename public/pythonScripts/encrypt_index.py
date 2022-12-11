import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Hash import MD5
from Cryptodome.Random import random
import numpy as np
import time
import hashlib
from PyPDF2 import PdfFileWriter, PdfFileReader
import sys
import json
import ast

def build_trapdoor(MK, keyword):
    keyword_index = MD5.new()
    keyword_index.update(str(keyword).encode('utf-8'))
    MK = MK.encode('utf-8')
    MK_length = len(MK)
    if MK_length < 16:
        MK += bytes(16 - MK_length)
    ECB_cipher = AES.new(MK, AES.MODE_ECB)
    # ECB_cipher = AES.new(key, AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())

def build_codeword(ID, trapdoor):
    ID_index = MD5.new()
    ID_index.update(str(ID).encode('utf-8'))
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    # print(ECB_cipher)
    return ECB_cipher.encrypt(ID_index.digest())

def build_index(master_key, ID, keyword_list):
    secure_index = [0] * len(keyword_list)
    for i in range(len(keyword_list)):
        codeword = build_codeword(ID, build_trapdoor(master_key, keyword_list[i]))
        # print("Key for ", keyword_list[i], "is ", codeword, "\n")
        secure_index[i] = codeword
    random.shuffle(secure_index)
    return secure_index

def searchable_encryption(index_table, master_key):
    # raw_data = pd.read_csv(index_table)
    # features = list(raw_data)
    # print(raw_data)
    # raw_data = raw_data.values
    # print(raw_data)
    # document_number = [i for i in range(0, len(features)) if features[i] in keyword_type_list]

    # index_header = []
    # for i in range(1, len(keyword_type_list) + 1):
    #     index_header.append("doc_" + str(i))
    document_index = {}
    # start_time = time.time()
    cntr=0
    for keyArr, valArr in index_table.items():
        # record = raw_data[row]
        enckey = build_index(master_key, cntr, keyArr)
        encval = build_index(master_key, cntr, valArr)
        document_index[tuple(enckey)]  = encval
        
        cntr+=1
    # print("hello")
    print(document_index)

    # encr_index_table = {}
    # i=0
    # for key in index_table:
    #     encr_row = build_index(i, index_table[key])
    #     encr_index_table[key] = encr_row

if __name__ == "__main__":
    index_str = sys.argv[1]
    key = sys.argv[2]
    # print(index_str)
    # print(key)
    index_str = index_str[1:-4]
    index_str+="}"
    json_acceptable_string = index_str.replace("'", "\"")
    index_table = ast.literal_eval(json_acceptable_string)
    searchable_encryption(index_table, key)
    # print("Hello")