'''
Created on 27 May 2014
For the 1916 Letter Analyser
@author: Bleier
'''
import unittest, os
from analyse import make_mmcorpus_and_dictionary, make_topics, topics2docs
from gensim import models, interfaces, corpora
from gensim.corpora import Dictionary

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

corpus_path = "tmp" + os.sep + "gensim_txt" + os.sep + "corpus.mm"

class Test_dataAnalyser(unittest.TestCase):
    def setUp(self):
        self. docs_split = []
        for item in documents:
            self.docs_split.append(item.split())
        self.d = make_mmcorpus_and_dictionary(self.docs_split, corpus_path)
        
        
    def test_make_mmcorpus_and_dictionary(self):
        mmcorpus = corpora.MmCorpus(corpus_path)
        
        #test dictionary
        self.assertTrue(isinstance(self.d, Dictionary))
        self.assertEqual(len(self.d), 12)
        #test the mmCorpus
        self.assertTrue(isinstance(mmcorpus, corpora.mmcorpus.MmCorpus))
        self.assertEqual(len(mmcorpus), 9)
        result_corpus = [[(0, 1), (1, 1), (2, 1)],
            [(0, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
            [(2, 1), (5, 1), (7, 1), (8, 1)],
            [(1, 1), (5, 2), (8, 1)],
            [(3, 1), (6, 1), (7, 1)],
            [(9, 1)],
            [(9, 1), (10, 1)],
            [(9, 1), (10, 1), (11, 1)],
            [(4, 1), (10, 1), (11, 1)]]
        self.assertEqual([doc for doc in mmcorpus], result_corpus)
        
        
    def test_make_topics(self):
        """
        test if topics are returned correctly
        the topics are returned in a list of topics:
        
        [u'0.703*"trees" + 0.538*"graph" + 0.402*"minors" + 0.187*"survey" + 0.061*"system" + 0.060*"time" + 0.060*"response" + 0.058*"user" + 0.049*"computer" + 0.035*"interface"', 
        u'0.460*"system" + 0.373*"user" + 0.332*"eps" + 0.328*"interface" + 0.320*"response" + 0.320*"time" + 0.293*"computer" + 0.280*"human" + 0.171*"survey" + -0.161*"trees"']
        """
        topics = make_topics(corpus_path, self.d, 2)
        self.assertTrue(isinstance(topics, list))
        self.assertTrue(isinstance(topics[0], list))
        self.assertTrue(isinstance(topics[0][0], tuple))
        self.assertTrue(isinstance(topics[0][0][0], float))
        self.assertTrue(isinstance(topics[0][0][1], unicode))
        self.assertEqual(abs(topics[0][0][0]), 0.703)
        self.assertEqual(topics[0][0][1], "trees")
        
            
    def test_topics2docs(self):
        """test t2d, should return a list of topic probabilities for each document, in the test there are 9 documents and 2 topics
                therefore a list of 9 items should be returned, each item is a tuple containing the number of the topic and probability, 
                e.g. [[(0, 0.066007833960904261), (1, -0.52007033063618513), (2, 0.37649581219168948)], [(0, 0.19667592859142577), (1, -0.76095631677000486), (2, -0.5080674581001664)]...] 
        """
        t2d = topics2docs(corpus_path, self.d, 2)
        self.assertTrue(isinstance(t2d, interfaces.TransformedCorpus))
        
        for item in t2d:
            self.assertTrue(isinstance(item, list))
            for t in item:
                self.assertTrue(isinstance(t, tuple))
                self.assertTrue(isinstance(t[0], int))
                self.assertTrue(isinstance(t[1], float))
        # the absolute values of the probability is important, negative values do not make a difference according to the gensim tutorial
        # self.topics2text should contain absolute values as given here in the 'result_topics' list
        # example is taken from gensim tutorial
        result_topics = [[(0, 0.066), (1, 0.520)],
                         [(0, 0.197), (1, 0.761)],
                         [(0, 0.090), (1, 0.724)],
                         [(0, 0.076), (1, 0.632)],
                         [(0, 0.102), (1, 0.574)],
                         [(0, 0.703), (1, 0.161)],
                         [(0, 0.877), (1, 0.168)],
                         [(0, 0.910), (1, 0.141)],
                         [(0, 0.617), (1, 0.054)]]
        self.assertEqual([[(tup[0], round(abs(tup[1]), 3) ) for tup in doc] for doc in t2d], result_topics)
        
    
        

if __name__ == "__main__":
    unittest.main()