import string
from nltk.corpus import stopwords
import sys

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

text = sys.argv[1]
cleaned_doc = text_preprocess(text)
print(cleaned_doc)