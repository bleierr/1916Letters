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

TEST_SAMPLE_DIR = "test_data" + os.sep + "txt" + os.sep + "shakespear" + os.sep + "samples"
TEST_SHAKESPEAR_DIR = "test_data" + os.sep + "txt" + os.sep + "shakespear" + os.sep + "texts"
#TEST_RICHARDIII_TRAG = "test_data" + os.sep + "txt" + os.sep + "shakespear_trag_richardIII.txt"
#TEST_MIDSUMMER_COM = "test_data" + os.sep + "txt" + os.sep + "shakespear_comedy_midsummernight.txt"
#TEST_ERRORS_COM = "test_data" + os.sep + "txt" + os.sep + "shakespear_comedy_errors.txt"
#TEST_MACBETH_TRAG = "test_data" + os.sep + "txt" + os.sep + "shakespear_trag_macbeth.txt"
TEST_SHAKESPEAR_CORPUS = "tmp" + os.sep + "txt" + os.sep + "shakespear_corpus.pickle"
TEST_SHAKESPEAR_DICT = "tmp" + os.sep + "txt" + os.sep + "shakespear_word.dict"
TEST_SHAKESPEAR_VECTOR_CORPUS = "tmp" + os.sep + "txt" + os.sep + "shakespear_vector_corpus.pickle"


FULL_LETTERS_EXCEL = "test_data"+ os.sep + "1916letters_all_latest_translations.xlsx"
FULL_LETTERS_CORPUS = "tmp" + os.sep + "full_letters.pickle" 

STOPWORD_LST = corpus.stopwords.words("english") + ["&", "&amp;"] + "conj om i'll th 's and. hee mee thee thy thou o".split()
"""richard bolingbroke buckingham york elizabeth aumerle hastings gloucester macbeth lear 
demetrius lysander hermia syracuse dromio antipholus ephesus adriana luciana demetrius 
angelo macduff theseus kent albaumerle gaunt catesby anne"""

#CLEANING_PATTERN = [("no-group", "<[/\w\d\s\"\'=]+>|<!--[/\w\d\s\"\'=.,-]+-->"), ("use-group", "[\W]*(\w+[\w\'-/.]*\w+|\w|&)[\W]*") ] # 1916 letter cleaning pattern

CLEANING_PATTERN = [("no-group", "<[/\w\d\s\"\'=]+>|<!--[/\w\d\s\"\'=.,-]+-->"), 
                    ("no-group", "\[A-Z]+[\s\.]+"), # Names and comments in some plays
                    ("use-group", "[\W]*(\w+[\'-/.]*\w+|[a-zA-Z]|&)[\W]*"),
                    ("no-group", "\[[\w\s\d]*\]"),
                    ("no-group", "[A-Z]\w+"), #names and place names
                    ("no-group", "\s[\[\]\'\"\-_<>.;,?!:\(\)]+\s"),
                    ("no-group", "_"), # remove underscore before a word
                    ("no-group", "\s\d+\s") #get rid of numbers
                    ] # Shakespear test cleaning pattern


