import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Hash import MD5
import sys

def build_codeword(ID, trapdoor):
    ID_index = MD5.new()
    ID_index.update(str(ID).encode('utf-8'))
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest())

def obtain_trapdoors():
    tr = pd.read_csv("trapdoors.csv")
    # print(tr)
    byte_object = tr['Heading']
    trapdoors = []
    for byte in byte_object:
        # byte_object = bytes.fromhex(byte)
        trapdoors.append(byte)
    return trapdoors
    # byte_object = bytes(byte_object)
    # print(byte_object)
    # byte_object = bytes.fromhex(byte_object)
    # print(type(byte_object))
    # print(len(byte_object))
    # print(byte_object)
    # arr = tr.to_numpy()
    # print(arr)
    # for i in arr:
    #     print(len(i))
    #     print(type(i))
    #     temp = i.encode("utf-8")
    #     print(len(temp))
    # with open('trapdoors.csv', 'r') as csvfile:
    #     reader = csv.reader(csvfile)

    # for row in reader:
    #     byte_object = row[0]
    #     byte_object = bytes.fromhex(byte_object)
    #     print(byte_object, len(byte_object))


def search_index(document, trapdoors):
    data_index = pd.read_csv("index.csv")
    # print(data_index)

    # search_result = []
    keyword_matrix = data_index.columns[1:]

    # flag = 0
    for trapdoor in trapdoors:
        # print("For the trapdoor:YES")
        cntr=1
        byte_object = bytes.fromhex(trapdoor)
        # print(byte_object)
        for keyword_set in keyword_matrix:
                # print("for row ", cntr, "set is ", keyword_set)
                temp = str(build_codeword(cntr, byte_object))
                # print("the codeword is ", temp)
                if(temp in keyword_set):
                    return cntr
                cntr+=1
    return -1
    # index_table = data_index.T
    # index_table = data_index.tail(data_index.shape[1] -1)
    # print(index_table)
    # values = index_table.values
    # print(values)

    # for trapdoor in trapdoors:
    # print(index_table.shape[0])
    # for row in range(index_table.shape[0]):
    #     print(index_table.features)
    # first_column = index_table.iloc[:, 0]
    # print(first_column)
    # for i in first_column:
    #     print(i)


    # print(data_index.columns)
    # keywords  = data_index.columns[1:]
    # for trapdoor in trapdoors:
    #     for row in keywords:
    #         for keyword in row:
    #             print(keyword)

    # for trapdoor in trapdoors:
    #     cntr=0
    #     for key, val in document.items():
    #         for keyword in key:
    #             if(str(build_codeword(cntr, trapdoor)) == keyword):
    #                 search_result.append(cntr)
    #                 break
    #         cntr+=1
    #     # print time.time() - start_time
    # return search_result

if __name__ == "__main__":

    trapdoor_set = sys.argv[1]
    index_str = sys.argv[2]
    # print("HELLO ")
    # trapdoor_set = trapdoor_set[2:-4]
    # trapdoors = list(trapdoor_set.split(","))
    # # print(trapdoors)
    # for i in trapdoors:
    #     print(i, len(i))
    #     temp = i[2:-1]
        # byteobj = bytes(temp, "utf-8")
        # print(byteobj, len(byteobj))
        # byteobj = i.decode("utf-8")
        # print(byteobj, len(byteobj))
    # print("india".encode("utf-8"))
    # index_str = index_str[1:-3]
    # print(index_str)
    # index_str = "shdfshfdjsk:shgfskhfjdsk, sfksdhks:shfkjhsjhksk"
    # temp_str = index_str.split(":")
    # print(temp_str)
    # index_str+="}"
    # json_acceptable_string = index_str.replace("'", "\"")
    # json_acceptable_string = json_acceptable_string.replace("\\", ",")
    # print(json_acceptable_string)
    # index_table = json.loads(json_acceptable_string)
    # index_table = ast.literal_eval(json_acceptable_string)
    # print(index_table)
    # # keyword_trapdoor = open(keyword + "_trapdoor").read().strip()
    
    # search_result = search_index(index_table, trapdoors)
    # print ("The identifier for the set of files that contain the keyword are: \n", search_result)
    # os.remove(keyword+"_trapdoor")

    # search_result = search_index("index.csv", trapdoors)
    # print(search_result)

    trapdoors = obtain_trapdoors()
    search_result = search_index("index.csv", trapdoors)
    print(search_result)