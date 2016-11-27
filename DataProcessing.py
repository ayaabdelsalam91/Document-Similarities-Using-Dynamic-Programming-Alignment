import nltk 
import sys
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
    train_input=sys.argv[1]
	train_output=sys.argv[2]
	test_input = sys.argv[3]
	test_output = sys.argv[4]
    create_dataset(train_input,train_output,400)
    labelsTrain = read_dataset(train_output)
    print labelsTrain
    create_dataset(test_input,test_output,50)
    labelsTest = read_dataset(test_output)
    print labelsTest