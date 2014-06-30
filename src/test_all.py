'''
Created on 18 Jun 2014

@author: Bleier
'''

from gensim import models, corpora, similarities, interfaces
from txt_classes import TxtCorpus, TxtItem
import unittest, shutil
import importer, analyse, outputter
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
        #set up test directory
        self.tempdir = "tmp"
        if os.path.isdir(self.tempdir):
            raise OSError("The sub folder 'tmp' exists already!")
        os.mkdir(self.tempdir)
        for idx, item in enumerate(documents):
            f = open(self.tempdir + os.sep + "testfile" + str(idx) + ".txt", "w")
            f.write(item)
            f.close()
        self.c = importer.get_texts_from_files(self.tempdir, self.tempdir) 
        self.vect_corpus = self.c.get_vector_corpus()
        self.dictionary = self.c.get_dict()        
        
    def test_letterCorpusCorrectlyImported(self):
        """
        tests it the letter corpus was correctly created
        """
        #tests if the items are correctly imported from text files
        self.assertTrue(isinstance(self.c, TxtCorpus))
        for item in self.c.get_txtitems():
            self.assertTrue(isinstance(item, TxtItem))
        self.assertEqual(len([l for l in self.c.get_txtitems()]), 9)
     
    def test_makeTopics(self):
        #ensures the dictionary is correctly imported
        self.assertEqual(len(self.dictionary), 12) 
        self.assertEqual(self.dictionary[11], "minors")
        self.assertEqual(self.dictionary[9], "trees")
        #tests if the topics are corrctly returned, topics are returned in a list of lists of tuples
        topics = analyse.make_topics(self.vect_corpus, self.dictionary, 2)
        self.assertTrue(isinstance(topics, list))
        for topic in topics:
            self.assertTrue(isinstance(topic, list))
            for t in topic:
                self.assertTrue(isinstance(t, tuple))
                self.assertTrue(isinstance(t[0], float))
                self.assertTrue(isinstance(t[1], unicode))
        
    def test_doc_similarity(self):        
        doc2topic = analyse.topics2docs(self.vect_corpus, self.dictionary, 2)
        self.assertTrue(isinstance(doc2topic, interfaces.TransformedCorpus))
        for item in doc2topic:
            self.assertTrue(isinstance(item, list))
            for t in item:
                self.assertTrue(isinstance(t, tuple))
                self.assertTrue(isinstance(t[0], int))
                self.assertTrue(isinstance(t[1], float))
    
    def test_print_output(self):
        toPrint = {}
        topics = analyse.make_topics(self.vect_corpus, self.dictionary, 2)
        toPrint["topics"] = topics
        doc2topic = analyse.topics2docs(self.vect_corpus, self.dictionary, 2)
        toPrint["topic_sim"] = [item for item in doc2topic]
        test_doc = "Human computer interaction".lower().split()
        """
        f = open("test_txt" + os.sep + "txt" + os.sep + "simtest.txt", "r")
        test_doc = f.read().lower().split()
        f.close()"""
        sims = analyse.doc_similarity(self.vect_corpus, self.dictionary, test_doc, 2)
        toPrint["doc_sim"] = ("Test Doc", [item for item in zip(sims, range(self.c.number_of_txts()))])
        s = outputter.data_to_output_string(toPrint)
        f = open("stat.txt", "w")
        f.write(s)
        f.close()
        
   
    def tearDown(self):
        shutil.rmtree(self.tempdir)

if __name__ == "__main__":
    unittest.main()