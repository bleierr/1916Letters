'''
Created on 18 Jun 2014

@author: Bleier
'''

from gensim import models, corpora, similarities
from txt_classes import TxtCorpus
from helper import item_from_pickle, item_to_pickle
import os


def make_lda_mallet_topics(vect_corpus, dictionary, num_topics=10,):
    path_to_mallet = "C:"+os.sep+"mallet"+os.sep+"bin"+os.sep+"mallet"
    mallet_lda = models.LdaMallet(path_to_mallet, corpus=vect_corpus, num_topics=num_topics, id2word=dictionary)
    print mallet_lda.show_topics()


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

def docs2topics(vector_corpus, dictionary, num_topics):
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


if __name__ == "__main__":
    path_to_txt_items = "letter_corpus" + os.sep + "corpusfiles.pickle"
    path_to_txt_items_clean = "letter_corpus" + os.sep + "corpusfiles_clean.pickle"
    vec_corpus_file = "letter_corpus" + os.sep + "corpus.vect"
    dict_file = "letter_corpus" + os.sep + "corpus.dict"
    corpus_dir = "letter_corpus" + os.sep + "letter_corpus.pickle"
    txtItems = item_from_pickle(path_to_txt_items)
    """
    new_corpus_items = []
    for item in txtItems:
        new_path = "letter_corpus" + os.sep + "cleantxt" + os.sep + item.unique_name + ".txt"
        item.txt_file_path = new_path
        new_corpus_items.append(item)
    #item_to_pickle(path_to_txt_items_clean, new_corpus_items)
    #corpus = TxtCorpus(path_to_txt_items_clean)
    
    #corpus.add_vector_corpus_and_dictionary(vec_corpus_file, dict_file)
    
    #save corpus with dict and vect corpus
    item_to_pickle(corpus_dir, corpus)
    corpus = item_from_pickle(corpus_dir)
    """
    nodes_strg = "Id,Label,inCollection,TextAmount"
    for topic in range(16):
        nodes_strg += "\nT{0},{1},{2},{3}".format(topic, "Topic "+str(topic), "topic", 100)
    for item in txtItems:
        node_name = item.unique_name
        in_collection = item.Collection
        num_words = len(item.get_txt())
        nodes_strg += "\n{0},{1},{2},{3}".format(node_name, "Letter "+str(node_name), in_collection, num_words)
    
    with open("letters_nodes_gephi.txt", "w") as f:
        f.write(nodes_strg)
    
    """
    d = corpus.get_dictionary()
    print d
    v = corpus.get_vector_corpus()
    topics = make_topics(v, d, 16)
    
    t2d = docs2topics(v, d, 16)
    
    #print topics
    strg = ""
    with open("letter_corpus" + os.sep +"topic_analysis.txt", "w") as f:
        for num,item in enumerate(topics):
            strg += "{0} Topic: {1}\n\n".format(num, item)
        
        strg += "\n\n\n\n\n"
        for num,item in enumerate(t2d):
            strg += "{0} Topic: {1}\n\n".format(num, item)   
            
        f.write(strg)
    """