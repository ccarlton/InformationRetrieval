from porter import PorterStemmer
from data_types import JokerData
import sys

class Info:
    def __init__(self, cluster_data):
        self.data = cluster_data

def main():
    if len(sys.argv) != 3:
        print "Usage: python ir.py <datafile.xml> <stopwords.xml>"
        return    
   
    data = JokerData(sys.argv[1]) 
    stemmer = PorterStemmer()

    jokes = data.ir_docs 
    for doc in data.ir_docs:
        stemmed_words = []
        for word in doc.words:
            stemmed_words.append(stemmer.stem(word, 0, len(word)-1))
        doc.words = stemmed_words

#    print len(jokes)    
#    print len(jokes[0].words)
#    print jokes[0].words
#    print jokes[0]

if __name__ == '__main__':
    main()
