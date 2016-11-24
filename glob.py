#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy

def process_line(s, dim):
    s = s.strip()
    char = s[0].upper()
    s = s[1:].strip()
    num_list = s.split(' ')
    arr = numpy.zeros(dim)
    i = 0
    for num in num_list:
        if num != '':
            if i < dim:
                arr[i] = int(num)
                i += 1
            else:
                print('Exceed dim upper limit in function "process_line"!')
                exit(0)
    return char, arr

def read_string(fname):
    f = open(fname)
    s_list = []
    s = ''
    for line in f:
        if line[0] == '>':
            if not s == '':
                s_list.append(s)
                s = ''
            continue 
        else:
            s += line.strip()
    if not s == '':
        s_list.append(s)
    f.close()
    return s_list[0], s_list[1]


def get_smatrix(fname):
    f = open(fname)
    aa = f.readline()
    aa = aa.replace(' ', '').strip()

    num_aa = len(aa)
    s_matrix = numpy.zeros([num_aa, num_aa])
    aa2num = {}
    for index, char in enumerate(aa):
        aa2num[char.upper()] = index

    for line in f:
        char, s_value = process_line(line, num_aa)
        s_matrix[aa2num[char], :] = s_value

    f.close()
    return s_matrix, aa2num 

def global_alignment(s_matrix, aa2num, s1, s2, p_gap):
    s1 = s1.upper()
    s2 = s2.upper()
    len1 = len(s1)+1
    len2 = len(s2)+1
    table = numpy.zeros([len1, len2])
    back_pointer = numpy.zeros([len1, len2])
    
    table[0, :] = range(0, len2*p_gap, p_gap)
    table[:, 0] = range(0, len1*p_gap, p_gap)

    for i in range(1, len1):
        for j in range(1, len2):
            score1 = table[i, j-1] + p_gap
            score2 = table[i-1, j-1]+s_matrix[aa2num[s1[i-1]], aa2num[s2[j-1]]]
            score3 = table[i-1, j] + p_gap
            table[i, j] = max(score1, score2, score3)

    score = table[len1-1, len2-1]
    return int(score)


m_blosum = 'BLOSUM62.txt'
m_pam = 'PAM250.txt'
s_file = 'rosalind_glob.txt'
p_gap = -5

s_matrix, aa2num = get_smatrix(m_blosum)
s1, s2 = read_string(s_file)
score = global_alignment(s_matrix, aa2num, s1, s2, p_gap)

print score