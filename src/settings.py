'''
Created on 13 May 2014

@author: Bleier
'''
import os
from nltk import corpus

TIMESTAMP = True
TIMESTAMP_COL = "Timestamp_"
PAGE_COL = "Page"
TRANSCRIPTION_COL = "Translation"
TXT_ID = "Letter"


shakespear_add_stopwords = """richard bolingbroke buckingham york elizabeth aumerle hastings gloucester macbeth lear 
demetrius lysander hermia syracuse dromio antipholus ephesus adriana luciana demetrius 
angelo macduff theseus kent albaumerle gaunt catesby anne conj om i'll th 's and. hee mee thee thy thou o""".split()

STOPWORD_LST = corpus.stopwords.words("english") + ["&", "&amp;"] + "cadogan gdns amp 0 1 2 3 4 5 6 7 8 9 may would one dear shall mr a b c d e f g h i j k l m n o p q r s t x y z".split() #+ shakespear_add_stopwords


#standard cleaning pattern
CLEANING_PATTERN = [("no-group", "<[/\w\d\s\"\'=]+>|<!--[/\w\d\s\"\'=.,-]+-->"),
                    ("no-group", "&[#\w\d]+;"), 
                    ("use-group", "[\W]*(\w+[\w\'-/.]*\w+|\w|&)[\W]*")
                     ] # 1916 letter cleaning pattern

"""CLEANING_PATTERN = [("no-group", "<[/\w\d\s\"\'=]+>|<!--[/\w\d\s\"\'=.,-]+-->"), 
                    ("no-group", "\[A-Z]+[\s\.]+"), # Names and comments in some plays
                    ("use-group", "[\W]*(\w+[\'-/.]*\w+|[a-zA-Z]|&)[\W]*"),
                    ("no-group", "\[[\w\s\d]*\]"),
                    ("no-group", "[A-Z]\w+"), #names and place names
                    ("no-group", "\s[\[\]\'\"\-_<>.;,?!:\(\)]+\s"),
                    ("no-group", "_"), # remove underscore before a word
                    ("no-group", "\s\d+\s") #get rid of numbers
                    ] # Shakespear test cleaning pattern
                    """
                    


