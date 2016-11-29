import sys
import math
from nltk.corpus import wordnet
from TrainingDataProcessing import *
import time
import numpy

def get_similarity_from_wordnet(word1,word2):
    if(word1 == word2):
        return 1
    wordFromList1 = wordnet.synsets(word1)
    wordFromList2 = wordnet.synsets(word2)
    if wordFromList1 and wordFromList2:
    	s = wordFromList1[0].wup_similarity(wordFromList2[0])
    else:
    	s=-1
    if s== None:
        s=-1
    return s

def _cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def get_similarity_from_glove(word1,word2,dictionary,glove):
    # print word1
    if(word1 == word2):
        return 1
    if(word1 in dictionary) and (word2 in dictionary):
        X_line = glove[dictionary[word1]]
        Y_line = glove[dictionary[word2]]
        X_vector = [float(num) for num in X_line[1:301]]
        Y_vector = [float(num) for num in Y_line[1:301]]
        s=_cosine_similarity( X_vector, Y_vector)
    else:
        s=-1
    return s

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
 
if __name__ == "__main__":
	dic=sys.argv[1]
	_glove=sys.argv[2]
	dictionary = read_dictionary(dic)
	glove= read_glove(_glove)
	tic = time.time()
	s= get_similarity_from_glove("mahhhjgjhth","cat",dictionary,glove)
	toc = time.time()
	print s
	print('Processing time: %r'
           % (toc - tic))
	tic = time.time()
	s= get_similarity_from_wordnet('cat','mahhhjgjhth')
	toc = time.time()
	print('Processing time: %r'
           % (toc - tic))
	#
	print s

