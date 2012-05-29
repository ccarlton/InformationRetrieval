from porter import PorterStemmer
from data_types import JokerData
from database import JokerDatabase
import operator
import math
import _mysql
import sys

class InfoRetrieval:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.data = []
        self.db = JokerDatabase()
        self.db.connect()
        self.total_docs = 0

    def restore_persisted_state(self):
        state = self.db.restore_state()

        self.total_docs = len(state.docs)
        
        self.data.append(state)
        self.calculate_idfs(state)

 
    def stem_words(self, data):
        for key, value in data.docs.iteritems():
            stemmed_words = []
            for word in value.words:
                stemmed_words.append(self.stemmer.stem(word, 0, len(word)-1))
            value.words = stemmed_words

    def calculate_query_idf(self, query):
        idf_dict = {}
        total = self.total_docs
        print "Total docs:  ", total
        for word in query.split(' '):
            doc_ct = 0
            for data2 in self.data:
                for key2, value2 in data2.docs.iteritems():
                    for word2 in value2.words:
                        if word2 == word:
                            doc_ct += 1
                            break
            idf_dict[word] = float(math.log((int(total)/int(doc_ct)), 2))
        return idf_dict

    def calculate_query_tf(self, query):
        freq_dict = {}
        tf_dict = {}
        total_words = len(query.split(' '))

        for word in query.split(' '):
            freq_dict[word] = 0
 
        for word in query.split(' '):
            freq_dict[word] += 1
        
        for key, value in freq_dict.iteritems():
            freq_dict[key] = value / total_words

        return freq_dict 

    def calculate_idfs(self, data):
        total = self.total_docs
        
        for key1, value1 in data.docs.iteritems():
            for word1 in value1.words:
                doc_ct = 0
                for data2 in self.data:
                    for key2, value2 in data2.docs.iteritems():
                        for word2 in value2.words:
                            if word2 == word1:
                                doc_ct += 1
                                break

                print "Found ", word1, " with an df of " , doc_ct, "/", total
                value1.terms_idf[word1] = math.log10(int(total)/int(doc_ct))

    def do_clear(self):
        for dfile in self.data:
            for key in dfile.docs.iterkeys():
                self.db.remove_id(key)

    def do_print(self, docid):
        found = False
        for dfile in self.data:
            if dfile.docs.has_key(str(docid)):
                found = True
                print dfile.docs[str(docid)].document.text
                #print dfile.docs[str(docid)].words

        if found == False:
            print "Document not found."

    def do_read(self, filename):
        data = JokerData(filename) 
        data.parse_docs()

        self.stem_words(data)
        self.data.append(data)
        
        count = 0 
        for dfile in self.data:
           for doc in dfile.docs:
               count += 1
        self.total_docs = count
 
        self.calculate_idfs(data)
          #self.db.persist_docs(data)
       

    def do_list(self):
        index = 0
        for dfile in self.data:
            print index, ":", dfile.filename
            for key in dfile.docs.iterkeys():
                print "    ", key 

    def do_show(self, docid):
        found = False
        for dfile in self.data:
            if dfile.docs.has_key(str(docid)):
                found = True
                print "\nWords:"
                print dfile.docs[str(docid)].words
                print "\nTerm Freqs:"
                print dfile.docs[str(docid)].terms_freq
                print "\nIDFs:"
                print dfile.docs[str(docid)].terms_idf

        if found == False:
            print "Document not found."

    def do_sim(self):
        return None

    def do_search(self, query):
        print "DO SEARCH!!!!"
        tfs  = self.calculate_query_tf(query)
        idfs = self.calculate_query_idf(query)
        tf_idfs = {}

        for key, value in tfs.iteritems():
            tf_idfs[key] = value * idfs[key]

        sims = {} 
        for dfile in self.data:
            for key, value in dfile.docs.iteritems():
                sims[key] = self.query_similarity(tf_idfs, value)

        list_sims = [] 

        max_sim = -9999
        max_key = 0
        for key, value in sims.iteritems():
             list_sims.append(float(value))
             if float(value) >= max_sim:
                max_sim = float(value)
                max_key = key
        print "simslist: ", sorted(list_sims)

        print "Max sim: ", max_sim 
        print "Max key: ", max_key 
        
        #print "Sim: ", sim
        #print "DOC: ", doc.words 
            

    def do_search_doc(self, docid):
        return None

    def query_similarity(self, query_wgt, doc):
        doc_wgts = doc.tf_idf()
        toprow = 0
        bott1 = 0
        bott2 = 0
        bottom = 0 
        sim = 0
        #print "Query_wgt: ", query_wgt
        #print "DOC_wgt: ", doc_wgts

        for key, value in query_wgt.iteritems():
            if doc_wgts.has_key(key):
                sim += doc_wgts[key]
                #print 'doc_wgts[',key,'] = ',doc_wgts[key]
                #print 'query_wgts[',key,'] = ',query_wgt[key]

        return sim

    def do_read_list(self, lst):
        myf = open(self.filename, 'r')
        for line in myf.readlines():
            self.do_read(line)
        myf.close()

    def do_quit(self):
        return None

    def show_consol(self):
        values = {
                    'clear'     : self.do_clear,
                    'print'     : self.do_print,
                    'read'      : self.do_read,
                    'list'      : self.do_list,
                    'read_list' : self.do_read_list,
                    'show'      : self.do_show,
                    'sim'       : self.do_sim,
                    'search'    : self.do_search,
                    'search_doc': self.do_search_doc,
                    'quit'      : self.do_quit
                 }

        while True:
            self.show_menu()
            try:
                choice = sys.stdin.readline()
            except KeyboardInterrupt:
                break
            
            current_opt = choice.replace('\n', '').split(' ')
            func = values[current_opt[0].lower()]

            if current_opt[0] == 'quit':
               return 
            elif len(current_opt) == 3:
                func(current_opt[1], current_opt[2])
            elif len(current_opt) == 2:
                func(current_opt[1])
            elif len(current_opt) == 1: 
                func()

    def show_menu(self):
        print "Document Collection Options:\n   -CLEAR\n   -PRINT <docID>\n   -SHOW <docID>\n   -SIM    <docID> <docID>\n   -SEARCH DOC <docID>\n   -QUIT"

def main():
    if len(sys.argv) != 1:
        print "Usage: python ir.py"
        return    
  
    infosys = InfoRetrieval()
    infosys.restore_persisted_state()
    infosys.show_consol()    

if __name__ == '__main__':
    main()
