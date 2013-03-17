import re
import nltk

from config import *
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.lancaster import LancasterStemmer

st = LancasterStemmer()

def clean(text):
    # Remove hyphens
    text = re.sub(r'[\']', '', text)
    # Replace non-whitespace, non-alphanumeric characters with spaces
    return re.sub(r'[^\w\s]+', ' ', text)

def tokenize(text):    
    # Tokenize the text, then stem each word
    return [st.stem(x) for x in wordpunct_tokenize(clean(text))]

def find_keyword(word, text):
    word = tuple(tokenize(word))
    ngrams = nltk.ngrams(text, len(word))
    return word in ngrams

def find_keywords(text):
    return sum([score for word, score in KEYWORDS.iteritems() 
        if find_keyword(word, text)])

def score(title, abstract):
    tt = tokenize(title)
    aa = tokenize(abstract)

    ttitle = find_keywords(tt)
    aabstract = find_keywords(aa)

    return ttitle * 1.5 + aabstract
