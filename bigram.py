#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sklearn.feature_extraction.text import TfidfVectorizer
#Comment

bigram_delimiter = 'aazf'

def get_test_texts(fname):
    f = open(fname)
    texts = []
    for line in f:
        label, content = line.split('\t')
        texts.append(content.strip().split(' '))
    return texts

def get_bigram(texts):
    bigram = []
    for line in texts:
        bigram.append(' '.join([line[i]+bigram_delimiter+line[i+1] for i in range(len(line)-1)]))
    return bigram

def bigram_to_words(string):
    return string.strip().split(bigram_delimiter)

def tf_idf(texts):
    transformer = TfidfVectorizer()
    m = transformer.fit_transform(texts)
    return transformer
    # print transformer.get_stop_words()

if __name__ == "__main__":
    # f_train = sys.argv[1]
    f_train = 'train.txt'
    texts = get_test_texts(f_train)
    bigram = get_bigram(texts)
    tf_idf(bigram)
