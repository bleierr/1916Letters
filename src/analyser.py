#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
'''
Created on 27 May 2014
For the 1916 Letter Analyser
@author: Bleier
'''
from nltk import Text, FreqDist, corpus
import importer
import re
#The objects that are pickled must be in the namespace where they are unpickled - pickle only pickles the data 
from letter_classes import Letter, TxtCorpus
from gensim import models, corpora, similarities
from gensim.corpora import Dictionary
from settings import STOPWORD_LST
           

def get_word_freq(lst):
    """
    Given a list of words the function returns a nltk.probability.FreqDist object
    """
    #creates a nltk.text.Text obj
    txt = Text(lst)
    #creates a nltk.probability.FreqDist obj
    return FreqDist(txt)

def make_mmcorpus_and_dictionary(docs, path):
    """
    Function to create a vector corpus: documents represented as sparse vectors
    and a dictionary out of the words in the docs
    docs is a list of documents, each document is a list of words
    """
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
    corpora.MmCorpus.serialize(path, corpus)
    return dictionary  

def make_lsi(txt_corpus, dictionary):
    """
    Given a text corpus that has a reference to a dictionary and vector corpus 
    the function returns 
    """
    tfidf = models.TfidfModel(txt_corpus)
    corpus_tfidf = tfidf[txt_corpus]
    """for doc in corpus_tfidf:
        print(doc)"""
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
    topics = lsi[corpus_tfidf]
    return lsi, corpus_tfidf, topics

        
def doc_similarity(vec_lsi, lsi, mmcorpus):
    """
    tests document similarity
    parameters: vec_lsi is the lsi from the document that should be tested, lsi is lsi of corpus and mmcorpus is the full corpus
    """
    index = similarities.MatrixSimilarity(lsi[mmcorpus])
    sims = index[vec_lsi]
    #sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return sims
   
    
def make_analysis(txt_corpus):
    """
    This is the main function of the module. The function adds attributes to each letter object in lst
    The parameter letters is a list of letter objects as defined in the module letter.py
    """

    # self._word_freq = self.get_word_freq(self._plain_text_lst)
    #get all text from all letters
    
    t1 = Text([[w for w in text] for text in txt_corpus.get_tokens()])
    fdist = FreqDist(t1)
    total_words = fdist.N()
    most_freq_word = fdist.max()
    
    hapaxes = fdist.hapaxes()
    #remove stopwords
    t2 = Text([[w for w in text] for text in txt_corpus.get_tokens()])
    fdist_no_stop = FreqDist(t2)
    #fdist_no_stop.plot(50, cumulative=False)
    return fdist_no_stop, total_words, most_freq_word, hapaxes
        
if __name__ == "__main__":
    pass

