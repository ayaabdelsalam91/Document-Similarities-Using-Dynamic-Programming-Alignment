import sys
from Similarity import *
from local import *
from TrainingDataProcessing import *
from random import *
# import glob
import time

def read_data(input):
	in_file = open(input, "r")
	texts = []
	labels = []
	for i,example in enumerate(in_file):
		label, text = example.strip().split('\t')
		texts.append(text)
		labels.append(label)
	return labels,texts
	in_file.close()

def read_data_random(input):
    f = open(input)
    texts = []
    for line in f:
        if line.strip() != '':
            texts.append(line.strip())
    f.close()
    return texts

def DocToDoc_Similarity_Concatenate(text, remove_stopword_flag, alignment_type_flag, similarity_type, two_glove_flag):
    result = []
    example_num = len(text)/2
    print 'Document_num =', example_num
    for i in range(example_num):
        example = text[2*i]
        print 'Doc #', (i+1)
        sampled = [2*i+1]
        for num in range(4):
            temp = randint(0, len(text)-1)
            while(temp == 2*i or temp == 2*i+1):
                temp = randint(0, len(text)-1)
            sampled.append(temp)
        for idx, j in enumerate(sampled):
            print j,
            if(alignment_type_flag == '1'):
                if Debug: print "global"  
                DPResult= global_alignment(example,text[j],remove_stopword_flag,similarity_type,two_glove_flag)
            else:
                if Debug: print "local"
                DPResult=local_alignment(example,text[j], 0, remove_stopword_flag,similarity_type,two_glove_flag)
            if (idx == 0):
                current_max = DPResult
                current_idx = j
            elif(DPResult>current_max):
                current_max = DPResult
                current_idx = j
        result.append(current_idx)
        print 'predicted:', current_idx
    return result


def local_alignment(s1, s2, p_gap , remove_stopword_flag,similarity_type , two_glove_flag):
    # tic = time.time()
    s1 = s1.lower()
    s2 = s2.lower()
    # len1 = len(s1)+1
    # len2 = len(s2)+1
    # # print len1, len2
    s1 = s1.split(' ')
    s2 = s2.split(' ')
    if(remove_stopword_flag):
        if Debug: print "remove_stopword_flag"
        s1 = removeStopwords(s1,Stopwords)
        s2 = removeStopwords(s2,Stopwords)
    len1 = len(s1)+1
    len2 = len(s2)+1

    table = numpy.zeros([len1, len2])
    Gaptimes=0
    Dtimes = 0

    for i in range(1, len1):
        for j in range(1, len2):
            score1 = table[i, j-1] + p_gap
            if(similarity_type == '1'):
                if Debug: print "glove"
                if(two_glove_flag):
                    if Debug: print "2 glove"
                    score2 =table[i-1, j-1] +  normalized (-1,1,-10,10,get_similarity_from_glove(s1[i-1], s2[j-1], dictionary,glove,secondary_dictionary,secondary_glove))
                else:
                    if Debug: print "1 glove"
                    score2 =   table[i-1, j-1]+ normalized (-1,1,-10,10,get_similarity_from_glove(s1[i-1], s2[j-1], dictionary,glove))
            else:
                if Debug: print "wordnet"
                wordnet_score  = get_similarity_from_wordnet(s1[i-1], s2[j-1])
                if wordnet_score == -1 : 
                    wordnet_score = 0
                score2 = table[i-1, j-1]+normalized (0,1,-10,10,wordnet_score)

            score4  = 0
            score3 = table[i-1, j] + p_gap
            table[i, j] = max(score1, score2, score3 , score4)
            if(table[i, j] ==score4):
                Dtimes+=1
            else:
                Gaptimes+=1
    print "Dtimes, Gaptimes : " , Dtimes, Gaptimes
    score = table.max()
    # toc = time.time()
    # print('Processing time: %r'
    #        % (toc - tic))

    return score

def global_alignment(s1,s2,remove_stopword_flag,similarity_type , two_glove_flag):
    p_gap = 0
    # tic = time.time()
    s1 = s1.lower()
    s2 = s2.lower()
    # len1 = len(s1)+1
    # len2 = len(s2)+1
    # # print len1, len2
    s1 = s1.split(' ')
    s2 = s2.split(' ')
    if(remove_stopword_flag):
        if Debug: print "remove_stopword_flag"
        s1 = removeStopwords(s1,Stopwords)
        s2 = removeStopwords(s2,Stopwords)
    else:
    	if Debug: print "dont remove_stopword_flag" 
    len1 = len(s1)+1
    len2 = len(s2)+1
    table = numpy.zeros([len1, len2])
    # print len1, len2
    
    for i in range(len2):
        table[0, i] = i*p_gap;
    for i in range(len1):
        table[i, 0] = i*p_gap;
    # Gaptimes=0
    # Dtimes = 0
    for i in range(1, len1):
        for j in range(1, len2):
            score1 = table[i, j-1] + p_gap  
            # tic = time.time()
            if(similarity_type == '1'):
                if Debug: print "glove"
                if(two_glove_flag):
                    if Debug: print "2 glove"
                    score2 = table[i-1, j-1]+normalized (-1,1,-10,10,get_similarity_from_glove(s1[i-1], s2[j-1], dictionary,glove,secondary_dictionary,secondary_glove))
                else:
                    if Debug: print "1 glove"
                    score2 = table[i-1, j-1]+normalized (-1,1,-10,10,get_similarity_from_glove(s1[i-1], s2[j-1], dictionary,glove))
            else:
                if Debug: print "wordnet"
                wordnet_score  = get_similarity_from_wordnet(s1[i-1], s2[j-1])
                if wordnet_score == -1 : 
                    wordnet_score = 0
                score2 = table[i-1, j-1]+normalized (0,1,-10,10,wordnet_score)
            # toc = time.time()
            #print ("time for glove similarity: %r" % (toc-tic))
            score3 = table[i-1, j] + p_gap
            table[i, j] = max(score1, score2, score3)
    #         if(table[i, j] ==score2 ):
    #           Dtimes+=1
    #         else:
    #           Gaptimes+=1


    # print "Dtimes, Gaptimes : " , Dtimes, Gaptimes
    score = table[len1-1, len2-1]
    # toc = time.time()

    # print('Processing time: %r'
    #        % (toc - tic))
    return score
    # return global_alignment(Doc1, Doc2, get_similarity_from_glove, glove, dictionary, p_gap)


def eval(actual,test):
    print test
    total = len(test)
    print total
    correct = 0
    for i in range(total):
     	 if actual[i] == test[i]:
        	correct += 1
                                
    print "%f%% (%d/%d)" % (float(correct)/total*100, correct, total)

if __name__ == "__main__":
    global Stopwords
    global dictionary 
    global secondary_dictionary
    global glove
    global secondary_glove
    global Debug
    #Debug = True
    Debug = False

    test = raw_input('Enter test path: ')
    alignment_type_flag =raw_input('Type 1 for global_alignment and 2 for local_alignment: ')
    similarity_type = raw_input('Type 1 for glove and 2 for wordnet: ')
    if similarity_type == '1':
        dic = raw_input('Enter dictionary path: ')
        _glove = raw_input('Enter glove path: ')
        double_glove_flag =  raw_input('Type True is you will be using 2 gloves: ')
        if(double_glove_flag== 'True'):
        	double_glove_flag =  True
        	dic2=raw_input('Enter second dictionary path: ')
        	_glove2= raw_input('Enter second glove path: ')
        	secondary_dictionary =  read_dictionary(dic2)
        	secondary_glove = read_glove(_glove2)
        else:
        	double_glove_flag = False
    remove_stopword_flag =raw_input('Type True is you will be want to remove stopwords: ')
    if(remove_stopword_flag == 'True'):
    	remove_stopword_flag = True
    	Stopwords = read_dictionary("Stopwords.txt")
    else:
    	remove_stopword_flag = False
    

    # test=sys.argv[1]
    # dic=sys.argv[2]
    # _glove=sys.argv[3]
    # dic2=sys.argv[4]
    # _glove2=sys.argv[5]
    # remove_stopword_flag =sys.argv[6] 
    # categories_flag =  sys.argv[7]
    # double_glove_flag = sys.argv[8]
    # alignment_type_flag = sys.argv[9]
    # similarity_type = sys.argv[10]


    if similarity_type != '1':
        dictionary = None
        glove = None
        double_glove_flag = False
    else:
        dictionary = read_dictionary(dic)
        glove = read_glove(_glove)
    # label, text = read_data(test)
    text = read_data_random(test)

    tic = time.time()
    # result = DocToDoc_Similarity(label,text,categories,remove_stopword_flag,alignment_type_flag ,similarity_type , double_glove_flag)
    result = DocToDoc_Similarity_Concatenate(text,remove_stopword_flag,alignment_type_flag ,similarity_type , double_glove_flag)
    correct_answer = range(1, len(text), 2)


    toc = time.time()
    print('Processing time: %r'
       % (toc - tic))
    # eval(label,result)
    eval(correct_answer, result)
    print 'configuration: alignment', alignment_type_flag, 'similarity', similarity_type
		