#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import numpy
from sklearn.feature_extraction.text import CountVectorizer
#Comment

bigram_delimiter = 'aazf'

def get_dataset(fname):
    f = open(fname)
    texts = []
    for line in f:
        if line.strip() == '':
            continue
        texts.append(line.strip())
    return texts

def eval(correct, predicted):
    count = 0
    for idx1, idx2 in zip(correct, predicted):
        if idx1 == idx2:
            count += 1
    return float(count)/min(len(correct), len(predicted))

def closest_docs(texts, transformer, comparation_num):
    doc_num = len(texts)
    targets = []
    correct_idx = []
    closest_idx = []
    sampled = numpy.zeros([doc_num/2, comparation_num], dtype=int)
    for i in range(0, doc_num/2):
        targets.append(2*i)
        correct_idx.append(2*i+1)
        sampled[i, 0] = 2*i+1
        for j in range(1, comparation_num):
            sampled[i, j] = random.randint(0, doc_num-1)
            while(sampled[i, j] == 2*i or sampled[i, j] == 2*i+1):
                sampled[i, j] = random.randint(0, doc_num-1)
    for i in range(len(targets)):
        closest_idx.append(find_closest(targets[i], sampled[i], texts, transformer))
    return sampled, closest_idx, correct_idx, targets

def find_closest(target_idx, compared_idx, texts, transformer):
    highest_score = -float("inf")
    closest = -1
    for idx in compared_idx:
        tf = transformer.transform([texts[target_idx], texts[idx]])
        score = tf[0].dot(tf[1].T)/((tf[0].dot(tf[0].T))*tf[1].dot(tf[1].T))
        if score > highest_score:
            closest = idx
            highest_score = score
    return closest

def tf_transf(texts):
    transformer = CountVectorizer()
    transformer.fit(texts)
    return transformer

if __name__ == "__main__":
    # f_train = sys.argv[1]
    f_train = 'sen_concatenate_corpus.txt'
    texts = get_dataset(f_train)
    transformer = tf_transf(texts)
    sampled, predicted_idx, correct_idx, _ = closest_docs(texts, transformer, 5)
    print eval(correct_idx, predicted_idx)
