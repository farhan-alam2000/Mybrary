import pandas as pd
import numpy as np
import time
import string
from nltk.corpus import stopwords
import csv
import sys
import PyPDF2

n_doc=4
inverted_index = {}
# document ="India, officially the Republic of India, is a country in South Asia. It is the seventh largest country by area, the second most populous country, and the most populous democracy in the world. Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west; China, Nepal, and Bhutan to the north; and Bangladesh and Myanmar to the east. In the Indian Ocean, India is in the vicinity of Sri Lanka and the Maldives; its Andaman and Nicobar Islands share a maritime border with Thailand, Myanmar, and Indonesia. The nation's capital city is New Delhi."

doc_text =""

# document = sys.argv[1]
# def text_extract(doc_name):
#     pdfFileObj = open(doc_name, 'rb')
#     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#     doc_text = (pdfReader.getPage(0).extractText())
#     pdfFileObj.close()

def text_preprocess(text):
    nltk_english_stopwords = stopwords.words('english')
    # remove punctuations
    trans = str.maketrans('', '', string.punctuation)
    text = text.translate(trans)
    # lowercase the text
    text = text.lower()
    # remove stopwords
    cleaned_text = ""
    for word in text.split():
        if word not in nltk_english_stopwords:
            cleaned_text += word + " " 
    return cleaned_text
    
def createIndex(doc, i):
    for term in doc.split():
        inverted_index[term]= inverted_index.get(term, [0]*1)
        inverted_index[term][i] +=1
    return inverted_index

# doc_name = "D:/work/BTP/CODE/India.pdf"
# print(doc_name)
# print(open(doc_name).read())
# doc_text = text_extract(doc_name)
doc_text = sys.argv[1]
cleaned_doc = text_preprocess(doc_text)
print("\nThe cleaned text is: \n", cleaned_doc)
indexTable = createIndex(cleaned_doc, 0)
print("\nThe inverted index table: \n", indexTable)

# index_header = ["keyword"]
# for i in range(1, (n_doc) + 1):
#     index_header.append("doc_" + str(i))

# csvstr=""
# for key,value in indexTable.items():
#     s = str(value)
#     csvstr += f"{key},{s[1:-1]}" + "\n"

# with open('index.csv', 'w',  encoding="utf-8") as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=index_header)
#     writer.writeheader()
#     csvfile.write(csvstr)
