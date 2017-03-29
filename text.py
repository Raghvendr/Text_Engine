import os
os.chdir("C://Users//122982//Desktop//Text_Analytics")
class TextEngine(object):
    def __init__(self,data = None,url = 0,
    google_search = 0,working_directory =None):
        self.data = data
        temp = self.data
        index = temp.find('.')
        self.format = self.data[index:]
        self.directory = working_directory
        self.filename= data
        self.url = url
        self.google_search = google_search
        self.ngrams = None
    
    ## Store the data in intended form
    def store_data(self,store_format = ".xslx",html_raw =0):
        # checking the availability on pandas library
        global zipfile, re, BeautifulSoup
        try:
            import pandas as pd
        except ImportError:
            print("Pandas library is not available: Please install Pandas to run this program")
             
        # Parsing the TEXT file in to standard format
        
        if(self.format == ".txt"):
            with open(self.data, 'r') as myfile:
                string=myfile.read().replace('\n', '')
            tmp = pd.DataFrame(columns =["Index","Content"])
            tmp = tmp.append({"Index":1,"Content": string},ignore_index= True)
            self.data= tmp
        
        # Parsing the DOCX file in to standard format
        elif (self.format == '.docx'):
            try:
                import zipfile
                import re
            except ImportError:
                print("zipfile library is not available: Please install zipfile to run this program")
                print("re library is not available: Please install re to run this program")   
            docx = zipfile.ZipFile(self.data)
            content = docx.read('word/document.xml')
            string = re.sub('<(.|\n)*?>','',content)
            string = string.replace("\r\n", "")
            tmp = pd.DataFrame(columns =["Index","Content"])
            tmp = tmp.append({"Index":1,"Content": string},ignore_index= True)
            self.data= tmp
             
        # Parsing HTML file in standard  format
               
        elif (self.format == ".html"):
            try: 
                from bs4 import BeautifulSoup
            except ImportError:
                print("bs4 library is not available: Please install bs4 to run this program")
            with open(self.data, 'r') as myfile:
                string=myfile.read().replace('\n', '')
            if (html_raw ==1):
                tmp = pd.DataFrame(columns =["Index","Content"])
                tmp = tmp.append({"Index":1,"Content": string},ignore_index= True) 
            else:
                string= BeautifulSoup(string,"lxml")
                string = string.get_text()
                #string = string.encode('utf-8')
                #string = string.replace("\n",'')
                tmp = pd.DataFrame(columns =["Index","Content"])
                tmp = tmp.append({"Index":1,"Content": string},ignore_index= True)
            self.data = tmp
            
        #parsing JSON file into standard format
        
        elif (self.format ==".json"):
            try:
                import codecs
                from copy import deepcopy
                import json
            except ImportError:
                print("codecs is not available: Please install codecs to run this program")
            except ImportError:
                print("copy is not available: Please install copy to run this program")
            except ImportError:
                print("json is not available: Please install json to run this program")
            data = []
            with codecs.open(self.data,'rU','utf-8') as f:
                for line in f:
                    data.append(json.loads(line))
            data1=deepcopy(data)
            index=[]
            for i in range (0,len(data)):
                if 'text' not in data[i].keys():
                    index.append(i)
        
            for i in sorted(index, reverse=True):
                del data1[i]
            tweets=pd.DataFrame(columns=['tweet_id', 'tweet_date', 'tweet', 'followers', 'following',
                                'friends', 'favorites', 'retweets'])
    
            for i in range (0,len(data1)):    
                tweets=tweets.append({'tweet':data1[i]['text'],'tweet_id':data1[i]['user']['id']
                            ,'tweet_date':data1[i]['created_at'],
                            'followers':data1[i]['user']['followers_count'], 
                            'following':data1[i]['user']['following'],
                            'friends':data1[i]['user']['friends_count'],                           
                            'retweets':data1[i]['retweet_count']},ignore_index= True)
            self.data = tweets
        
        # parsing the EXCEL file and CSV file
        elif ( self.format == '.xlsx'):
            try:    
                import openpyxl
            except ImportError:
                print("Pandas library is not available: Please install Pandas to run this program")
            data = pd.read_excel(self.data)
            self.data = data 
        
        elif ( self.format == '.csv'):
            try:    
                import openpyxl
            except ImportError:
                print("Pandas library is not available: Please install Pandas to run this program")
            data = pd.read_csv(self.data)
            self.data = data 
            
        # Parsing the PDF file into standard format
        elif (self.format == ".pdf"):
            try:    
                import pyPdf
            except ImportError:
                print("pyPdf library is not available: Please install pyPdf to run this program")
            pdf = pyPdf.PdfFileReader(open(self.data, "rb"))
            tmp = pd.DataFrame(columns =["Page","Content"])
            
            #creating count for assigning indices
            count =0;
            for page in pdf.pages:
                count +=1
                string= page.extractText()
                string = string.encode('utf-8')
                tmp = tmp.append({"Page":count,"Content": string},ignore_index= True)
            self.data = tmp
        #  parsing the data from a url in store into text format 
        elif(self.url ==1):
            try: 
                from bs4 import BeautifulSoup
                import urllib2
                import pandas as pd
            except ImportError:
                print("bs4 library is not available: Please install bs4 to run this program")
                print("urllib2 library is not available: Please install urllib2 to run this program")
                print("pandas library is not available: Please install pandas to run this program")
            self.format = '.html'     
            page = urllib2.urlopen(self.data)
            string = BeautifulSoup(page,"lxml")
            if (html_raw ==1):
                string = string.encode('utf-8')
                string = string.replace("\n",'')
                tmp = pd.DataFrame(columns =["Index","Content"])
                tmp = tmp.append({"Index":1,"Content": string},ignore_index= True) 
            else:
                string = string.get_text()
                #string = string.encode('utf-8')
                
                tmp = pd.DataFrame(columns =["Index","Content"])
                tmp = tmp.append({"Index":1,"Content": string},ignore_index= True)
            self.data = tmp
        elif(self.google_search ==1):
            url_list = []
            try:
                import google
                import urllib2
                from bs4 import BeautifulSoup
            except ImportError:
                print("google library is not available: please install google to run this program")
                print("bs4 library is not available: Please install bs4 to run this program")
                print("urllib2 library is not available: Please install urllib2 to run this program")

            for url in google.search(self.data,num =5,stop =1):
                url = url.encode('utf-8')
                url_list.append(url)
            self.format = '.html'     
            page = urllib2.urlopen(url_list[1])
            string = BeautifulSoup(page,"lxml")
            if (html_raw ==1):
                string = string.encode('utf-8')
                string = string.replace("\n",'')
                tmp = pd.DataFrame(columns =["Index","Content"])
                tmp = tmp.append({"Index":1,"Content": string},ignore_index= True) 
            else:
                string = string.get_text()
                #string = string.encode('utf-8')
                tmp = pd.DataFrame(columns =["Index","Content"])
                tmp = tmp.append({"Index":1,"Content": string},ignore_index= True)
            self.data = tmp
        else:
            raise ValueError("This format of the data is not supported")
        
        #Returning the None to the function
        return None
            
    ## pre-processing steps 
    def html_remover(self,column=None):
        try:
            import re 
        except ImportError:
            print("re library is not available: Please install re to run this program")
        htmlcleanr= re.compile('<.*?>')
        m= self.data
        if self.format==".txt":
            for i in range(0, len(m)):
                m['Content'][i]=re.sub(htmlcleanr,'',m['Content'][i])
        elif self.format==".html":
            for i in range(0, len(m)):
                m['Content'][i]=re.sub(htmlcleanr,'',m['Content'][i])
        elif self.format==".json":
            for i in range(0, len(m)):
                m['tweet'][i]=re.sub(htmlcleanr,'',m['tweet'][i])
        elif self.format ==".xlsx":
            for i in range(0, len(m)):
                m[column][i]=re.sub(htmlcleanr,'',m[column][i])
        elif self.format ==".csv":
            for i in range(0, len(m)):
                m[column][i]=re.sub(htmlcleanr,'',m[column][i])
        else:
            raise NameError("format not supported")
            
        self.data=m
        
    def url_remover(self,column=None):
        try:
            import re 
        except ImportError:
            print("re library is not available: Please install re to run this program")
        m= self.data
        if self.format==".txt":
            for i in range(0, len(m)):
                m['Content'][i]=re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+','',m['Content'][i])
        elif self.format==".html":
            for i in range(0, len(m)):
                m['Content'][i]=re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+','',m['Content'][i])
        elif self.format==".json":
            for i in range(0, len(m)):
                m['tweet'][i]=re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+','',m['tweet'][i]) 
        elif self.format==".xlsx":
            for i in range(0, len(m)):
                m[column][i]=re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+','',m[column][i]) 
        elif self.format==".csv":
            for i in range(0, len(m)):
                m[column][i]=re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+','',m[column][i])
        else:
            raise NameError("format not support")
        self.data=m   
        
        
     ## Aanchal's code 
     
    def RT_remover(self):
        try:
            import re 
        except ImportError:
            print("re library is not available: Please install re to run this program")
        m= self.data
        RTcontent= re.compile(r'(RT @[\w]+:)', re.I )
        if self.format==".txt":
            for i in range(0, len(m)):
                m['Content'][i]=re.sub(RTcontent,'',m['Content'][i])
        elif self.format==".html":
            for i in range(0, len(m)):
                m['Content'][i]=re.sub(RTcontent,'',m['Content'][i])
        elif self.format==".json":
            for i in range(0, len(m)):
                m['tweet'][i]=re.sub(RTcontent,'',m['tweet'][i]) 
            
        self.data=m
        
    def tokenization(self,column):
        try:
            import re
            import pandas as pd 
        except ImportError:
            print("re library is not available: Please install re to run this program")
        m=self.data
        emoticons_str = r""" (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
        )"""
    
        regex_str = [emoticons_str,
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hashtags
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
        ]
        
        tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

        emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
        new=pd.DataFrame()
        for i in range(0,len(m[column])):
            tokens=tokens_re.findall(m[column][i])
            if False:
                tokens=[token if emoticon_re.search(token) else token.lower() for token in tokens]
            new=new.append({'tokens':tokens}, ignore_index=True)
            
        m=pd.concat([m,new],axis=1)
        self.data=m
    
    def punct_space_removal(self):
        m=self.data
        try:
            import string 
        except ImportError:
            print("string library is not available: Please install string to run this program")
        
        try:
            import re 
        except ImportError:
            print("re library is not available: Please install re to run this program")
        
        puncts= set(string.punctuation)
        
        
        for i in range(0, len(m['tokens'])):
            index=[]
            for j in range(0,len(m['tokens'][i])):
                if m['tokens'][i][j] in puncts:
                    index.append(j)
            for k in sorted(index, reverse=True):
                del m['tokens'][i][k]
        
        for i in range(0,len(m['tokens'])):
            g=m['tokens'][i]
            m['tokens'][i]=[w.strip(" ") for w in g]
            
            m['tokens'][i]=[x for x in m['tokens'][i] if x]
        self.data=m
    
    def stop_word_removal(self):
        #to be implemented
        return None;
    
    def stemming(self):
        #to be implemented
        return None;
        
    # this is static method    
    @staticmethod    
    def N_grams(data,tokenize = 1,ngrams =2):
        #to be implemented
        try:
            import nltk
            #from nltk import word_tokenize
            from nltk.util import ngrams
        except ImportError:
            print("NLTK library is not available: Please install NLTK to run this program")
        if (tokenize ==1):
            ngrams = ngrams(data,ngrams)
        else:
            data = nltk.word_tokenize(data)
            ngrams = ngrams(data,ngrams)
        return ngrams;
        
    @staticmethod
    def find_ngrams(s, n,tokenize =0):
        if (tokenize ==1):
            return zip(*[s[i:] for i in range(n)])
        else: 
            s = s.split(" ")
            return zip(*[s[i:] for i in range(n)])
   
    ##Text Transformation
    def text_transformation(self):
        #to be implemented
        return;
    
    def feature_selection(self, method):
        #to be implemented
        return;
    
    def clustering(self,clusters,method):
        #to be implemented
        return;
    
    def classification(self,Type,method):
        #to be implemented
        return;
        
    def information_retrieval(self,Type,method):
        #to be implemented
        return;
    
    def topic_discovery(self,Type):
        #to be implemented
        return;
    
    def summarization(self,Type):
        #to be implemented
        return;
        
    def topic_extraction(self):
        #to be implemented
        return;
        
    def text_preprocessing(self,tokenization =0,stemming =0,stop_word_removal= 0,N_grams =0):
        #to be implemented
        return;
    
    
    
        
    
    
      
        
        