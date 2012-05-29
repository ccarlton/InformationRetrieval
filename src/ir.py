from porter import PorterStemmer
from data_types import JokerData
from database import JokerDatabase
import _mysql
import sys

class InfoRetrieval:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.data = []
        self.db = JokerDatabase()
        self.db.connect()

    def restore_persisted_state(self):
        state = self.db.restore_state()
        print 'State: ', state
        self.data.append(state)
 
    def stem_words(self, data):
        for key, value in data.docs.iteritems():
            stemmed_words = []
            for word in value.words:
                stemmed_words.append(self.stemmer.stem(word, 0, len(word)-1))
            value.words = stemmed_words

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
        self.db.persist_docs(data)
 
        self.data.append(data)

    def do_list(self):
        index = 0
        for dfile in self.data:
            print index, ":", dfile.filename
            for key in dfile.docs.iterkeys():
                print "    ", key 

    def do_show(self):
        return None

    def do_sim(self):
        return None

    def do_search(self):
        return None

    def do_quit(self):
        return None

    def do_read_list(self, lst):
        myf = open(self.filename, 'r')
        for line in myf.readlines():
            self.do_read(line)
        myf.close()

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
