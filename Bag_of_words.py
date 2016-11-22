import sys
def bag_of_words(path):
	file = open(path, "r")
	BOW = dict()
	for line in file:
		words = line.split()
		for word in words:
			if word in BOW:
				BOW[word] += 1
			else:
				BOW[word] = 1

	print BOW


if __name__ == "__main__":
        path=sys.argv[1]
        bag_of_words(path)