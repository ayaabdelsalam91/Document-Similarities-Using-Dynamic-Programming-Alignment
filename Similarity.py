import sys
import math
from nltk.corpus import wordnet
from TrainingDataProcessing import *
import time
import numpy
import string

def get_similarity_from_wordnet(word1,word2):
    if(word1 == word2):
        return 1
    try:
        wordFromList1 = wordnet.synsets(word1)
        wordFromList2 = wordnet.synsets(word2)
        if wordFromList1 and wordFromList2:
            s = wordFromList1[0].wup_similarity(wordFromList2[0])
        else:
            s=-1
    except UnicodeDecodeError:
        s = -1
    if s== None:
        s=-1
    return s

def get_similarity_from_avg_wordnet(word1,word2):
    if(word1 == word2):
        return 1
    try:
        wordFromList1 = wordnet.synsets(word1)
        wordFromList2 = wordnet.synsets(word2)
        if wordFromList1 and wordFromList2:
            s = 0
            count = 0
            for synset1 in wordFromList1:
                for synset2 in wordFromList2:
                    temp = synset1.wup_similarity(synset2)
                    if temp:
                        s += temp
                        count += 1
            if count == 0:
                s = -1
            else:
                s = s/count
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

def get_word_from_glove(word,Main_dictionary,Main_glove,dictionary,glove):
    if(word in Main_dictionary):
        X_line = Main_glove[Main_dictionary[word]]
        X_vector = [float(num) for num in X_line[1:301]]
        return X_vector
    elif(word in dictionary):
        X_line = glove[dictionary[word]]
        X_vector = [float(num) for num in X_line[1:301]]
        return X_vector
    else:
        return -1

def get_sentence_similarity(FirstSentence,SecondSentence,Main_dictionary,Main_glove,dictionary,glove_dictionary):
    # print "FirstSentence:   " , FirstSentence
    # print "SecondSentence:  " , SecondSentence
    table = string.maketrans("","")
    FirstSentence = FirstSentence.lower()
    SecondSentence = SecondSentence.lower()
    FirstSentence = FirstSentence.split(' ')
    SecondSentence = SecondSentence.split(' ')
    # print "FirstSentence:   " , FirstSentence
    # print "SecondSentence:  " , SecondSentence
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
            vector = get_word_from_glove(SecondSentence[i],Main_dictionary,Main_glove,dictionary,glove_dictionary)
            if(vector != -1 and vector !=[]):
                num+=1
                SecondSentence_vector = [SecondSentence_vector[j] + vector[j] for j in range(300)]
    if(num > 1):
        SecondSentence_vector = [SecondSentence_vector[j]/num for j in range(300)]
    else:
        print SecondSentence
    similarity = _cosine_similarity(FirstSentence_vector,SecondSentence_vector)
    #print "similarity" , similarity
    return similarity



