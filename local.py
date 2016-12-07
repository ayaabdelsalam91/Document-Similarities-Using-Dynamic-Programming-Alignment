#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy
import re
import time
import sys
import bigram
import Similarity
from TrainingDataProcessing import *
from Testing import *
#Comment

def local_extension(s1, s2, sim_fun, p_gap):
    len1 = len(s1)+1
    len2 = len(s2)+1
    table = numpy.zeros([len1, len2])
    max_score = 0

    for i in range(1, max(len1, len2)):
        new_scores = []
        if i < len1:
            for j in range(1, min(i, len2)):
                score1 = table[i, j-1] + p_gap
                score2 = table[i-1, j-1]+sim_fun(s1[i-1], s2[j-1])
                score3 = table[i-1, j] + p_gap
                table[i, j] = max(score1, score2, score3)
                new_scores.append(table[i, j])
        if i < len2:
            for j in range(1, min(i, len1)):
                score1 = table[j, i-1] + p_gap
                score2 = table[j-1, i-1]+sim_fun(s1[i-1], s2[j-1])
                score3 = table[j-1, i] + p_gap
                table[j, i] = max(score1, score2, score3)
                new_scores.append(table[i, j])
        if i < len1 and i < len2:
            score1 = table[i, i-1] + p_gap
            score2 = table[i-1, i-1]+sim_fun(s1[i-1], s2[i-1])
            score3 = table[i-1, i] + p_gap
            table[i, i] = max(score1, score2, score3)
            new_scores.append(table[i, i])
        new_max = max(new_scores)
        if new_max > max_score:
            max_score = new_max
        if i >= 3 and new_max < max_score/3:
            break
    return max_score



def bigram_alignment(s1, s2, pos1, pos2, sim_fun, p_gap):
    max_score = 0
    for i in pos1:
        for j in pos2:
            temp = 3 + local_extension(s1[i+2:], s2[i+2:], sim_fun, p_gap) + local_extension(s1[:i], s2[:i], sim_fun, p_gap)
            if temp > max_score:
                max_score = temp
    return max_score

def local_heuristics(s1, s2, sim_fun, p_gap, transformer):
    bigram_list = bigram.get_bigram([s1, s2])
    bigram_s1 = bigram_list[0].split(' ')
    bigram_s2 = bigram_list[1].split(' ')
    # tfidf = transformer.transform(bigram_list)
    # dictionary = {}
    # for i in transformer.vocabulary_:
    #     dictionary[transformer.vocabulary_[i]] = i
    # print dictionary
    # sum_tfidf = tfidf.sum(0)
    # print sum_tfidf
    # tfidf_orders = sum_tfidf.argsort()
    # print tfidf_orders
    count = 0
    score = 0
    flags = [0] * len(bigram_s1)
    for i in range(len(bigram_s1)):
        if flags[i] != 0:
            continue
        pos1 = []
        pos2 = []
        for j in range(len(bigram_s1)):
            if bigram_s1[i] == bigram_s1[j]:
                print bigram_s1[j]
                pos1.append(j)
                flags[j] = 1
        for j in range(len(bigram_s2)):
            if bigram_s1[i] == bigram_s2[j]:
                print bigram_s2[j]
                pos2.append(j)
        print pos1, pos2
        if len(pos2) > 0:
            score += bigram_alignment(s1, s2, pos1, pos2, sim_fun, p_gap)
            count += 1
    if count == 0 or count == 1:
        score = local_alignment(s1, s2, sim_fun, p_gap)
    return score




if __name__ == "__main__":
    # f_train = sys.argv[1]
    f_train = 'train.txt'
    texts = bigram.get_test_texts(f_train)
    bigram_texts = bigram.get_bigram(texts)
    transformer = bigram.tf_idf(bigram_texts)
    p_gap = -0.5
    print local_heuristics(texts[0], texts[2], Similarity.get_similarity_from_wordnet, p_gap, transformer)
