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
   
    jokes = data.get_jokes()

    print len(jokes)    
    print len(jokes[0].words)
    print jokes[0].words
    print jokes[0]

if __name__ == '__main__':
    main()
