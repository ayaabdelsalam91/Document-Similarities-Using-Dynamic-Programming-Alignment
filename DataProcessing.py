import nltk 
def create_dataset(input,output,count):
	in_file = open(input, "r")
	out_file = open(output, "w")
	categories= dict.fromkeys( ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast'] , 0 )
	for example in in_file:
		label, text = example.strip().split('\t')
		if(label in categories):
			if(categories[label]<count):
				categories[label]+=1
				out_file.write(example)
	in_file.close()
	out_file.close()

def read_dataset(input):
	file = open(input, "r")
	labels = dict()
	for example in file:
		label, text = example.strip().split('\t')
		if label in labels:
			labels[label] += 1
		else:
			labels[label] = 1
	return (labels)





if __name__ == "__main__":
    # reading, tokenizing, and normalizing data
    create_dataset('/Users/aya/Documents/CMSC701/Project/Document-Similarities-Using-Dynamic-Programming-Alignment/datasets/20ng-train-all-terms.txt','/Users/aya/Documents/CMSC701/Project/Document-Similarities-Using-Dynamic-Programming-Alignment/train.txt',400)
    labelsTrain = read_dataset('/Users/aya/Documents/CMSC701/Project/Document-Similarities-Using-Dynamic-Programming-Alignment/train.txt')
    print labelsTrain
    create_dataset('/Users/aya/Documents/CMSC701/Project/Document-Similarities-Using-Dynamic-Programming-Alignment/datasets/20ng-test-all-terms.txt','/Users/aya/Documents/CMSC701/Project/Document-Similarities-Using-Dynamic-Programming-Alignment/test.txt',50)
    labelsTrain = read_dataset('/Users/aya/Documents/CMSC701/Project/Document-Similarities-Using-Dynamic-Programming-Alignment/test.txt')
    print labelsTrain