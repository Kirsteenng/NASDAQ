#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 22:25:56 2017

@author: Kirsteenng
"""
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import pandas as pd
from nltk.corpus import sentiwordnet as swn

#-------------------------------------------------------------------------------
# 'rU' means to read
#f = open('/Users/Kirsteenng/Desktop/tes', 'rU')
#raw = f.read()

# input: dataframe
# output: dataframe
def sub(result):
    for i in range(1,len(result)):
        result.Symbol[i] = str(result.Symbol[i])
        if result.Symbol[i] == 'nan':
            result.set_value(i,'Symbol', result.Symbol[i-1])

    return result

# input: a list of strings
# output: a list of lists
# Tokenize sentences into words, remove stopwords
def clean(raw):
    #remove tags
   
    raw = re.sub("<(\w|\s|\!|\@|\#|\%|\$|\^|\&|\*|\(|\)|\.|\,|\?|\/|\;|\:|\'|\"|\+|\=|\~|\-|\_)*>", "", raw )
    raw = re.sub(r'\\r\\n', '',raw)

    return raw

# input: raw is a datafram cell,raw = result.Body[i]
# output: filtered is a list with individual words
def parse(raw):
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    #separate into words
    words = tokenizer.tokenize(raw)
    filtered = []
    for i in words:
        if i not in stop_words:
            filtered.append(i)

    #print('---------------------------------filtered',filtered)
    return filtered

# input: filtered is a list of tokenized words
# output: stemmed is a list of lemmatized words
def stemming(filtered):
    stemmed = [lemma.lemmatize(w) for w in filtered]
    return stemmed

# input: article is a list of tokenized words
# output:list is a list containing +20 -20 words from keyword
def search(keyword,article,sLength):
    my_list =[]
    counter =0
    #print '                ******************** Searching for keyword:' + keyword
    for counter in range(sLength):
        if article[counter] in keyword:
            my_list = my_list + add(keyword,article,counter,sLength)
    #print list
    return my_list

# Take +20 words or until beginning and -20 key words to the left
# output: a list of lemmatized words
def add(keyword,article,counter,sLength):
    upper = counter - 20
    lower = counter + 20
    if (upper >= 0 and lower <= sLength):
        ll = article[upper:counter] + article [counter:lower]
        return stemming(ll)

    elif (upper >= 0 and lower >= sLength):
        ll = article[upper:counter] + article [counter:sLength]
        return stemming(ll)

    elif (upper <= 0 and lower <= sLength):
        ll = article[0:counter] + article [counter:lower]
        return stemming(ll)

    else:
        return stemming (article[0:counter] + article [counter:sLength])

def stopword(text, new_list):
    f = open(text, 'r')
    for i in f:
        i = i.lower()
        i = i.strip()
        new_list.append(i)
        
    f.close()
    
    return new_list

def labelling(x):
    score = 0
    for i in x:
        exp = swn.senti_synsets(i,'a')
        if len(exp)>0:
            exp0 = list(exp)[0]
            score = score + (exp0.pos_score() - exp0.neg_score() * (1- exp0.obj_score()))
            
    # If article is positive
    if score >= 1:
        return 1
    else: 
        return 0
        
              
# -------------------------------------------- Main Begins ----------------------------------------

# /CNBC_articles.json
# /reuters_article.json

result = pd.read_json('/Users/Kirsteenng/tutorial/tutorial/spiders/CNBC_articles.json')

result = result.rename(columns={"name": "Symbol"})
result.Symbol.astype(str)

result = sub(result)

name = pd.read_csv('/Users/Kirsteenng/tutorial/tutorial/res/reuters.csv')
result = result.merge(name, left_on='Symbol', right_on='Symbol', how='left')

lemma = nltk.wordnet.WordNetLemmatizer ()
sLength = len(result)

# Adding tokenize column and its values to nan
result = result.reindex(columns=['Symbol','Name','Article','Time','Body','Tokenize','Label'])
result['Tokenize']= result['Tokenize'].astype(object)


sub_stop = []
old_list = stopwords.words('english')

new_list = stopword('/Users/Kirsteenng/Desktop/NASDAQ/Stop_Words_Generic.txt',sub_stop)
new_list = stopword('/Users/Kirsteenng/Desktop/NASDAQ/Stop_Words_DatesandNumbers.txt',new_list)
new_list = stopword('/Users/Kirsteenng/Desktop/NASDAQ/Stop_Words_Names.txt',new_list)

stop_words = set(new_list + old_list)

# -------------------------------------------- Main Loop Begins ----------------------------------------
#before=[[] for _ in range(sLength)]

for i in range(sLength):
    raw = result.Body[i]
    if type(raw) == float:
        continue
    
    raw = u' '.join(raw).encode('utf-8')
    keyword = result.Name[i]

    if len(raw) > 4:
        words = clean(raw)
        result.set_value(i,'Body',words)
        words = parse(words)

        # keyword_list is a list containing the keywords surrounding the name of the company
        keyword_list = search(keyword,words,len(words))

        #print keyword_list
        score = labelling(keyword_list)
        result.set_value(i,'Label',score)
        result.set_value(i,'Tokenize',keyword_list)


#print result

result.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/testresultCNBC.csv',encoding='utf-8', header=True, index=False,)
#result.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/testresultReuters.csv')
#result.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/testresultMarketWatch.csv')



