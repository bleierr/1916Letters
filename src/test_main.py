'''
Created on 26 May 2014
For the 1916 Letter Analyser
@author: Bleier
'''
import unittest
import main
from settings import *
from helper import item_from_pickle
from gensim.corpora import Dictionary
from letter_classes import TxtCorpus

class Test_1916LetterMain(unittest.TestCase):
    def test_data_importer(self):
        c = main.main_dataimporter(TEST_CORPUS, TEST_WORD_DICT, TEST_VECTOR_CORPUS, excel_file=TEST_EXCEL)
        letters = item_from_pickle(TEST_CORPUS)
        self.assertTrue(isinstance(letters, dict))
        self.assertTrue(len(letters), 3)
        d = item_from_pickle(TEST_WORD_DICT)
        self.assertEqual(len(d), 83)  # this number depends on the stopword list, first was 114 items in dict, now 83
        self.assertTrue(isinstance(d, Dictionary))
        #get dictionary via corpus obj
        self.assertTrue(isinstance(c.get_dict(), Dictionary)) 
        """get vector corpus via corpus obj     
        the method get_vector_corpus() on a TxtCorpus returns a tuple of two lists, the first contains the ids of the documents, 
        the second a lists of tuples with dict-word mapping and a vector as frequency indicator for each doc
        """
        self.assertTrue(isinstance(c.get_vector_corpus(), tuple))
        self.assertEqual(c.get_vector_corpus()[0], ["32", "44", "45"])
        
        doc_ids, vector_corpus = c.get_vector_corpus()
        
        self.assertTrue(len(vector_corpus), 3)
        
        for item in vector_corpus:
            self.assertTrue(isinstance(item, list))
            self.assertTrue(len(item) in [57, 3, 29]) # this length depends on the stopword list, first was [79, 8, 38], 
            for t in item:
                self.assertTrue(isinstance(t, tuple))
            

        
        
        
    def test_data_analyser(self):
        pass
        
        
        
        
    
    
    def test_pretty_output(self):
        pass

if __name__ == "__main__":
    unittest.main()


                

