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

def rearrange_dataset(input,output,categories):
	
	
	out_file = open(output, "w")
	outCategories = []
	for i in range (0,len(categories)):
		#print categories[i]
		in_file = open(input, "r")
		for example in in_file:
			label, text = example.strip().split('\t')
			#print categories[i] , label
			if(label==categories[i]):
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
	#test_input = sys.argv[3]
    test_output = sys.argv[2]
    #categories= dict.fromkeys( ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast'] , 0 )
    #categories= dict.fromkeys( ['project', 'course', 'student','faculty'] , 0 )
    #categories= dict.fromkeys( ['earn', 'money-fx', 'trade', 'acq','crude'] , 0 )
    categories= ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast']
    rearrange_dataset(test_input,test_output,categories)
	# test_input = sys.argv[3]
    test_output = sys.argv[2]
    #categories= dict.fromkeys( ['comp.graphics', 'sci.med', 'soc.religion.christian', 'sci.crypt','talk.politics.mideast'] , 0 )
    #categories= dict.fromkeys( ['project', 'course', 'student', 'sci.crypt','faculty'] , 0 )
    categories= dict.fromkeys( ['earn', 'money-fx', 'trade', 'acq','crude'] , 0 )
    #testing 2
    #create_dataset(test_input,test_output,50,500,categories)
    labels  = read_dataset(test_output)
    avg  = get_average_size(test_output )
    print labels
    #print avg
    create_dataset(test_input,test_output,50,1000,categories)
    labels  = read_dataset(test_output)
    avg  = get_average_size(test_output )
    print labels
    print avg



	#labelsTest = read_dataset(test_output)
	#print labelsTest
