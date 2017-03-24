#!/usr/bin/python
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag

#To tokenize 
def tokenize(data):
    sent_tokens = sent_tokenize(data)
    word_tokens = [word_tokenize(sent) for sent in sent_tokens]
    return sent_tokens, word_tokens
#word_tokenize the data; for idf calculation
def get_words(data):
    words = word_tokenize(data)
    return words
