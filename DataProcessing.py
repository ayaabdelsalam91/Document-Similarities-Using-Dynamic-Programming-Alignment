import nltk 
import sys
def create_dataset(input,output,count,average,categories):
	in_file = open(input, "r")
	out_file = open(output, "w")
	
	for example in in_file:
		label, text = example.strip().split('\t')
		if(label in categories):
			if(categories[label]<count and len(text) > average/2 and len(text) <  average + average/2):
				categories[label]+=1
				#print example
				out_file.write(example)

	in_file.close()
	out_file.close()

def read_dataset(input):
	file = open(input, "r")
	labels = dict()
	for example in file:
		#print example
		label, text = example.strip().split('\t')
		if label in labels:
			labels[label] += 1
		else:
			labels[label] = 1
	return (labels)

def get_average_size(input):
	in_file = open(input, "r")
	total_number=0
	total_size= 0
	for example in in_file:
		label, text = example.strip().split('\t')
		total_number+=1
		total_size+= len(text)
	return total_size/total_number





if __name__ == "__main__":
    
    # reading, tokenizing, and normalizing data
    test_input=sys.argv[1]
	#train_output=sys.argv[2]
	# test_input = sys.argv[3]
    test_output = sys.argv[2]
    #categories= dict.fromkeys( ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast'] , 0 )
    #categories= dict.fromkeys( ['project', 'course', 'student', 'sci.crypt','faculty'] , 0 )
    categories= dict.fromkeys( ['earn', 'money-fx', 'trade', 'acq','crude'] , 0 )

    #{'earn': 1083, 'money-fx': 87, 'trade': 75, 'acq': 696, 'grain': 10, 'interest': 81, 'crude': 121, 'ship': 36}
    #{'earn': 2840, 'money-fx': 206, 'trade': 251, 'acq': 1596,  'crude': 253, 'ship': 108}
 #    create_dataset(train_input,train_output,400)
 #    labelsTrain = read_dataset(train_output)
 #    print labelsTrain
    create_dataset(test_input,test_output,50,1000,categories)
    labels  = read_dataset(test_output)
    avg  = get_average_size(test_output )
    print labels
    print avg


	#labelsTest = read_dataset(test_output)
	#print labelsTest