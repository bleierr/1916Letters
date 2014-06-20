'''
Created on 16 May 2014

@author: Bleier
'''
import unittest, re, datetime, time, os, shutil
from letter_classes import TxtCorpus, Letter
from importer import *
from helper import item_to_pickle, item_from_pickle
from letter_classes import Letter, TxtCorpus
from gensim import corpora
from settings import TEST_EXCEL, TEST_CORPUS, TEST_WORD_DICT


text = "Human machine interface for lab abc computer applications. A survey of user opinion of computer system response time"

lst = [["Human", "machine", "interface", "for", "lab", "abc", "computer", "machine"],
        ["A", "survey", "of", "user", "opinion", "of", "computer", "system", "response", "time"]]

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

class Test(unittest.TestCase):
    
    def setUp(self):
        self.c = make_text_corpus(TEST_EXCEL, TEST_CORPUS) # makes the test corpus and saves it to a file
        make_vector_corpus_and_dictionary(self.c, TEST_VECTOR_CORPUS, TEST_WORD_DICT)
        self.tempdir = "tmp" + os.sep + "gensim_txt"
        if os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)
        os.mkdir(self.tempdir)
        num_files = len(documents)
        for idx, item in enumerate(documents):
            f = open(self.tempdir + os.sep + "testfile" + str(idx) + ".txt", "w")
            f.write(item)
            f.close()
        self.corp = get_text_from_txt(self.tempdir, self.tempdir)
        
    def test_get_letters_from_Excel(self):
        """
        Tests the function get_letters_from_Excel, and ensures that a dictionary with letter objects is returned
        """
        letters, wb = get_letters_from_Excel(TEST_EXCEL)
        self.assertTrue(isinstance(letters, list)) # the function returns a dictionary
        msg = "Error: The item with the key {0} is not of type Letter"
        for key, value in letters.items():
            self.assertTrue(isinstance(value, Letter), msg.format(key))
        """
        msg = "Error: In item with the key {0}. The key should be also part of the transcription, but is not found in: {1}"
        for key, value in letters.items():
            self.assertTrue(key in value.get_txt()[0], msg.format(key, value.get_txt()))"""
        msg = "Error: The key 'second' not found in dictionary letters."
        self.assertTrue("32" in letters, msg)
        
    def test_time_stamps(self):
        possible_timestamps = ["2013-11-13","2013-09-30", "2013-11-03", "2013-11-05", "2013-09-27"]
        for item in self.c.get_letters():
            for key, item in item.get_pages().items():
                for version in item:
                    time_stamp = version[0]
                    msg = "Error: The timestamp {0} is not in the list of possible timestamps."
                    self.assertTrue(time_stamp.strftime('%Y-%m-%d') in possible_timestamps, msg)
                
    
         
    def test_make_text_corpus(self):
        """
        Tests if corpus, dictionary and text-dictionary mapping corpus is created correctly
        """
        self.assertTrue(isinstance(self.c, TxtCorpus))
        d = item_from_pickle(TEST_WORD_DICT) # get the dictionary from pickle
        vec = d.doc2bow(["this", "a"]) 
        #print vec
               
        #self.assertEqual(vec, [(1, 1)])
        #self.assertTrue(u"machine" in dictionary.token2id)
        
    def test_make_word_dictionary(self):
        """
        Tests the dictionary for the words
        """
        d = item_from_pickle(TEST_WORD_DICT) # get the dictionary from pickle
        self.assertTrue(isinstance(d, Dictionary))
        print d.token2id
        self.assertTrue("gold" in d.token2id)    #token2id reverses key - value in dictionary: 32: "house" ==> "house": 32
        self.assertFalse("all" in d.token2id)
        msg = "Error: The filepath to the gensim Dictionary stored in the TxtCorpus is not correct: {0}"
        self.assertEqual(self.c.dict_path, TEST_WORD_DICT, msg.format(self.c.dict_path))
        
    def test_get_text_from_txt(self):
        c = get_text_from_txt(TEST_SHAKESPEAR_DIR, TEST_SHAKESPEAR_DIR)
        for item in c.get_tokens():
            """get tokens should return a list of tuples, the first item is the key used in the dictionary that serves as source for the TxtCorpusname 
            the second item is a list of tokens
            """
            self.assertTrue(isinstance(item, tuple))
            self.assertTrue(isinstance(item[0], str))
            self.assertTrue(isinstance(item[1], list))
            self.assertTrue("shakespear" in item[0]) # each of the test files used in the shakespear folder contain the name shakespear in the filename, the filename is used as key in the dict
                    

    def test_corpusImportedCorrectly(self):
        self.assertTrue(isinstance(self.corp, TxtCorpus))
        self.assertTrue(len([item for item in self.corp]), 9)
        

    def tearDown(self):
        os.remove(TEST_CORPUS)
        os.remove(TEST_WORD_DICT)


if __name__ == "__main__":
    unittest.main()