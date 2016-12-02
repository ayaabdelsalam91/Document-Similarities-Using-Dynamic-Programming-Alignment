import sys
import math

def _cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def normalized(OldMin,OldMax,NewMin,NewMax,OldValue):
	OldRange = (OldMax - OldMin)  
	NewRange = (NewMax - NewMin)  
	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue


def bag_of_words(path):
	file = open(path, "r")
	BOW = dict()
	unqiue_count=0
	for line in file:
		words = line.split()
		for word in words:
			if(word[-1]=='.'):
				word=word[:-1]
			if word in BOW:
				BOW[word.lower()] += 1
			else:
				BOW[word.lower()] = 1
				unqiue_count+=1
	file.close()
	return BOW,unqiue_count

def create_dictionary(in_path,out_path):
	in_file = open(in_path, "r")
	out_file = open(out_path, "w")
	for line in in_file:
		words = line.split()
		out_file.write(words[0])
		out_file.write("\n")
	in_file.close()
	out_file.close()

def read_dictionary(in_path):
	_dictionary = dict()
	in_file = open(in_path, "r")
	for i,line in  enumerate(in_file):
		word = line.split()
		_dictionary[word[0]] = i
	in_file.close()
	return _dictionary

def get_unknown_words(BOW,dictionary):	
	unk=[]
	unknown_count=0
	for word in BOW:
		if(word not in dictionary):
			unk.append(word)
			unknown_count+=1
	return unk, unknown_count

def create_training_glove(BOW,in_path,out_path):
	in_file = open(in_path, "r")
	out_file = open(out_path, "w")
	for line in in_file:
		words = line.split()
		if(words[0] in BOW):
			print words[0]
			out_file.write(line)
	in_file.close()
	out_file.close()

def read_glove (input):
	glove = []
	in_file = open(input, "r")
	X = in_file.readlines()
	for i, X_line in enumerate(X):
		X_line = X_line.strip()
		X_line = X_line.split(' ')
		glove.append(X_line)
	in_file.close()
	return glove


def blosum_construction (input, output):
	in_file = open(input, "r")
	out_file = open(output, "w")
	X = in_file.readlines()
	for i, X_line in enumerate(X):
		print i
		X_line = X_line.strip()
		X_line = X_line.split(' ')
		for j, Y_line in enumerate(X):
			if(j<=i):
				Y_line = Y_line.strip()
				Y_line = Y_line.split(' ')
				X_vector = [float(num) for num in X_line[1:301]]
				Y_vector = [float(num) for num in Y_line[1:301]]
				output_line = str(_cosine_similarity( X_vector, Y_vector)) + "\t"
				out_file.write(output_line)
		out_file.write("\n")
	in_file.close()
	out_file.close()


if __name__ == "__main__":
		glove=sys.argv[1]
		blosum=sys.argv[2]
		blosum_construction (glove,blosum)
		#dic=sys.argv[2]
		#train=sys.argv[3]
		#test=sys.argv[2]
		#test_glove  =sys.argv[3]
		#create_dictionary(test_glove,dic)
		#dictionary = read_dictionary(dic)
		#BOW1,count= bag_of_words(train)
		#
		#BOW2,count= bag_of_words(test)
		#print BOW2
		#create_training_glove(BOW2,glove,test_glove) 
		#print count
		#unknown ,  unknown_count= get_unknown_words(BOW2,dictionary)
		#print unknown_count
		#print unknown
        #bag_of_words(path)