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
        
        for word in query.split(' '):
            doc_ct = 0
            for data2 in self.data:
                for key2, value2 in data2.docs.iteritems():
                    for word2 in value2.words:
                        if word2 == word:
                            doc_ct += 1
                            break
            if doc_ct == 0:
                idf_dict[word] = 0
            else:
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
        self.db.persist_docs(data)
       

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

    def do_sim(self, docID1, docID2):
        doc1 = 0
        doc2 = 0
        for dfile in self.data:
            for key, value in dfile.docs.iteritems():
                if key == docID1:
                    doc1 = value
                elif key == docID2: 
                    doc2 = value

        if doc1 == 0 or doc2 == 0:
            print "Error invalid docID"
            return    
            
        doc1_wgts = doc1.tf_idf()
        doc2_wgts = doc2.tf_idf()
        
        sim = 0
        for key1, value1 in doc1_wgts.iteritems():
            for key2, value2 in doc2_wgts.iteritems():
                if key2 == key1:
                    sim += value1
                    sim += value2        
        print "Sim: ", sim
        return sim

    def do_search(self, query):
        tfs  = self.calculate_query_tf(query)
        idfs = self.calculate_query_idf(query)
        tf_idfs = {}

        for key, value in tfs.iteritems():
            tf_idfs[key] = value * idfs[key]

        sims = {} 
        for dfile in self.data:
            for key, value in dfile.docs.iteritems():
                sims[key] = self.query_similarity(tf_idfs, value)

        sorted_sims = sorted(sims.iteritems(), key=operator.itemgetter(1), reverse=True)
        for pair in sorted_sims:
            if pair[1] > 0:
                print "    ", pair[0], ":", pair[1] 

    def do_search_doc(self, docid):
        sims = {}
        for dfile in self.data:
            for key, value in dfile.docs.iteritems():
                sims[key] = self.do_sim(docid, key)    
     
        sorted_sims = sorted(sims.iteritems(), key=operator.itemgetter(1), reverse=True)
        print "Most relevant documents:"
        for pair in sorted_sims:
            if pair[1] > 0:
                print "    ", pair[0], ":", pair[1] 


    def query_similarity(self, query_wgt, doc):
        doc_wgts = doc.tf_idf()
        sim = 0

        for key, value in query_wgt.iteritems():
            if doc_wgts.has_key(key):
                sim += doc_wgts[key]
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
            if not values.has_key(current_opt[0].lower()):
                continue
            
            func = values[current_opt[0].lower()]

            if current_opt[0] == 'quit':
               return 
            elif current_opt[0] == 'search' and "\"" in choice: 
                cs = choice.split('"')
                func(cs[1])
            elif len(current_opt) == 3:
                func(current_opt[1], current_opt[2])
            elif len(current_opt) == 2:
                func(current_opt[1])
            elif len(current_opt) == 1: 
                func()

    def show_menu(self):
        print "Document Collection Options:\n   -CLEAR\n   -PRINT <docID>\n   -SHOW <docID>\n   -READ <filename>\n   -READ_LIST <list>\n   -SIM    <docID> <docID>\n   -SEARCH_DOC <docID>\n   -SEARCH <query>\n   -QUIT"

def main():
    if len(sys.argv) != 1:
        print "Usage: python ir.py"
        return    
  
    infosys = InfoRetrieval()
    infosys.restore_persisted_state()
    infosys.show_consol()    

if __name__ == '__main__':
    main()
