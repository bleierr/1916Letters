'''
Created on 19 Jun 2014

@author: Bleier
'''
'''
Created on 18 Jun 2014

@author: Bleier
'''

from gensim import models, corpora, similarities, interfaces
from letter_classes import TxtCorpus, Letter
import unittest, shutil
import analyse
import importer
import os




documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

class Test_All_Modules(unittest.TestCase):
    def setUp(self):
        self.tempdir = "tmp" + os.sep + "gensim_txt"
        if os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)
        os.mkdir(self.tempdir)
        num_files = len(documents)
        for idx, item in enumerate(documents):
            f = open(self.tempdir + os.sep + "testfile" + str(idx) + ".txt", "w")
            f.write(item)
            f.close()
        self.c = importer.get_text_from_txt(self.tempdir, self.tempdir)  
        
        #file path to mm corpus
        self.file_path = self.tempdir + os.sep + "corpus.mm"
        # the method c.get_tokens() returns a tuple of fileID, list of tokens
        id_lst, vect_corpus = self.c.get_vector_corpus()
        self.dictionary = self.c.get_dict()
        #self.id_txt_mapping = self.c.get_tokens()
        #self.tokens = [t[1] for t in self.id_txt_mapping]
        #self.dictionary = analyse.make_mmcorpus_and_dictionary(self.tokens, self.file_path) 
        corpora.MmCorpus.serialize(self.file_path, vect_corpus)
        
        
    def test_letterCorpusCorrectlyImported(self):
        """
        tests it the letter corpus was correctly created
        """
        #tests if the items are correctly imported from text files
        self.assertTrue(isinstance(self.c, TxtCorpus))
        for item in self.c.get_letters():
            self.assertTrue(isinstance(item, Letter))
        self.assertEqual(len([l for l in self.c.get_letters()]), 9)
        
       
        
    def test_makeTopics(self):
        print self.dictionary
        self.assertEqual(len(self.dictionary), 12)
        self.assertEqual(self.dictionary[11], "time")
        
        #tests if the topics are corrctly returned, topics are returned in a list of lists of tuples
        topics = analyse.make_topics(self.file_path, self.dictionary, 2)
        self.assertTrue(isinstance(topics, list))
        for topic in topics:
            self.assertTrue(isinstance(topic, list))
            for t in topic:
                self.assertTrue(isinstance(t, tuple))
                self.assertTrue(isinstance(t[0], float))
                self.assertTrue(isinstance(t[1], unicode))
        

    def test_doc_similarity(self):
        
        doc2topic = analyse.topics2docs(self.file_path, self.dictionary, 2)
        self.assertTrue(isinstance(doc2topic, interfaces.TransformedCorpus))
        for item in doc2topic:
            self.assertTrue(isinstance(item, list))
            print item
            for t in item:
                self.assertTrue(isinstance(t, tuple))
                self.assertTrue(isinstance(t[0], int))
                self.assertTrue(isinstance(t[1], float))
        
        
           
           
        """ 
        ids, cor = self.c.get_vector_corpus()
        for item in zip(ids, cor):
            print item
        """
        

if __name__ == "__main__":
    unittest.main()