import MySQLdb
from data_types import JokerData, TXTData
class Database(object):
    def __init__(self):
        self.params_set = False
        self.host = None
        self.port = None
        self.user = None
        self.passwd = None
        self.db = None
        self.cursor = None

    def set_params(self, host, port, user, passwd, db):
        self.params_set = True
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def connect(self):
        if self.params_set == False:
            print "Error connection parameters not set"
            return None
        else:
            self.db = MySQLdb.connect(host=self.host,
                                      port=self.port, 
                                      user=self.user, 
                                      passwd=self.passwd, 
                                      db=self.db)
            self.cursor = self.db.cursor()

class IRDatabase(Database):
    def __init__(self):
        super(IRDatabase, self).__init__()
        self.connected = False
    
    def restore_state(self):
        if self.params_set == False:
            print "Error connection parameters not set"
            return None
        else:
            statment = "SELECT id, text FROM documents"
            self.cursor.execute(statment)
            rows = self.cursor.fetchall()
            ndict = {}
            
            for row in rows:
               ndict[row[0]] = row[1]
            return ndict

    def get_document_text(docID):
        if self.connected == False:
            print "Error database not connected"
            return None
        else:
            statment = "SELECT text FROM documents WHERE id = %s"
            self.cursor.execute(statment, docID)

            row = self.cursor.fetchone()
            print row

class JokerDatabase(IRDatabase):
    def __init__(self):
        super(JokerDatabase, self).__init__()
        self.set_params("external-db.s123655.gridserver.com",
                        3306,
                        "db123655_cpe466",
                        "466cpe466",
                        "db123655_466")
        
    def connect(self):
        print "Connecting to persistant data source..."
        self.db = MySQLdb.connect(host="external-db.s123655.gridserver.com",
                                  port=3306, 
                                  user="db123655_cpe466", 
                                  passwd="466cpe466", 
                                  db="db123655_466")
        self.cursor = self.db.cursor()
        print "Connected!"
        self.connected = True

    def restore_state(self):
        if self.params_set == False:
            print "Error connection parameters not set"
            return None
        else:
            statment = "SELECT id, text, words FROM documents"
            self.cursor.execute(statment)
            rows = self.cursor.fetchall()
            ndict = {}
            
            data = JokerData("no.fn")
            for row in rows:
                txt = TXTData("no.fn")
                txt.set_text(row[1])
                txt.set_words(row[2].split(' ')) 
                txt.unique_word_frequency()
                ndict[row[0]] = txt 
            data.set_docs(ndict)
            return data 

    def persist_docs(self, data):
        if self.connected == False:
            print "Error can not persist docs, there is no active database connection"
            return
        else:
            count = 0
            for key, value in data.docs.iteritems():
                words = ""
                for word in value.words:
                    words += word 
                    words += " "
                
                if self.contains_id(key) == False:
                    count += 1
                    sql2 = "INSERT into documents(id, text, words) VALUES('%s', '%s', '%s')" % \
                            (str(key), value.document.text, words) 
                    self.cursor.execute(sql2)

        print "The total number of rows persisted is ", count

    def contains_id(self, docid):
        sql = "SELECT id from documents where id = %s"
        self.cursor.execute(sql, str(docid))
        rows = self.cursor.fetchall()
        
        if len(rows) == 0:
            return False
        else: 
            return True

    def remove_id(self, docid):
        sql = "DELETE from documents where id = %s"
        self.cursor.execute(sql, str(docid))
