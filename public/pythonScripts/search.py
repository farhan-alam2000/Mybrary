import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Hash import MD5
import sys
import os
import ast
# import time

def build_codeword(ID, trapdoor):
    ID_index = MD5.new()
    ID_index.update(str(ID).encode('utf-8'))
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest())

def search_index(document, trapdoors):
    search_result = []
    # data_index = pd.read_csv(document)
    # data_index = data_index.values
    # start_time = time.time()
    # for row in range(data_index.shape[0]):
    #     if str(build_codeword(row, trapdoor)) in data_index[row]:
    #         search_result.append(row)

    for trapdoor in trapdoors:
        cntr=0
        for key, val in document.items():
            for keyword in key:
                if(str(build_codeword(cntr, trapdoor)) == keyword):
                    search_result.append(cntr)
                    break
            cntr+=1
        # print time.time() - start_time
    return search_result

if __name__ == "__main__":

    trapdoor_set = sys.argv[1]
    # ind_table_str = sys.argv[2]
    # print("HELLO")
    # print(ind_table_str)

    # print("THE TRAPDOOR SET IN SEARCH.PY IS ", trapdoor_set)

    # json_acceptable_string = ind_table_str.replace("'", "\"")
    # index_table = ast.literal_eval(json_acceptable_string)
    # print(index_table)
    # # keyword_trapdoor = open(keyword + "_trapdoor").read().strip()
    
    # search_result = search_index(index_table, trapdoors)
    # print ("The identifier for the set of files that contain the keyword are: \n", search_result)
    # os.remove(keyword+"_trapdoor")