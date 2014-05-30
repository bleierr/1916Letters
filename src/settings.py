'''
Created on 13 May 2014

@author: Bleier
'''
import os
from nltk import corpus

#TESTS

TEST_EXCEL = "test_data"+ os.sep + "test_1916Letters.xlsx"
TEST_CORPUS = "tmp"+ os.sep + "test_corpus.pickle"
TEST_WORD_DICT = "tmp" + os.sep + "test_word.dict"
TEST_VECTOR_CORPUS = "tmp" + os.sep + "test_vector_corpus.pickle"


FULL_LETTERS_EXCEL = "test_data"+ os.sep + "1916letters_all_latest_translations.xlsx"
FULL_LETTERS_CORPUS = "tmp" + os.sep + "full_letters.pickle" 

STOPWORD_LST = corpus.stopwords.words("english") + ["&", "&amp;"]
