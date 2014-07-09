'''
Created on 16 May 2014

@author: Bleier
'''
import unittest, os, shutil
from txt_classes import TxtCorpus, TxtItem
from importer import *
from gensim import corpora


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
        self.tempdir = "tmp"
        if os.path.isdir(self.tempdir):
            raise OSError("The sub folder 'tmp' exists already!")
        os.mkdir(self.tempdir)
        self.tempdir_excel = "tmp" + os.sep + "excel" 
        if os.path.isdir(self.tempdir_excel):
            shutil.rmtree(self.tempdir_excel)
        os.mkdir(self.tempdir_excel)
        excel_file = "test_data"+ os.sep + "test_1916Letters.xlsx"
        
        self.tempdir_txt = "tmp" + os.sep + "txt"
        if os.path.isdir(self.tempdir_txt):
            shutil.rmtree(self.tempdir_txt)
        os.mkdir(self.tempdir_txt)
        
        self.tempdir_gensim = "tmp" + os.sep + "gensim"
        if os.path.isdir(self.tempdir_gensim):
            shutil.rmtree(self.tempdir_gensim)
        os.mkdir(self.tempdir_gensim)
        
        # makes the test corpus from an excel file
        texts, id2texts = get_texts_from_Excel(excel_file, self.tempdir_excel) 
        self.c_from_excel = make_text_corpus(texts, self.tempdir_excel)
        
        for idx, item in enumerate(documents):
            f = open(self.tempdir_txt + os.sep + "testfile" + str(idx) + ".txt", "w")
            f.write(item)
            f.close()
        #makes a text corpus from a number of text files
        texts, id2texts = get_texts_from_files(self.tempdir_txt, self.tempdir_txt, ".txt") 
        self.c_from_txt = make_text_corpus(texts, self.tempdir_txt)
        
    def test_get_texts_from_Excel(self):
        """
        Tests the function get_texts_from_Excel, and ensures that a TxtCorpus with TxtItem objects is returned
        The corpus should also have a vector corpus and a dictionary to translate the items in the vector corpus to words
        """
        self.assertTrue(isinstance(self.c_from_excel, TxtCorpus))
        msg = "Error: The item with number {0} is not of type TxtItem"
        for idx, txt in enumerate(self.c_from_excel.get_txtitems()):
            self.assertTrue(isinstance(txt, TxtItem), msg.format(idx))

        
        
    def test_time_stamps(self):
        possible_timestamps = ["2013-11-13","2013-09-30", "2013-11-03", "2013-11-05", "2013-09-27"]
        for item in self.c_from_excel.get_txtitems():
            for key, item in item.get_pages().items():
                for version in item:
                    time_stamp = version[0]
                    msg = "Error: The timestamp {0} is not in the list of possible timestamps."
                    self.assertTrue(time_stamp.strftime('%Y-%m-%d') in possible_timestamps, msg)
                
    
         
    def test_make_text_corpus(self):
        """
        Tests if corpus, dictionary and text-dictionary mapping corpus is created correctly
        """
        self.assertTrue(isinstance(self.c_from_excel, TxtCorpus))
        d = self.c_from_excel.get_dict()
        vec = d.doc2bow(["this", "a"])
        
    def test_make_word_dictionary(self):
        """
        Tests the dictionary for the words
        """
        d = self.c_from_excel.get_dict()
        self.assertTrue(isinstance(d, corpora.Dictionary))
        #self.assertTrue("gold" in d.token2id)    #token2id reverses key - value in dictionary: 32: "house" ==> "house": 32
        self.assertFalse("all" in d.token2id)
        msg = "Error: The filepath to the gensim Dictionary stored in the TxtCorpus {0} is not the same as: {1}"
        self.assertEqual(self.c_from_excel.dict_path, self.tempdir_excel + os.sep + "text_corpus.dict", msg.format(self.c_from_excel.dict_path, self.tempdir_excel + os.sep + "text_corpus.dict"))
        

    def test_corpusImportedCorrectly(self):
        self.assertTrue(isinstance(self.c_from_txt, TxtCorpus))
        self.assertTrue(len([item for item in self.c_from_txt]), 9)
        
    def tearDown(self):
        shutil.rmtree(self.tempdir_excel)
        shutil.rmtree(self.tempdir_txt)
        shutil.rmtree(self.tempdir_gensim)
        shutil.rmtree(self.tempdir)


if __name__ == "__main__":
    unittest.main()