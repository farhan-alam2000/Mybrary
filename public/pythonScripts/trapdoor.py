import csv
from Cryptodome.Cipher import AES
from Cryptodome.Hash import MD5
import sys
from fuzzygeneration import addFuzzy

def build_trapdoor(MK, keyword):
    keyword_index = MD5.new()
    keyword_index.update(str(keyword).encode('utf-8'))
    # key = bytes.fromhex("0123456789abcdef0123456789abcdef")
    MK = MK.encode('utf-8')
    MK_length = len(MK)
    if MK_length < 16:
        MK += bytes(16 - MK_length)
    ECB_cipher = AES.new(MK, AES.MODE_ECB)
    # ECB_cipher = AES.new(key, AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())

if __name__ == "__main__":

    keywords = sys.argv[1]
    password = sys.argv[2]
    # print("password is ", password)
    fuzzySet = addFuzzy(keywords, 1)
    # finalfuzzySet = []
    # for term in keywords.split():
    #      fuzzySet = addFuzzy(term, 1)
    #      for fuzz in fuzzySet:
    #         finalfuzzySet.append(fuzz)

    # fuzzySet = addFuzzy(keywords, 1)
    # trapdoor_file = open(keyword + "_trapdoor", "w+")
    trapdoor_set = []
    for word in fuzzySet:
        trapdoor_of_keyword = build_trapdoor(password, word)
        print(trapdoor_of_keyword, len(trapdoor_of_keyword))
        trapdoor_string = trapdoor_of_keyword.hex()
        # print(type(trapdoor_of_keyword))
        # csv = str(trapdoor_of_keyword)[2:-1]
        # csv = csv.replace('\\t', ',').replace('\\n', '\n')
        # print(csv, file=open('trapdoors.csv', 'w'))
        trapdoor_set.append(trapdoor_string)
    # trapdoor_bytearr = bytearray(trapdoor_set)
    # byteformat = bytes(trapdoor_bytearr)

    with open('trapdoors.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Heading"])
        for byte_obj in trapdoor_set:
            writer.writerow([byte_obj])
            
    print("Saved Trapdoor file")