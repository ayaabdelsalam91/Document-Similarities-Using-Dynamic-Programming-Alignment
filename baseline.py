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
    labels = []
    texts = []
    for line in f:
        label, content = line.split('\t')
        labels.append(label.strip())
        texts.append(content.strip())
    return labels, texts

def get_label_instances(labels):
    label_set = list(set(labels))
    label_num = len(label_set)
    label_instances = []
    for i in range(label_num):
        label_instances.append([])
    for i in range(len(labels)):
        label_instances[label_set.index(labels[i])].append(i)
    return label_instances

def eval(doc_idx, labels):
    count = 0
    for idx, label in zip(doc_idx, labels):
        if labels[idx] == label:
            count += 1
    return float(count)/min(len(doc_idx), len(labels))

def closest_docs(texts, label_instances, transformer):
    doc_num = len(texts)
    label_num = len(label_instances)
    label_counts = [len(l) for l in label_instances]
    closest_idx = []
    sampled = numpy.zeros([doc_num, label_num], dtype=int)
    for i in range(label_num):
        for j in range(doc_num):
            sampled[j, i] = label_instances[i][random.randint(0, label_counts[i]-1)]
    for i in range(doc_num):
        closest_idx.append(find_closest(i, sampled[i], texts, transformer))
    return sampled, closest_idx

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
    labels, texts = get_dataset(f_train)
    transformer = tf_transf(texts)
    label_instances = get_label_instances(labels)
    sampled, closest_idx = closest_docs(texts, label_instances, transformer)
    print eval(closest_idx, labels)
