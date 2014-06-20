'''
Created on 27 May 2014
For the 1916 Letter Analyser
@author: Bleier
'''
import unittest, os
from analyser import make_mmcorpus_and_dictionary, make_lsi, doc_similarity
from gensim.corpora import Dictionary
from gensim import models, interfaces, corpora
from importer import get_text_from_txt, make_vector_corpus, make_word_dictionary
from settings import *
from letter_classes import Letter

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

class Test_dataAnalyser(unittest.TestCase):
    def setUp(self):
        mmcorpus_path = "tmp" + os.sep + "corpus.mm"
        self.dictionary = make_mmcorpus_and_dictionary([[word for word in document.split()] for document in documents], mmcorpus_path)
        self.mmcorpus = corpora.MmCorpus(mmcorpus_path) #load the saved mmcorpus
        self.lsi, self.topics, self.topics2text = make_lsi(self.mmcorpus, self.dictionary, 2)
        
        
    def test_make_vector_corpus_and_dictionary(self):
        """
        tests the function 'make_vector_corpus_and_dictionary': The function should create a file, in our example the file under the filename specified in mmcorpus_path under setUp
        the mmcorpus file contains is a list of lists, each list represents a document and the words of each document are represented as tuples (0,1), where the first item (0) is the
        mapping to a dictionary and the second is the frequency indicator
        In addition to creating the mmcorpus file the function creates and returns a dictionary with the word to id mapping used to translate the words in the mmcorpus
        """
        #test dictionary
        self.assertTrue(isinstance(self.dictionary, Dictionary))
        self.assertEqual(len(self.dictionary), 12)
        
        #test the mmCorpus
        self.assertTrue(isinstance(self.mmcorpus, corpora.mmcorpus.MmCorpus))
        self.assertEqual(len(self.mmcorpus), 9)
        result_corpus = [[(0, 1), (1, 1), (2, 1)],
            [(0, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
            [(2, 1), (5, 1), (7, 1), (8, 1)],
            [(1, 1), (5, 2), (8, 1)],
            [(3, 1), (6, 1), (7, 1)],
            [(9, 1)],
            [(9, 1), (10, 1)],
            [(9, 1), (10, 1), (11, 1)],
            [(4, 1), (10, 1), (11, 1)]]
        self.assertEqual([doc for doc in self.mmcorpus], result_corpus)
        
    def test_make_lsi(self):
        """
        the function 'make_lsi' takes mmCorpus, dictionary and an integer as arguments. A tuple with three items is returned:
        item 1: A latent semantic index, in our example stored as self.lsi
        item 2: A list of topics, in our example stored in self.topics
        item 3: And a list of text to corpus probability; stored in self.topics2text
        """
        #test lsi object
        self.assertTrue(isinstance(self.lsi, models.lsimodel.LsiModel))
        
        """test topics2text, should return a list of topic probabilities for each document, in the test there are 9 documents and 2 topics
                therefore a list of 9 items should be returned, each item is a tuple containing the number of the topic and probability, 
                e.g. [[(0, 0.066007833960904261), (1, -0.52007033063618513), (2, 0.37649581219168948)], [(0, 0.19667592859142577), (1, -0.76095631677000486), (2, -0.5080674581001664)]...] 
        """
        self.assertTrue(isinstance(self.topics2text, interfaces.TransformedCorpus))
        
        for item in self.topics2text:
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
        self.assertEqual([[(tup[0], round(abs(tup[1]), 3) ) for tup in doc] for doc in self.topics2text], result_topics)
        
        """
        test if topics are returned correctly
        the topics are returned in a list of topics:
        
        [u'0.703*"trees" + 0.538*"graph" + 0.402*"minors" + 0.187*"survey" + 0.061*"system" + 0.060*"time" + 0.060*"response" + 0.058*"user" + 0.049*"computer" + 0.035*"interface"', 
        u'0.460*"system" + 0.373*"user" + 0.332*"eps" + 0.328*"interface" + 0.320*"response" + 0.320*"time" + 0.293*"computer" + 0.280*"human" + 0.171*"survey" + -0.161*"trees"']
        """
        self.assertTrue(isinstance(self.topics, list))
        self.assertTrue(self.topics[0][:30] in ['0.703*"trees" + 0.538*"graph" ', '-0.703*"trees" + -0.538*"graph" ']) # the result could also be '-0.703*"trees" + 0.538*"graph" '
             
        #as in the example above absolute values are used to test the results, negative values are not relevant (see comment above)
        result = [(0.703, "trees"), (0.538, "graph"), (0.402, "minors"), (0.187, "survey"), (0.061, "system"), (0.060, "response"), (0.060, "time"), (0.058, "user"), (0.049, "computer"), (0.035, "interface")]

        self.assertEqual([(round(abs(tup[0]), 3), tup[1]) for tup in self.lsi.show_topic(0)], result)

    def test_doc_similarity(self):
        """
        doc = "Human computer interaction"
        vec_bow = self.dictionary.doc2bow(doc.lower().split())
        vec_lsi = self.lsi[vec_bow]
        sims = doc_similarity(vec_lsi, self.lsi, self.mmcorpus)
        self.assertTrue(isinstance(sims, list))
        self.assertTrue(isinstance(sims[0], tuple))
        """
        #this sets up the test corpus
        c = get_text_from_txt(TEST_SHAKESPEAR_DIR, TEST_SHAKESPEAR_CORPUS)
        make_word_dictionary(c, TEST_SHAKESPEAR_DICT)
        make_vector_corpus(c, TEST_SHAKESPEAR_VECTOR_CORPUS)
        
        
        
        path = "tmp" + os.sep + "shakespear_corpus.mm"
        corpus_ids, mmcorpus = c.get_vector_corpus()
        #corpora.MmCorpus.serialize(path, corpus)
        
        #get test sample
        f = open(TEST_SAMPLE_DIR + os.sep + "sample_errors.txt", "r")
        docs = f.read()
        f.close()
        
        l = Letter()
        l.add_page("12", "1", docs)
        
        #make_sample_vec_lsi(l.get_txt(), dictionary)
        
        #transform the sample to vector representation
        dictionary = c.get_dict()
        vec_bow = dictionary.doc2bow(l.get_txt())
       
        #mmcorpus = corpora.MmCorpus(path) 
        tfidf = models.TfidfModel(mmcorpus) 
        corpus_tfidf = tfidf[mmcorpus]
        #vec_tfidf = tfidf[vec_bow]
        
        
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=7)
        #sample_tfidf = models.TfidfModel(docs)
        vec_lsi = lsi[vec_bow]
        #print vec_lsi
        #print(lsi.show_topics(7))
        
        #for item in mmcorpus:
            #print item
        sims = doc_similarity(vec_lsi, lsi, mmcorpus)
        #print sims
        #print corpus_ids
        #for num, item in sorted(zip(corpus_ids, sims)):
            #print num, item
        
        #print sims # returns something else
        
        

if __name__ == "__main__":
    unittest.main()