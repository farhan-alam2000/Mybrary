import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Hash import MD5
from Cryptodome.Random import random
import numpy as np
import time
import hashlib
from PyPDF2 import PdfFileWriter, PdfFileReader
import sys

def build_trapdoor(MK, keyword):
    keyword_index = MD5.new()
    keyword_index.update(str(keyword).encode('utf-8'))
    # print(keyword_index)
    # key=bytes(MK,'hex');
    key = bytes.fromhex("0123456789abcdef0123456789abcdef")
    ECB_cipher = AES.new(key, AES.MODE_ECB)
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
        secure_index[i] = codeword
    random.shuffle(secure_index)
    return secure_index

def searchable_encryption(index_table, master_key):
    raw_data = pd.read_csv(index_table)
    features = list(raw_data)
    print(raw_data)
    raw_data = raw_data.values
    # print(raw_data)
    # document_number = [i for i in range(0, len(features)) if features[i] in keyword_type_list]

    # index_header = []
    # for i in range(1, len(keyword_type_list) + 1):
    #     index_header.append("doc_" + str(i))
    document_index = []
    start_time = time.time()
    for row in range(raw_data.shape[0]):
        record = raw_data[row]
        res = build_index(master_key, row, record)
        document_index.append(res)

    time_cost = time.time() - start_time
    print (time_cost)
    document_index_dataframe = pd.DataFrame(np.array(document_index), columns=features)
    document_index_dataframe.to_csv("yes_index.csv") #document.split(".")[0] + 

    # encr_index_table = {}
    # i=0
    # for key in index_table:
    #     encr_row = build_index(i, index_table[key])
    #     encr_index_table[key] = encr_row

def encrypt_doc(doc_name, master_key):
    out = PdfFileWriter()
    file = PdfFileReader(doc_name)
    num = file.numPages
    for idx in range(num):
        page = file.getPage(idx)        
        out.addPage(page)

    password = master_key
    out.encrypt(password)

    with open(doc_name + "_encrypted.pdf", "wb") as f:
        out.write(f)

if __name__ == "__main__":
    master_key = "0123456789abcdef0123456789abcdef"
    # master_key = open("masterkey").read()
    # if len(master_key) > 16:
    #     print ("the length of master key is larger than 16 bytes, only the first 16 bytes are used")
    #     master_key = bytes(master_key[:16])

    # keyword_list_file_name = input("please input the file stores keyword type:  ")
    # keyword_type_list = open("keywordlist").read().split(",")
    # document_name="D:\work\BTP\CODE\Backend\index.csv"
    doc_text = sys.argv[1]
    # doc_text = "India, officially the Republic of India, is a country in South Asia. It is the seventh largest country by area, the second most populous country, and the most populous democracy in the world. Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west; China, Nepal, and Bhutan to the north; and Bangladesh and Myanmar to the east. In the Indian Ocean, India is in the vicinity of Sri Lanka and the Maldives; its Andaman and Nicobar Islands share a maritime border with Thailand, Myanmar, and Indonesia. The nation's capital city is New Delhi."
    index_name = "C:/Users/alaam/OneDrive/Desktop/python/FuzzBuzz/Backend/index.csv" 
    searchable_encryption(index_name, master_key)
    # encrypt_doc(doc_text, master_key)
    print ("Finished")
