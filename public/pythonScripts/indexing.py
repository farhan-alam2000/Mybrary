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

n_doc=4
inverted_index = {}
# document ="India, officially the Republic of India, is a country in South Asia. It is the seventh largest country by area, the second most populous country, and the most populous democracy in the world. Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west; China, Nepal, and Bhutan to the north; and Bangladesh and Myanmar to the east. In the Indian Ocean, India is in the vicinity of Sri Lanka and the Maldives; its Andaman and Nicobar Islands share a maritime border with Thailand, Myanmar, and Indonesia. The nation's capital city is New Delhi."

# document = sys.argv[1]
# def text_extract(doc_name):
#     pdfFileObj = open(doc_name, 'rb')
#     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#     doc_text = (pdfReader.getPage(0).extractText())
#     pdfFileObj.close()
    
def createIndex(fuzzySet, doc_no, doc_id):
    inverted_index["document"] = inverted_index.get("document", [""]*n_doc)
    inverted_index["document"][doc_no] = doc_id
    key = tuple(fuzzySet)
    inverted_index[key]= inverted_index.get(key, [0]*n_doc)
    inverted_index[key][doc_no] +=1

# def addFuzzy(keyword):
#     # Set the maximum edit distance
#     max_distance = 2

#     # Generate a set of fuzzy keywords using the distance algorithm from the fuzzywuzzy package
#     fuzzy_keywords = set()
#     fuzzy_keywords.add(keyword)  # Add the given keyword to the set

#     # Generate variations of the keyword by removing or adding letters
#     for i in range(len(keyword)):
#         fuzzy_keywords.add(keyword[:i] + keyword[i + 1:])  # Remove a letter
#         for c in "abcdefghijklmnopqrstuvwxyz":
#             fuzzy_keywords.add(keyword[:i] + c + keyword[i:])  # Add a letter
#             fuzzy_keywords.add(keyword[:i] + c + keyword[i + 1:])  # Substitute a letter

#     print("Without filtering", fuzzy_keywords)
#     print(len(fuzzy_keywords))
#     # Filter the fuzzy keywords to include only those with a distance of 2 or less
#     fuzzy_keywords = {word for word in fuzzy_keywords if fuzz.distance(word, keyword, max_distance) <= max_distance}

#     # Print the fuzzy keyword set
#     print("With filtering", fuzzy_keywords)
#     print(len(fuzzy_keywords))
#     return fuzzy_keywords

# # ans = addFuzzy("cat")

# fuzzy_keywords = []
# def addFuzzy2(keyword, d):
#     if d>1:
#         addFuzzy2(keyword, d-1)
    
#     if d==0:
#         fuzzy_keywords.append(keyword)
#     else:
#         for k in range(len(fuzzy_keywords)):
#             for j in range(1, 2*len(fuzzy_keywords)):
#                 if j&1:
#                     fuzzkey = fuzzy_keywords[k]
#                     fuzzkey.insert('*', math.floor((j+1)/2))
#                 else:
#                     fuzzkey = fuzzy_keywords[k]
#                     fuzzkey[math.floor(j/2)] = '*'
                
#                 if fuzzkey not in fuzzy_keywords:
#                     fuzzy_keywords.append(fuzzkey)
#     print(fuzzy_keywords)
#     return fuzzy_keywords

# addFuzzy2("cat", 1)

def handleFuzzy(doc, doc_no, doc_id):
    for term in doc.split():
        fuzzySet = addFuzzy(term, 1)
        createIndex(fuzzySet, doc_no, doc_id)

# doc_name = "D:/work/BTP/CODE/India.pdf"
# print(doc_name)
# print(open(doc_name).read())
# doc_text = text_extract(doc_name)

# CODE
cleaned_doc = sys.argv[1]
key = sys.argv[2]
# doc_text = "India, is a country."
#  Bounded by t officially the Republic of India,he Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west; China, Nepal, and Bhutan to the north; and Bangladesh and Myanmar to the east. In the Indian Ocean, India is in the vicinity of Sri Lanka and the Maldives; its Andaman and Nicobar Islands share a maritime border with Thailand, Myanmar, and Indonesia. The nation's capital city is New Delhi."

# print("\nThe cleaned text is: \n", cleaned_doc)
handleFuzzy(cleaned_doc, 0, key)
print(str(inverted_index))
# FINAL RESULT OF THIS CODE IS INVERTED INDEX TABLE, IN THE FORM OF A DICTIONARY


# indexTable = createIndex(fuzzySet, 0)
# print("\nThe inverted index table: \n", indexTable)
# CODE

# index_header = ["keyword"]
# for i in range(1, (n_doc) + 1):
#     index_header.append("doc_" + str(i))

# csvstr=""
# for key,value in inverted_index.items():
#     # print(key, value)
#     s = str(value)
#     keystr = str(key)
#     csvstr += f"{keystr},{s[1:-1]}" + "\n"
#     print(csvstr)

# with open('index.csv', 'w',  encoding="utf-8", newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=index_header)
#     writer.writeheader()
#     for key,value in inverted_index.items():
#         s = str(value)
#         keystr = str(key)
#         # print(csvstr)
#         # writer.writerow(csvstr)
#         writer.writerow([keystr, s[1:-1]])
    # csvfile.write(csvstr.split("\n"))

# writer = csv.writer(csvfile)
#   writer.writerow([tuple_string])