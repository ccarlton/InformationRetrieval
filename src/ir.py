from porter import PorterStemmer
from data_types import JokerData
import sys

class InfoRetrieval:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.data = []
        self.show_consol()    
    
    def stem_words(self, index):
        for doc in self.data[index].ir_docs:
            stemmed_words = []
            for word in doc.words:
                stemmed_words.append(self.stemmer.stem(word, 0, len(word)-1))
            doc.words = stemmed_words

    def do_clear(self):
        return None

    def do_print(self, docid):
        found = False
        for dfile in self.data:
            index = 0
            for md5 in dfile.ir_md5s:
                if long(md5) == long(docid):
                    found = True
                    print "Document Found:"
                    print dfile.ir_docs[index].document.text  
                index += 1

        if found == False:
            print "Document not found."

    def do_read(self, filename):
        data = JokerData(filename) 
        self.data.append(data)

        index = len(self.data)
        self.stem_words(index-1)

    def do_list(self):
        index = 0
        for dfile in self.data:
            print index, ":", dfile.filename
            for hval in self.data[index].ir_md5s:
                print "    ",  hval
            index += 1

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
                break
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
    infosys.show_consol()    

if __name__ == '__main__':
    main()
