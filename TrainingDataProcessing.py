import sys
def bag_of_words(path):
	file = open(path, "r")
	BOW = dict()
	unqiue_count=0
	for line in file:
		words = line.split()
		for word in words:
			if word in BOW:
				BOW[word] += 1
			else:
				BOW[word] = 1
				unqiue_count+=1

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
			out_file.write(line)


if __name__ == "__main__":
		glove=sys.argv[1]
		dic=sys.argv[2]
		train=sys.argv[3]
		test=sys.argv[4]
		train_glove  =sys.argv[5]
		#create_dictionary(glove,dic)
		dictionary = read_dictionary(dic)
		BOW1,count= bag_of_words(train)
		create_training_glove(BOW1,glove,train_glove) 
		#BOW2,count= bag_of_words(test)
		#print count
		#unknown ,  unknown_count= get_unknown_words(BOW2,dictionary)
		#print unknown_count
		#print unknown
        #bag_of_words(path)