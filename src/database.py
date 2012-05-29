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

       # row = self.cursor.fetchone()
       # print int(row[0])  
       # if int(row[0]) == 1:
       #     return True 
       # else: 

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
                txt.set_words(row[2]) 
                ndict[row[0]] = txt 
            data.set_docs(ndict)
            return data 

    def persist_docs(self, data):
        if self.connected == False:
            print "Error can not persist docs, there is no active database connection"
            return
        else:
            for key, value in data.docs.iteritems():
                data_tuple = (key, value.document.text, value.words)
                words = ""
                for word in value.words:
                    words += word 
                    words += " "
    
                print "\n\n\n"
                print key
                print value.document.text
                print words, "\n\n\n"
                #self.cursor.execute("INSERT INTO documents(id, text, words)  values(%s, %s, %s)",
                #                    data_tuple)
   
 
class ElectionDatabase:

    def __init__(self):
        self.db = 0

    def connect(self):
        self.db = MySQLdb.connect(host="external-db.s123655.gridserver.com",
                                  port=3306, 
                                  user="db123655_cpe466", 
                                  passwd="466cpe466", 
                                  db="db123655_466")
        self.cursor = self.db.cursor()

    def insert_row_num(self, data_tuple):
        self.cursor.execute("INSERT INTO election_data_num(id, party, ideology, race, gender, religion, income, education, age, region, bush_approval, vote)  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             data_tuple)      

    def data_slice(self, attribute, att_range):
        print attribute
        print att_range

        slices = {} 
        s = []
        for i in range(int(att_range)):
            index = i+1
            statment = "SELECT * FROM election_data_num WHERE party = " + str(index)        
            self.cursor.execute(statment)        
            rows = self.cursor.fetchall()
            slices[index] = rows
            print "dictionary: ", slices
            return slices
            #s.append()
            #s.append(rows)
            #print "dictionary: ", slices
       
    def is_homogeneous(self, data):
        first = data[0] 
        for d in data:
            if (d != first):
                return False
        return True
        """category = str(category).lower()
        print category
        statment = "SELECT COUNT(DISTINCT %s) FROM election_data_num WHERE %s = %s"  
        self.cursor.execute(statment, category, attr, val)

        
        row = self.cursor.fetchone()
        print int(row[0])  
        if int(row[0]) == 1:
            return True 
        else: 
            return False 
        """

    def clean_up_nums(self):
        statment = "truncate table election_data_num"  
        self.cursor.execute(statment)

