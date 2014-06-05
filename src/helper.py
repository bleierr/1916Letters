#-*- coding: utf-8 -*-
'''
Created on 13 May 2014

@author: Bleier
'''
from __future__ import division
import re
import cProfile
import shelve
import cPickle as pickle
from settings import STOPWORD_LST, CLEANING_PATTERN


def replace_problem_char(strg):
    repl = "'"
    pat = "’"
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
    

def clean_txt(strg):
    """
    Strips xml markup from string, splits a string into word token, strips leading and trailing punctuation and white space
    Parameter strg is a string, the function returns a list of strings
    
    """
    for type, pat in CLEANING_PATTERN:
        if type == "no-group":
            strg = "".join(re.split(pat , strg))
        elif type == "use-group":
            regex = re.compile(pat)
            lst = []
            for item in strg.split():
                mm = regex.match(item)
                if mm:
                    lst.append(mm.group(1))
            strg = " ".join(lst)
    return strg.lower().split()
            
            
def replace_strg(strg, lst):
    """
    Takes a string argument and cleans it of instances in list 'lst' 
    lst is a list of tuples containing a character or string and its replacement
    """
    cleanStrg = ""
    for item, repl in lst:
        cleanStrg += strg.replace(item, repl)
    return cleanStrg


if __name__ == "__main__":
    
    cProfile.run("strip_punct()")
    cProfile.run("clean_txt()")

    
