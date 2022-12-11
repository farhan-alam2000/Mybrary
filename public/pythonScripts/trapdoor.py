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

    keyword = sys.argv[1]
    password = sys.argv[2]
    fuzzySet = addFuzzy(keyword, 1)

    # trapdoor_file = open(keyword + "_trapdoor", "w+")
    trapdoor_set = []
    for word in fuzzySet:
        trapdoor_of_keyword = build_trapdoor(password, word)
        # print(trapdoor_of_keyword)
        trapdoor_set.append(trapdoor_of_keyword)

    print(trapdoor_set)