'''
Created on 13 May 2014

@author: Bleier
'''
import os
from nltk import corpus


TIMESTAMP = True
TIMESTAMP_COL = "Translation_Timestamp" #"Timestamp_"
PAGE_COL = "Page"
TRANSCRIPTION_COL = "Translation"
TXT_ID = "Letter"
"""
#following is the setting for the unittest file test_importer.py
#To run the unittest use these settings
TIMESTAMP = True
TIMESTAMP_COL = "Timestamp"
PAGE_COL = "Page"
TRANSCRIPTION_COL = "Text"
TXT_ID = "Text_ID"
"""

NODES_FILE = [()]

EDGES_FILE = [()]

shakespear_add_stopwords = """richard bolingbroke buckingham york elizabeth aumerle hastings gloucester macbeth lear 
demetrius lysander hermia syracuse dromio antipholus ephesus adriana luciana demetrius 
angelo macduff theseus kent albaumerle gaunt catesby anne conj om i'll th 's and. hee mee thee thy thou o""".split()

STOPWORD_LST = corpus.stopwords.words("english") + ["&", "&amp;"] 
STOPWORD_FILE = "letters_stopwords.txt" #if not stopword file is used 'None' has to be added

SPELL_CHECK_PWL = "letters_pwl.txt" #if no personal word list is used the variable has to be set to 'None'

#standard cleaning pattern
CLEANING_PATTERN = [("no-group", "<unclear>questionable reading</unclear>"), # appeared in letter 1004 several times
                    ("no-group", "<[/\w\d\s\"\'=]+>|<!--[/\w\d\s\"\'=\.,-]+-->"),
                    ("no-group", "[\d\.]+[ap]m"), #remove times e.g. 5pm or 4.30pm
                    ("no-group", "\'s"), #remove Gen. 's' e.g. Paul's
                    ("no-group", "[\d/'\.]+"),
                    ("no-group", "\s(\w\.)+\s"),
                    ("no-group", "&[#\w\d]+;"), 
                    ("use-group", "[\W]*(\w+[\w\'-/\.]*\w+|\w|&)[\W]*")
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
                    


