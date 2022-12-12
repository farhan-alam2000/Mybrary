import csv
import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Hash import MD5
from Cryptodome.Random import random
import sys
import ast

def build_trapdoor(MK, keyword):
    keyword_index = MD5.new()
    keyword_index.update(str(keyword).encode('utf-8'))
    MK = MK.encode('utf-8')
    MK_length = len(MK)
    if MK_length >16:
        MK = MK[:16]
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
        # print(cntr, keyArr)
        enckey = build_index(master_key, cntr, keyArr)
        encval = build_index(master_key, cntr, valArr)
        document_index[tuple(enckey)]  = encval
        
        cntr+=1
    return document_index
    # print("hello")
    # print(document_index)

    # encr_index_table = {}
    # i=0
    # for key in index_table:
    #     encr_row = build_index(i, index_table[key])
    #     encr_index_table[key] = encr_row

if __name__ == "__main__":
    index_str = sys.argv[1]
    master_key = sys.argv[2]
    # print("password is ", key)
    # print("INDEX STR IS ", index_str)
    # index_str = index_str[1:-4]
    # index_str+="}"
    # print("INDEX STR IS ", index_str)
    # json_acceptable_string = index_str.replace("'", "\"")
    # index_table = ast.literal_eval(json_acceptable_string)
    df = pd.read_csv("hello.csv")
    inverted_index = df.to_dict(orient='list')
    index_new = {}
    for key, val in inverted_index.items(): 
        # print(key, val)
        if(key=="document"): index_new[key] = val
        else:
            tuple_str = ast.literal_eval(key)
            index_new[tuple_str] = val
            inverted_index = index_new
    print("THE INVERTED INDEX IS ", inverted_index, type(inverted_index))
    document_index = searchable_encryption(inverted_index, master_key)

    # with open('index.csv', 'w',  encoding="utf-8", newline='') as csvfile:
    #     writer = csv.DictWriter(csvfile)
    #     # writer.writeheader()
    #     for key,value in document_index.items():
    #         s = str(value)
    #         keystr = str(key)
    #         # print(csvstr)
    #         # writer.writerow(csvstr)
    #         writer.writerow([keystr, s[1:-1]])
    #     # csvfile.write(csvstr.split("\n"))

    # writing to csv file
    with open("index.csv", "w") as outfile:
        writerfile = csv.writer(outfile)
        # dict_rows = [[key, value] for key, value in document_index.items()]
        writerfile.writerow(document_index.keys())        
        writerfile.writerows(zip(*document_index.values()))
    print(document_index)

    # for key, values in document_index.items():
    #     valuestr = ','.join(values)