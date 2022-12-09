import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Hash import MD5
import sys
import os
# import time

def build_codeword(ID, trapdoor):
    ID_index = MD5.new()
    ID_index.update(str(ID).encode('utf-8'))
    ECB_cipher = AES.new(b']o\x1f\xbe\xbe-2\x12]\xf5 \nC!\x86\xa3', AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest())

def search_index(document, trapdoor):
    search_result = []
    data_index = pd.read_csv(document)
    data_index = data_index.values
    # start_time = time.time()
    for row in range(data_index.shape[0]):
        if str(build_codeword(row,trapdoor)) in data_index[row]:
            search_result.append(row)

    # print time.time() - start_time
    return search_result

if __name__ == "__main__":

    keyword = sys.argv[1]
    keyword_trapdoor = open(keyword + "_trapdoor").read().strip()
    search_result = search_index("yes_index.csv", keyword_trapdoor)
    print ("The identifier for the set of files that contain the keyword are: \n", search_result)
    os.remove(keyword+"_trapdoor")