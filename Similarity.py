import sys
import math
from nltk.corpus import wordnet
from TrainingDataProcessing import *
import time
import numpy

def get_similarity_from_wordnet(word1,word2):
    if(word1 == word2):
        return 1
    try:
        wordFromList1 = wordnet.synsets(word1)
        wordFromList2 = wordnet.synsets(word2)
        if wordFromList1 and wordFromList2:
            s = wordFromList1[0].wup_similarity(wordFromList2[0])
            # s = 0
            # count = 0
            # for synset1 in wordFromList1:
            #     for synset2 in wordFromList2:
            #         temp = synset1.wup_similarity(synset2)
            #         if temp:
            #             s += temp
            #             count += 1
            # if count == 0:
            #     s = -1
            # else:
            #     s = s/count
        else:
        	s=-1
    except UnicodeDecodeError:
        s = -1
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

def get_similarity_from_glove(word1,word2,dictionary,glove,Secondary_dictionary=None,Secondary_glove=None):
    if(word1 == word2):
        return 1
    if(word1 in dictionary) and (word2 in dictionary):
        X_line = glove[dictionary[word1]]
        Y_line = glove[dictionary[word2]]
        X_vector = [float(num) for num in X_line[1:301]]
        Y_vector = [float(num) for num in Y_line[1:301]]
        s=_cosine_similarity( X_vector, Y_vector)
    elif Secondary_dictionary != None :
        if(word1 in Secondary_dictionary) and (word2 in Secondary_dictionary):
            X_line = Secondary_glove[Secondary_dictionary[word1]]
            Y_line = Secondary_glove[Secondary_dictionary[word2]]
            X_vector = [float(num) for num in X_line[1:301]]
            Y_vector = [float(num) for num in Y_line[1:301]]
            s=_cosine_similarity( X_vector, Y_vector)
        else:
            s=-1
    else:
        s=-1
    # if(s!=-1):
    #     print word1 , word2 , s
    return s

def get_sentence_similarity(FirstSentence,SecondSentence,Main_dictionary,Main_glove,dictionary,glove_dictionary):
    table = string.maketrans("","")
    FirstSentence = FirstSentence.lower()
    SecondSentence = SecondSentence.lower()
    FirstSentence = FirstSentence.split(' ')
    SecondSentence = SecondSentence.split(' ')
    len1 = len(FirstSentence)+1
    len2 = len(SecondSentence)+1
    FirstSentence_vector=[0] * 300
    SecondSentence_vector=[0] *  300
    num=0
    for i in range(0, len1-1):
        if(len(FirstSentence[i])>0):
            FirstSentence[i] = FirstSentence[i].translate(table, string.punctuation)
            # if(FirstSentence[i][-1] == '.' or FirstSentence[i][-1] == '?'):
            #   FirstSentence[i]=FirstSentence[i][:-1]
            vector = get_word_from_glove(FirstSentence[i],Main_dictionary,Main_glove,dictionary,glove_dictionary)
            if(vector != -1 and vector !=[]):
                num+=1
                FirstSentence_vector = [FirstSentence_vector[j] + vector[j] for j in range(300)]
    if(num > 1):
        FirstSentence_vector = [FirstSentence_vector[j]/num for j in range(300)]
    else:
        print FirstSentence
    num=0
    for i in range(0, len2-1):
        if(len(SecondSentence[i])>0):
            SecondSentence[i] = SecondSentence[i].translate(table, string.punctuation)
            # if(SecondSentence[i][-1] == '.' or SecondSentence[i][-1] == '?'):
            #   SecondSentence[i]=SecondSentence[i][:-1]
            vector = get_word_from_glove(SecondSentence[i],Main_dictionary,Main_glove,dictionary,glove_dictionary)
            if(vector != -1 and vector !=[]):
                num+=1
                SecondSentence_vector = [SecondSentence_vector[j] + vector[j] for j in range(300)]
    if(num > 1):
        SecondSentence_vector = [SecondSentence_vector[j]/num for j in range(300)]
    else:
        print SecondSentence
    similarity = _cosine_similarity(FirstSentence_vector,SecondSentence_vector)
    # print similarity[0][0]
    return normalized(-1,1,0,5,similarity)

# def global_alignment(s1, s2, sim_fun, glove, dictionary, p_gap):
#     tic = time.time()
#     s1 = s1.lower()
#     s2 = s2.lower()
#     print s1
#     print s2
#     s1 = s1.split(' ')
#     s2 = s2.split(' ')
#     len1 = len(s1)+1
#     len2 = len(s2)+1
#     table = numpy.zeros([len1, len2])
    
#     for i in range(len2):
#         table[0, i] = i*p_gap;
#     for i in range(len1):
#         table[i, 0] = i*p_gap;

#     for i in range(1, len1):
#         for j in range(1, len2):
#             score1 = table[i, j-1] + p_gap
#             score2 = table[i-1, j-1]+sim_fun(s1[i-1], s2[j-1], glove, dictionary)
#             score3 = table[i-1, j] + p_gap
#             table[i, j] = max(score1, score2, score3)

#     score = table[len1-1, len2-1]
#     toc = time.time()
#     print('Processing time: %r'
#            % (toc - tic))
#     exit(0)
#     return score
 
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

