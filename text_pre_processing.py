import re
twitter_data1 =[];
clean_re = re.compile('(http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+)|((RT @[\w]+:)|(RT@[\w]+:))',re.I)
for i in range(0, len(twitter_data1)):
    print (i)
    twitter_data1['TWEET'][i]= re.sub(clean_re,'',twitter_data1['TWEET'][i])

#2. for html tags removal

htmlcleanr= re.compile('<.*?>')

for i in range(0, len(twitter_data1)):
    print (i)
    twitter_data1['TWEET'][i]=re.sub(htmlcleanr,'',twitter_data1['TWEET'][i])

#3. removing extra white spaces    

for i in range(0, len(twitter_data1)):
    print (i)
    twitter_data1['TWEET'][i]=re.sub(' +', ' ', twitter_data1['TWEET'][i])

#4. to keep emoticons, @ words, hashtags together before tokenization

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
    
regex_str = [
    emoticons_str,
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hashtags
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)
    

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens