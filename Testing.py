import sys
from Similarity import *
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

	
def DocToDoc_Similarity(label,text,categories):
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
			DPResult= DP(example,text[index])
			if(i==0):
				# indexx = index
				max = DPResult
				# print "awel mara" , max  , index , label[index]
			elif(DPResult>max):
				# indexofchoosen = index
				max = DPResult
				# print "Max at3'yar"  , max , i , index , label[index]
				output=i
		# if(output != 0):
		# 	print "Example : " , example
		# 	print "Right answer: "  , text[indexx]
		# 	print "Choosen answer: "  , text[indexofchoosen]

		result.append(categories[output])
		# if(count==50):
		# 	break
	return result

def removeStopwords(sentence):
	output=[]
	for word in sentence:
		if word not in Stopwords:
			output.append(word)
	return output

def DP(Doc1,Doc2):
    p_gap = 0
    # tic = time.time()
    s1 = Doc1
    s2 = Doc2
    s1 = s1.lower()
    s2 = s2.lower()
    # len1 = len(s1)+1
    # len2 = len(s2)+1
    # # print len1, len2
    s1 = s1.split(' ')
    s2 = s2.split(' ')
    s1 = removeStopwords(s1)
    s2 = removeStopwords(s2)
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
            score2 = table[i-1, j-1]+normalized (-1,1,-10,10,get_similarity_from_glove(s1[i-1], s2[j-1], dictionary,glove))
            # toc = time.time()
            #print ("time for glove similarity: %r" % (toc-tic))
            score3 = table[i-1, j] + p_gap
            table[i, j] = max(score1, score2, score3)
    #         if(table[i, j] ==score2 ):
    #         	Dtimes+=1
    #         else:
    #         	Gaptimes+=1


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
		test=sys.argv[1]
		dic=sys.argv[2]
		_glove=sys.argv[3]
		global Stopwords
		Stopwords = read_dictionary("Stopwords.txt")
		BOW , unq = bag_of_words(test)
		print unq

		global dictionary 
		dictionary = read_dictionary(dic)
		global glove
		unk , c =  get_unknown_words(BOW,dictionary)
		print unk
		print c
		glove = read_glove(_glove)
		label ,  text = read_data(test)
		tic = time.time()
		#categories = ['earn', 'money-fx', 'trade', 'acq','crude']
		categories = ['project', 'course', 'student','faculty']
		#categories= ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast']
		result = DocToDoc_Similarity(label,text,categories)
		# print DP(text[10],text [8])
		# print DP(text [10],text [100])

		toc = time.time()
		print('Processing time: %r'
           % (toc - tic))
		eval(label,result)

		#print result
		#dic=sys.argv[2]
# def get_testData(input):

# randint(0, 49)