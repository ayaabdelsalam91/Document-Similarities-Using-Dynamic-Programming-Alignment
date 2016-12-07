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

def DocToDoc_Similarity(label, text,categories,remove_stopword_flag,alignment_type_flag,similarity_type,two_glove_flag):
	result=[]
	count=0
	for example in text:
		# indexofchoosen = 0
		max=0
		output=0
		# indexx=0
		for i in range(0, len(categories) ):
			count+=1
			print count
			index = randint(i*50, i*50+49)
			print index
			if(alignment_type_flag == '1'):
				if Debug: print "global"  
				DPResult= global_alignment(example,text[index],remove_stopword_flag,similarity_type,two_glove_flag)
			else:
				if Debug: print "local"
				DPResult=local_alignment(example,text[index], 0, remove_stopword_flag,similarity_type,two_glove_flag)
			if(i==0):
				indexx = index
				max = DPResult
				print "awel mara" , max  , index , label[index]
			elif(DPResult>max):
				indexofchoosen = index
				max = DPResult
				print "Max at3'yar"  , max , i , index , label[index]
				output=i
		if(output != 0):
			print "Example : " , example
			print "Right answer: "  , text[indexx]
			print "Choosen answer: "  , text[indexofchoosen]

		# 	# print "count kam isa? " ,  count
		# if(count > 50):
		# 	break

		result.append(categories[output])

	return result

def DocToDoc_Similarity_Random(text, categories, remove_stopword_flag, alignment_type_flag, similarity_type, two_glove_flag):
    result = []
    example_num = len(text)/4
    for i in range(example_num):
        example = text[4*i]
        for j in range(1, 4):
            if(alignment_type_flag == '1'):
                if Debug: print "global"  
                DPResult= global_alignment(example,text[4*i+j],remove_stopword_flag,similarity_type,two_glove_flag)
            else:
                if Debug: print "local"
                DPResult=local_alignment(example,text[4*i+j], 0, remove_stopword_flag,similarity_type,two_glove_flag)
            if (j == 1):
                current_max = DPResult
                current_idx = j
            elif(DPResult>current_max):
                current_max = DPResult
                current_idx = j
        result.append(4*i+current_idx)
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
					score2 = normalized (-1,1,-10,10,get_similarity_from_glove(s1[i-1], s2[j-1], dictionary,glove,secondary_dictionary,secondary_glove))
					score4 = table[i-1, j-1] +  score2
				else:
					if Debug: print "1 glove"
					score2 = normalized (-1,1,-10,10,get_similarity_from_glove(s1[i-1], s2[j-1], dictionary,glove))
					score4 = table[i-1, j-1]+ score2
			else:
				if Debug: print "wordnet"
				wordnet_score  = get_similarity_from_wordnet(s1[i-1], s2[j-1])
				if wordnet_score == -1 : 
					wordnet_score = 0
				score2 = table[i-1, j-1]+normalized (0,1,-10,10,wordnet_score)

            #score2 = table[i-1, j-1]+sim_fun(s1[i-1], s2[j-1])
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
    categories_flag  =raw_input('Type category number: ')
    print categories_flag
    alignment_type_flag =raw_input('Type 1 for global_alignment and 2 for local_alignment: ')
    similarity_type = raw_input('Type 1 for glove and 2 for wordnet: ')

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


    
    dictionary = read_dictionary(dic)
    glove = read_glove(_glove)
    label ,  text = read_data(test)
    # text = read_data_random(test)
    if(categories_flag == '1'):
    	categories= ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast']
    	print "graphics"
    elif (categories_flag == '2'):
    	categories = ['earn', 'money-fx', 'trade', 'acq','crude']
    	print "earn"
    elif (categories_flag == '3'):
        categories = ['project', 'course', 'student','faculty']
        print "project"
    else:
        categories = ['MSRpar', 'surprise.SMTnews', 'SMTeuroparl']
        print 'surprise.SMTnews'
    	

    tic = time.time()
    result = DocToDoc_Similarity(label,text,categories,remove_stopword_flag,alignment_type_flag ,similarity_type , double_glove_flag)
    # result = DocToDoc_Similarity_Random(text,categories,remove_stopword_flag,alignment_type_flag ,similarity_type , double_glove_flag)
    # correct_answer = range(1, len(text), 4)


    toc = time.time()
    print('Processing time: %r'
       % (toc - tic))
    eval(label,result)
    # eval(correct_answer, result)
		