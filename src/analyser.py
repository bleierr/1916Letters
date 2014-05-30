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
from gensim.corpora import Dictionary
           

def get_word_freq(lst):
    """
    Given a list of words the function returns a nltk.probability.FreqDist object
    """
    #creates a nltk.text.Text obj
    txt = Text(lst)
    #creates a nltk.probability.FreqDist obj
    return FreqDist(txt)
    
    
    
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

