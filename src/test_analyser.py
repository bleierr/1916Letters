'''
Created on 27 May 2014
For the 1916 Letter Analyser
@author: Bleier
'''
import unittest, os
from analyser import make_mmcorpus_and_dictionary, make_lsi, doc_similarity
from gensim.corpora import Dictionary
from gensim import models, interfaces, corpora
from importer import get_text_from_txt
from settings import TEST_MIDSUMMER_SAMPLE
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
        self.lsi, self.corpus_tfidf, self.topics = make_lsi(self.mmcorpus, self.dictionary)
        
        
    def test_make_vector_corpus_and_dictionary(self):
        self.assertTrue(isinstance(self.dictionary, Dictionary))
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
        
        self.assertTrue(isinstance(self.corpus_tfidf, interfaces.TransformedCorpus))
        self.assertTrue(isinstance(self.topics, interfaces.TransformedCorpus))
        result_corpus = [[(0, 0.57735026918962573), (1, 0.57735026918962573), (2, 0.57735026918962573)],
                         [(0, 0.44424552527467476), (3, 0.44424552527467476), (4, 0.44424552527467476), (5, 0.32448702061385548), (6, 0.44424552527467476), (7, 0.32448702061385548)],
                         [(2, 0.5710059809418182), (5, 0.41707573620227772), (7, 0.41707573620227772), (8, 0.5710059809418182)],
                         [(1, 0.49182558987264147), (5, 0.71848116070837686), (8, 0.49182558987264147)],
                         [(3, 0.62825804686700459), (6, 0.62825804686700459), (7, 0.45889394536615247)],
                         [(9, 1.0)],
                         [(9, 0.70710678118654746), (10, 0.70710678118654746)],
                         [(9, 0.50804290089167492), (10, 0.50804290089167492), (11, 0.69554641952003704)],
                         [(4, 0.62825804686700459), (10, 0.45889394536615247), (11, 0.62825804686700459)]]
        
        self.assertEqual([doc for doc in self.corpus_tfidf], result_corpus)
        result_topics = [[(0, -0.066), (1, 0.520)],
                         [(0, -0.197), (1, 0.761)],
                         [(0, -0.090), (1, 0.724)],
                         [(0, -0.076), (1, 0.632)],
                         [(0, -0.102), (1, 0.574)],
                         [(0, -0.703), (1, -0.161)],
                         [(0, -0.877), (1, -0.168)],
                         [(0, -0.910), (1, -0.141)],
                         [(0, -0.617), (1, 0.054)]]
        
        #self.assertEqual([[(tup[0], round(tup[1], 3) ) for tup in doc] for doc in self.topics], result_topics)
        
        result = [(-0.703, "trees"), (-0.538, "graph"), (-0.402, "minors"), (-0.187, "survey"), (-0.061, "system"), (-0.060, "response"), (-0.060, "time"), (-0.058, "user"), (-0.049, "computer"), (-0.035, "interface")]
       
        #self.assertEqual([(round(tup[0], 3), tup[1]) for tup in self.lsi.show_topic(0)], result)

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
        c = get_text_from_txt()
        print c
        
        
        path = "tmp" + os.sep + "shakespear_corpus.mm"
        corpus_ids, corpus = c.get_vector_corpus()
        corpora.MmCorpus.serialize(path, corpus)
        
        #get test sample
        f = open(TEST_MIDSUMMER_SAMPLE, "r")
        docs = f.read()
        f.close()
        
        l = Letter()
        l.add_page("12", "1", docs)
        
        #transform the sample to vector representation
        dictionary = c.get_dict()
        vec_bow = dictionary.doc2bow(l.get_txt())
       
        mmcorpus = corpora.MmCorpus(path) 
        tfidf = models.TfidfModel(mmcorpus) 
        corpus_tfidf = tfidf[mmcorpus]
        #vec_tfidf = tfidf[vec_bow]
        
        
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=3)
        #sample_tfidf = models.TfidfModel(docs)
        vec_lsi = lsi[vec_bow]
        print vec_lsi
        
        #for item in mmcorpus:
            #print item
        sims = doc_similarity(vec_lsi, lsi, mmcorpus)
        print sims
        print corpus_ids
        for num, item in zip(corpus_ids, sims):
            print num, item
        
        #print sims # returns something else
        
        

if __name__ == "__main__":
    unittest.main()