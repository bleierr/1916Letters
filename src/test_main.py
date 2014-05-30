'''
Created on 26 May 2014
For the 1916 Letter Analyser
@author: Bleier
'''
import unittest
import main
from settings import TEST_EXCEL, TEST_CORPUS, TEST_WORD_DICT, TEST_VECTOR_CORPUS
from helper import item_from_pickle
from gensim.corpora import Dictionary
from letter_classes import TxtCorpus

class Test_1916LetterMain(unittest.TestCase):
    def test_data_importer(self):
        c = main.main_dataimporter(TEST_EXCEL, TEST_CORPUS, TEST_WORD_DICT, TEST_VECTOR_CORPUS)
        letters = item_from_pickle(TEST_CORPUS)
        self.assertTrue(isinstance(letters, dict))
        d = item_from_pickle(TEST_WORD_DICT)
        self.assertEqual(len(d), 114)
        self.assertTrue(isinstance(d, Dictionary))
        #get dictionary via corpus obj
        self.assertTrue(isinstance(c.get_dict(), Dictionary)) 
        #get vector corpus via corpus obj       
        self.assertTrue(isinstance(c.get_vector_corpus(), list))
        #self.assertEqual(len(c.get_vector_corpus()[0]), 8)
        #self.assertEqual(len(c.get_vector_corpus()[0]), 38)
        for item in c.get_vector_corpus():
            self.assertTrue(isinstance(item, list))
            self.assertTrue(len(item) in [79, 8, 38])
            for t in item:
                self.assertTrue(isinstance(t, tuple))
            

        
        
        
    def test_data_analyser(self):
        pass
    
    def test_pretty_output(self):
        pass

if __name__ == "__main__":
    unittest.main()


                

