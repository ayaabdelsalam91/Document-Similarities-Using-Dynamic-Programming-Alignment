#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy
import re
import time
#Comment

def global_alignment(s1, s2, sim_fun, glove, dictionary, p_gap):
    tic = time.time()
    s1 = s1.lower()
    s2 = s2.lower()
    print s1
    print s2
    s1 = s1.split(' ')
    s2 = s2.split(' ')
    len1 = len(s1)+1
    len2 = len(s2)+1
    table = numpy.zeros([len1, len2])
    
    for i in range(len2):
        table[0, i] = i*p_gap;
    for i in range(len1):
        table[i, 0] = i*p_gap;

    for i in range(1, len1):
        for j in range(1, len2):
            score1 = table[i, j-1] + p_gap
            score2 = table[i-1, j-1]+sim_fun(s1[i-1], s2[j-1], glove, dictionary)
            score3 = table[i-1, j] + p_gap
            table[i, j] = max(score1, score2, score3)

    score = table[len1-1, len2-1]
    toc = time.time()
    print('Processing time: %r'
           % (toc - tic))
    exit(0)
    return score