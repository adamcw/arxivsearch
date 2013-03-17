KEYWORDS = {
    'topological': 10, 
    'qubit': 5, 
    'qec': 20,
    'tqec': 20,
    'ftqc': 20,
    'ftqec': 20,
    'fault tolerant': 25,
    'error correction': 20,
    'error': 5,
    'surface code': 20,
    'code': 10, 
    'circuit': 15,
    'quantum computing': 15,
    'computer': 15, 
    'lower': 5,
    'distillation': 4,
    'threshold': 6, 
    'cluster state': 15,
    'error rate': 10,
    'classical processing': 15,
    'ion trap': 10,
    'scalability': 8, 
    'scalable': 8, 
    'stabiliser': 15,
    'minimum weight': 25,
    'perfect matching': 25,
    'gate': 10,
    'cnot': 15,
    'shor': 20, 
    'pauli': 20,
    'clifford': 20,
    'toffoli': 20,
    'grover': 20, 
    'algorithm': 20,
    'hadamard': 10, 
    'unitary': 5,
    'logical qubit': 15,
    'logical': 7,
    'nearest neighbour': 15, 
    'nearest neighbor': 15, 
}

import re
import nltk
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
