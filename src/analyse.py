'''
Created on 18 Jun 2014

@author: Bleier
'''

from gensim import models, corpora, similarities
from settings import STOPWORD_LST
import os




def make_mmcorpus_and_dictionary(docs, file_path):
   
    
    #remove items in stopword list (might not be necessary if it has been done in previous step)
    texts = [[word.lower() for word in document if word.lower() not in STOPWORD_LST]
         for document in docs]

    all_tokens = sum(texts, [])
    #print(all_tokens)
    
    #remove all the token that exist only once
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
             for text in texts]
    dictionary = corpora.Dictionary(texts)
     
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(file_path, corpus)
    return dictionary  


def make_topics(corpus_path, dictionary, num_topics):
    """
    Given a text corpus that has a reference to a dictionary and vector corpus 
    the function returns 
    """
    corpus = corpora.MmCorpus(corpus_path)
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    """for doc in corpus_tfidf:
        print(doc)"""
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    topics_str = lsi.show_topics(num_topics)
    """
        the topics are returned in a list of topic strings:
        
        [u'0.703*"trees" + 0.538*"graph" + 0.402*"minors" + 0.187*"survey" + 0.061*"system" + 0.060*"time" + 0.060*"response" + 0.058*"user" + 0.049*"computer" + 0.035*"interface"', 
        u'0.460*"system" + 0.373*"user" + 0.332*"eps" + 0.328*"interface" + 0.320*"response" + 0.320*"time" + 0.293*"computer" + 0.280*"human" + 0.171*"survey" + -0.161*"trees"']
    """
    topics = []
    for item in topics_str:
        topic = []
        for strg in item.split(" + "):
            strg = strg.strip()
            t = []
            for item in tuple(strg.split("*")):
                item = item.strip("\"").strip("'").strip()
                t.append(item)
            topic.append((float(t[0]), t[1]))
        topics.append(topic)
                             
    return topics

def topics2docs(corpus_path, dictionary, num_topics):
    """
    Given a filepath to mmcorpus and a dictionary that can be used to translate the word ids
    the function returns a document to topic list.
    """
    corpus = corpora.MmCorpus(corpus_path)
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    """for doc in corpus_tfidf:
        print(doc)"""
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    #returns lsi, a list of topics and a list of distribution of topics over the corpus documents
    doc2topics = lsi[corpus_tfidf]
    return doc2topics
    
        

