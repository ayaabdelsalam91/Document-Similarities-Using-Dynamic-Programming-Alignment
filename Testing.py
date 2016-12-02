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

	
def DocToDoc_Similarity(text,categories):
	result=[]
	
	count=0
	for example in text:
		max=0
		output=0
		for i in range(0, len(categories) ):
			count+=1
			print count
			index = randint(i*50, i*50+49)
			DPResult= DP(example,text[index])
			if(DPResult>max):
				max = DPResult
				output=i
		result.append(categories[output])
	return result

def DP(Doc1,Doc2):
    p_gap = -0.5
    tic = time.time()
    s1 = Doc1
    s2 = Doc2
    s1 = s1.lower()
    s2 = s2.lower()
    s1 = s1.split(' ')
    s2 = s2.split(' ')
    len1 = len(s1)+1
    len2 = len(s2)+1
    table = numpy.zeros([len1, len2])
    print len1, len2
    
    for i in range(len2):
        table[0, i] = i*p_gap;
    for i in range(len1):
        table[i, 0] = i*p_gap;

    for i in range(1, len1):
        for j in range(1, len2):
            score1 = table[i, j-1] + p_gap
            tic = time.time()
            score2 = table[i-1, j-1]+get_similarity_from_glove(s1[i-1], s2[j-1], glove, dictionary)
            toc = time.time()

            print ("time for glove similarity: %r" % (toc-tic))
            score3 = table[i-1, j] + p_gap
            table[i, j] = max(score1, score2, score3)

    score = table[len1-1, len2-1]
    toc = time.time()

    print('Processing time: %r'
           % (toc - tic))
    return score
	# return global_alignment(Doc1, Doc2, get_similarity_from_glove, glove, dictionary, p_gap)

def eval(actual,test):
    total = len(actual)
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
		global dictionary 
		dictionary = read_dictionary(dic)
		global glove
		glove = read_glove(_glove)
		label ,  text = read_data(test)
		print len(text)
		tic = time.time()

		categories = ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast']
		result = DocToDoc_Similarity(text,categories)


		#testing
		categories = ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast']
		result = DocToDoc_Similarity(text,categories)

		toc = time.time()
		print('Processing time: %r'
           % (toc - tic))
		eval(label,result)

		#print result
		#dic=sys.argv[2]
# def get_testData(input):

# randint(0, 49)