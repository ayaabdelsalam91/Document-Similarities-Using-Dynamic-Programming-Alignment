import sys
from Similarity import *
from TrainingDataProcessing import *
from random import *
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

	
def DocToDoc_Similarity(text):
	result=[]
	categories = ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast']
	for example in text:
		max=0
		output=0
		for i in range(0, 5):
			index = randint(i*50, i*50+49)
			DPResult= DP(example,text[index])
			if(DPResult>max):
				max = DPResult
				output=i
		result.append(categories[output])
	return result

def DP(Doc1,Doc2):
	return random()

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
		label ,  text = read_data(test)
		print len(text)
		result = DocToDoc_Similarity(text)
		eval(label,result)
		#print result
		#dic=sys.argv[2]
# def get_testData(input):

# randint(0, 49)