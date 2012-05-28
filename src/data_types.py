import hashlib
import sys
import os.path
import csv
import math
import re
import xml.dom.minidom

class Vector:
    def __init__(self, values):
        self.values = values
    
    def dump(self):
        print self.values
    
    def length(self):
        val = 0
        for x in self.values:
            x = float(x)
            val += x*x
        return math.sqrt(val)

    def mean(self):
        val = 0
        for x in self.values:
            val += float(x);
        return val/len(self.values)
 
    def median(self):
        nums = sorted(self.values)
        size = len(nums)
        midPos = size / 2

        if size % 2 == 0:
            median = (nums[midPos] + nums[midPos-1]) / 2.0
        else:
            median = nums[midPos]

        return median

    def largest(self):
        max = float("-inf")
        for x in self.values:
            num = float(x)
            if num > max:
                max = num
            
        return max

    def smallest(self):
        min = float("inf")
        for x in self.values:
            num = float(x)
            if num < min:
                min = num
            
        return min

    def standard_dev(self):
        n = len(self.values)
        m = mean()
        for a in self.values:
            a = float(a)
            std = std + (a - m)**2
        return sqrt(std / float(n-1))


class Data(object):
    def __init__(self, fn):
        self.filename = fn
        self.filetype = fn.split('.')[1]
        
class CSVData(Data):
    def __init__(self, fn):
        super(CSVData, self).__init__(fn)		  
	
    def parse_vectors(self):
        reader = csv.reader(open(self.filename, 'r'))
        self.vectors=[]

        for row in reader:
            for i, x in enumerate(row):
                if len(x)< 1:
                    x = row[i] = 0
            self.vectors.append(Vector(list(row)))

    def print_vectors(self):
        for x in self.vectors:
            x.dump()

    def largest(self, c1):
        max_val = float("-inf")
        for x in self.vectors:
            if x[c1] >= max_val:
                max_val = x[c1]

        return max_val
   
    def  smallest(self, c1):
        min_val = float("inf")
        for x in self.vectors:
            if x[c1] <= min_val:
                min_val = x[c1] 
        return min_val
   
    def mean(self, c1):
        sum = 0;
        for x in self.vectors:
            sum += x[c1]
        return sum / len(self.vectors)
   
    def median(self, c1):
        float_list = []
        for x in self.vectors:
            float_list.append(x[c1])
        float_list = sorted(float_list)

        if len(float_list) % 2 == 0:
            low_index = int(len(float_list)/2)
            avg = float_list[low_index]
            avg += float_list[low_index+1]
            return float(avg/2)
        else: 
            return float_list[len(float_list)/2]
   
    def standard_dev_column(self, c1):
        float_list = []
        for x in vectors:
            float_list.append(x[c1])
        mean = sum(float_list)/len(float_list)
        for i in range(len(float_list)):
            float_list[i] -= mean
            float_list[i] *= float_list[i]

        list_sum = sum(float_list)
        stddev = Math.sqrt(list_sum / (len(float_list)-1))

        return stddev

    def standard_dev_vector(self, i1):
        float_list = vectors[i1]
        mean = 0
       # mean = sum(float_list)/len(float_list)
        for i in range(len(float_list)):
            float_list[i] -= mean
            float_list[i] *= float_list[i]
        list_sum = sum(float_list)
        stddev = Math.sqrt(list_sum / (len(float_list)-1))

        return stddev

    def dot_product(self, i1, i2):
        dot_product = 0
        for i in range(len(vectors[i1])):
            dot_product += vectors[i1][i] * vectors[i2][i]
        return dot_product
   
    def euclidian(self, i1, i2):
        v1 = vectors[i1]
        v2 = vectors[i2]
        if len(v1) != len(v2): 
           print 'Error can not compute distance between unequal vector lengths.'
           return
        else:
           total = 0
           for i in range(len(v1)):
              val = v1[i] - v2[i]
              val = val * val
              total += val
           return Math.sqrt(total)

    def manhattan(self, i1, i2):
        v1 = self.vectors[i1]
        v2 = self.vectors[i2]
        if len(v1) != len(v2): 
           print 'Error can not compute distance between unequal vector lengths.'
           return
        else:
           total = 0
           for i in range(len(v1)):
              val = v1[i] - v2[i]
              total += val
           return total

    def pearson(self, i1, i2):
        v1 = self.vectors[i1]
        v2 = self.vectors[i2]
        mean_v1 = sum(v1)/len(v1)
        mean_v2 = sum(v2)/len(v2) 
        std_v1 = standard_dev_vector(i1)
        std_v2 = standard_dev_vector(i2)
        
        pearson_cor = 0
        for i in range(len(v1)):
            pearson_cor += ((v1[i]-mean_v1) * (v2[i]-mean_v2))/((len(v1)-1)*std_v1*std_v2)
        return pearson_cor

class ClusteringData(CSVData):
    def __init__(self, fn):
        super(ClassificationData, self).__init__(fn)	
	  
    def parse_vectors(self):
        reader = csv.reader(open(self.filename, 'r'))
        self.vectors=[]
        self.restrictions=[]

        row_ct = 0
        for row in reader:
            for i, x in enumerate(row):
                if len(x)< 1:
                    x = row[i] = 0
            
            if row_ct == 0:
                self.restrictions.append(Vector(list(row)))
            elif self.restrictions[row_ct]:
                self.vectors.append(Vector(list(row)))
            row_ct += 1

class ClassificationData(CSVData):
    def __init__(self, fn):
        super(ClassificationData, self).__init__(fn)	
	  
    def build_size_map(self):
        mdict = {}
        for i in range(len(self.domain_size)):
            mdict[self.attributes[i]] = self.domain_size[i]
        self.size_map = mdict
    
    def parse_tuples(self):
        reader = csv.reader(open(self.filename, 'r'))
        self.tuples=[]
        
        row_ct = 0
        for row in reader:
            if row_ct == 0:
                self.attributes = row
            elif row_ct == 1:
                self.domain_size = tuple(row)
            elif row_ct == 2:
                self.category = row;
            else:    
                for i, x in enumerate(row):
                    if len(x)< 1:
                        x = row[i] = -1
                    x = row[i] = int(x)
                #print tuple(row)
                self.tuples.append(tuple(row))
            row_ct += 1
        self.build_size_map()

    def parse_restr_tuples(self):
        reader = csv.reader(open(self.filename, 'r'))
        self.restr=[]
        
        row_ct = 0
        for row in reader:
            for i, x in enumerate(row):
                if len(x)< 1:
                    x = row[i] = -1
                    x = row[i] = int(x)
                self.restr.append(tuple(row))
            row_ct += 1

class TXTData(Data):
    def __init__(self, filename):
        super(TXTData, self).__init__(filename)		  
        self.words = []
        self.paragraphs = []
        self.sentences = []

    def read_document(self):
        file_in = open(self.filename, 'r')
        self.document = Document(file_in.read())

    def set_text(self, text):
        self.document = Document(text)

    def paragraph_tokenize(self):
        if len(self.paragraphs) == 0:
            self.paragraphs = self.document.text.split("\n\n")
               
        return self.paragraphs;

    def sentence_tokenize(self):
        if len(self.sentences) == 0:
            sentence_reg_exp = re.compile(r"""
                (?:(?<=[.!?])|(?<=[.!?]['"])) # Match sentances ending with .! or ?              
                (?<!  Mr\.)(?<!  Mrs\.)(?<!  Jr\.)(?<!  Dr\.)(?<!  Prof\.)(?<!  Sr\.)(?<!  \.\.\.)\s+ # Exclude things that'll break early
                """, 
                re.IGNORECASE | re.VERBOSE)
            self.sentences = sentence_reg_exp.split(self.document.text)
        return self.sentences 

    def word_tokenize(self):
        if len(self.words) == 0:
            self.words = re.findall(r"""\w+(?:')\w+|\w+(?:-)\w+|\w+""", self.document.text)
        return self.words

    def unique_word_list(self):
        if len(self.words) == 0:
            self.word_tokenize()
 
        word_set = set()
        for x in self.words:
           word_set.add(x)
        return word_set   
         
    def unique_word_frequency(self):
        if len(self.words) == 0:
            self.word_tokenize()
       
        freq_dict = dict()
        for x in self.words:
            if freq_dict.has_key(x):
                freq_dict[x] += 1
            else:
                freq_dict[x] = 1 
        return freq_dict

    def print_count_statistics(self):
        print 'Length of document in words: ', len(self.word_tokenize())
        print 'Unique words: ', len(self.unique_word_list())
        print 'Sentence count: ', len(self.sentence_tokenize())
        print 'Paragraph count: ', len(self.paragraph_tokenize())
        return

    def print_freq_statistics(self, equal, greater):
        word_dict = self.unique_word_frequency() 
        greater_flist = []
        equal_flist = []
        highest_freq = 0
        highest_freq_list = []
      
        for x in word_dict.keys():
            if word_dict[x] > highest_freq:
                highest_freq_list = []
                highest_freq_list.append(x)
                highest_freq = word_dict[x]
            if word_dict[x] == highest_freq:
                highest_freq_list.append(x)  
            if word_dict[x] > int(greater):
                greater_flist.append(x)
            if word_dict[x] == int(equal):
                equal_flist.append(x)

        print 'Highest Frequency: ', highest_freq 
        print 'Words with frequency ', highest_freq
        print highest_freq_list
        print 'Words with frequency greater than ', greater
        print greater_flist
        print 'Words with frequency equal to ', equal
        print equal_flist
        return

    def word_search(self, word):
        word_dict = self.unique_word_frequency() 
        return word_dict.has_key(word)

class Data(object):
    def __init__(self, fn):
        self.filename = fn
        self.filetype = fn.split('.')[1]
        
class CSVData(Data):
    def __init__(self, fn):
        super(CSVData, self).__init__(fn)		  
	
    def parse_vectors(self):
        reader = csv.reader(open(self.filename, 'r'))
        self.vectors=[]


class XMLData(Data):
    def __init__(self, filename):
        super(XMLData, self).__init__(filename)
        self.document = []
        self.read_file()
    
    def read_file(self):
        file_in = open(self.filename, 'r')
        self.document = Document(file_in.read())
        file_in.close()

    def parse_file(self):
        self.xml = xml.dom.minidom.parseString(self.document.text)

class IRData(XMLData):
    def __init__(self, filename):
        super(IRData, self).__init__(filename)		  
        self.stopwords = ['i', 'you', 'they', 'them', 'his', 'do', 'be', 'am',
                            'are', 'have', 'had', 'in', 'onto', 'and', 'or', 'of',
                            'from', 'a', '&quot']
        self.ir_docs = []
        self.ir_md5 = []
        self.parse_file()

    def parse_docs(self):
        return None

    def remove_stop_words(self):
        for doc in self.ir_docs:
            doc.word_tokenize();
            for word in doc.words:
                if word.lower() in self.stopwords:
                    doc.words.remove(word)

class JokerData(IRData):
    def __init__(self, filename):
        super(JokerData, self).__init__(filename)		  
        self.parse_docs()
         
    def parse_docs(self):
        tjokes = []
        tmd5s  = []

        for joke in self.xml.getElementsByTagName('joke'):
            ntxt = TXTData("no.fn")
            ntxt.set_text(joke.toxml().replace('<joke>','').replace('</joke',''))
            tjokes.append(ntxt)
            tmd5s.append( int(hashlib.md5(ntxt.document.text).hexdigest(), 16) )
            
        self.ir_md5s = tmd5s
        self.ir_docs = tjokes
        self.remove_stop_words() 

class Document:
    def __init__(self, text):
        self.text = text
        self.word_count = -1 
        self.paragraph_count = -1
        self.sentence_count = -1

