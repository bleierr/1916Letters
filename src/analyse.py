'''
Created on 18 Jun 2014

@author: Bleier
'''

from gensim import models, corpora, similarities

def make_lda_topics(vect_corpus, dictionary, num_topics=10, passes=1):
        
    lda = models.ldamodel.LdaModel(vect_corpus, id2word=dictionary, num_topics=num_topics, passes=passes)
    
    return lda.show_topics(topics=15, topn=20, log=False, formatted=True)
    

def make_topics(vector_corpus, dictionary, num_topics):
    """
    Given a vector corpus and a dictionary to translate the vector corpus the function returns a list of topics. 
    The number of topics generated is specified with the parameter num_topics. 
    """
    #corpus = corpora.MmCorpus(corpus_path)
    tfidf = models.TfidfModel(vector_corpus)
    corpus_tfidf = tfidf[vector_corpus]
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

def topics2docs(vector_corpus, dictionary, num_topics):
    """
    Parameters are a vector corpus file, a dictionary that can be used to translate the vector corpus, 
    and an integer for num_topics
    the function returns a document to topic list, with as many topics as requested by num_topics.
    """
    tfidf = models.TfidfModel(vector_corpus)
    corpus_tfidf = tfidf[vector_corpus]

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    #returns lsi, a list of topics and a list of distribution of topics over the corpus documents
    doc2topics = lsi[corpus_tfidf]
    return doc2topics
    
def doc_similarity(vector_corpus, dictionary, test_doc, num_topics):
    """
    tests document similarity
    Given a vector corpus of documents and a test document (test_doc) the function tests the similarity of the test doc to the
    documents in the vector corpus. test_doc is a list of word tokens. tokens should be all lower case and stopwords removed.
    A dictionary to translate the vector corpus and a topic number has to be supplied as well.
    """
    lsi = models.LsiModel(vector_corpus, id2word=dictionary, num_topics=num_topics)
    
    vec_bow = dictionary.doc2bow(test_doc)
    vec_lsi = lsi[vec_bow] # convert the query to LSI space
    index = similarities.MatrixSimilarity(lsi[vector_corpus])
    sims = index[vec_lsi]
    #sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return [item for item in sims] 

      

