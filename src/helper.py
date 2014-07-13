#-*- coding: utf-8 -*-
'''
Created on 13 May 2014

@author: Bleier
'''
from __future__ import division
import re, os
import cProfile
import shelve
import cPickle as pickle
from settings import STOPWORD_LST


def replace_problem_char(strg):
    for pat, repl in [("é", "e"), ("’", "'"),("À", "A")]:
        expr = re.compile(pat)
    return expr.sub(repl, strg)


def item_to_shelve(shelve_file, item, name):
    d = shelve.open(shelve_file)
    d[name] = item
    d.close()


def item_from_shelve(shelve_file, name):
    d = shelve.open(shelve_file)
    corpus = d[name]
    d.close()
    return corpus

def item_to_pickle(file_name, item):
    pickle.dump( item, open( file_name, "wb" ) )
    
def item_from_pickle(file_name):
    return pickle.load( open( file_name, "rb" ) )


def lexical_diversity(text):
    """
    Calculates the lexical diversity of a nltk text object
    """
    return len(text)/ len(set(text))

def percentage(count, total):
    """
    Given the two parameters count and total it returns the percentage count of total
    """
    return 100 * count / total

def txt_no_hapax_no_stopwords(docs):
    
    #remove items in stopword list (might not be necessary if it has been done in previous step)
    texts = [[word.lower() for word in document if word.lower() not in STOPWORD_LST]
         for document in docs]

    all_tokens = sum(texts, [])
    #print(all_tokens)
    
    #remove all the token that exist only once
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
             for text in texts]

def get_text_files(filedir, ext):
    """
    given a directory path the function returns a list of files in this directory
    the second parameter 'ext' is a string containing the file extension of the files that should be returned, e.g. ".txt"
    """
    files = []
    for file in os.listdir(filedir):
        if file.endswith(ext):
            files.append(file)         
    return files    


            
def replace_strg(strg, lst):
    """
    Takes a string argument and cleans it of instances in list 'lst' 
    lst is a list of tuples containing a character or string and its replacement
    """
    cleanStrg = ""
    for item, repl in lst:
        cleanStrg += strg.replace(item, repl)
    return cleanStrg



    
