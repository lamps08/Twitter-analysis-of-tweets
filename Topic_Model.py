# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:04:55 2018
References :Dr Gene Moo Lee Notes,Analytics Vidhya
@author: lamps08
"""
from __future__ import division, print_function
from gensim import corpora, models, similarities, matutils
import gensim
import re
import numpy as np
import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

#ps = PorterStemmer()
ss = SnowballStemmer("english")


lowercase = []
cleaned = []
stemed_list = []
with open("samsung.json",'r') as f:
    read = json.load(f)
    stopWords = set(stopwords.words('english')) 
    for words in read:
        tweet = words.lower().split()
        lowercase.append(tweet)
    #print (tokenized)
    #removing stop words and punctuations
    for tweet in lowercase:
        #print (tweet)
        
        cleaned_word = " ".join([word for word in tweet
                                 
                                 if 'http' and 'https' not in word
                                 and not word.startswith('@')
                                 and not word.startswith('#')
                                 and word not in stopWords
                                 and word != 'rt'
                                 
                                 
                                 ])
        punct_free = re.sub(r'[^\w\s]', ' ',cleaned_word )
        cleaned.append(punct_free)
    #print (cleaned)
# building Word Cloud from stemmed words
    for word in cleaned:
        stemed_word = " ".join([ss.stem(words) for words in word.split()
                                                              
                                 
                                 ])
    
            
        #punct_free = re.sub(r'[^\w\s]', ' ',cleaned_word )  
        stemed_list.append(stemed_word)
    #print(stemed_list)
# Topic Modelling using LDA - creating term dictinory for our model
word_split = [doc.split() for doc in stemed_list]  
dictionary = corpora.Dictionary(word_split)

# creating do term matrix
doc_term_matrix = [dictionary.doc2bow(doc) for doc in word_split]


#Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)
print(ldamodel.print_topics(num_topics=10, num_words=5))
# Topic Modelling using NMF



vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
doc_term_matrix = vectorizer.fit_transform(stemed_list)
print (doc_term_matrix.shape)
vocab = vectorizer.get_feature_names() 
from sklearn import decomposition

#print ('num of documents, num of unique words')
#print (doc_term_matrix.shape)

num_topics = 10

clf = decomposition.NMF(n_components=num_topics, random_state=1)
doctopic = clf.fit_transform(doc_term_matrix)
#print (num_topics, clf.reconstruction_err_)
topic_words = []
num_top_words = 5

#print (vocab[100])

for topic in clf.components_:
    #print topic.shape, topic[:10]
    word_idx = np.argsort(topic)[::-1][:num_top_words]
    print (word_idx)
    for idx in word_idx:
        print (vocab[idx])
        

    