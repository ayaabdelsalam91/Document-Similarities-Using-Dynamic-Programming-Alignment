import sys
import math
from nltk.corpus import wordnet
from TrainingDataProcessing import *
import time
import numpy
import string


if __name__ == "__main__":
    wordFromList1 = wordnet.synsets("cat")
    print wordFromList1[1]
    wordFromList2 = wordnet.synsets("dog")
    print wordFromList2[1]
    s  = wordFromList1[0].wup_similarity(wordFromList2[0])
    print s
    wordFromList1 = wordnet.synsets("panda")
    print wordFromList1[1]

    wordFromList2 = wordnet.synsets("pizza")
    print wordFromList2[0]
    s  = wordFromList1[0].wup_similarity(wordFromList2[0])
    print s


