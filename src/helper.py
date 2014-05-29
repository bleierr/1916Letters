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


def replace_problem_char(strg):
    repl = "'"
    pat = "’"
    expr = re.compile(pat)
    return expr.sub(repl, strg)

def strip_xml(strg):
    """
    Function gets rid of all xml like markup - strings enclosed in angle brackets will be deleted
    """
    pat = "<[/\w\d\s\"\'=]+>|<!--[/\w\d\s\"\'=.,-]+-->"
    expr = re.compile(pat)
    return ''.join(expr.split(strg)).strip()



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



def clean_txt(strg):
    """
    Strips xml markup from string, splits a string into word token, strips leading and trailing punctuation and white space
    Parameter strg is a string, the function returns a list of strings
    
    """
    lst_words = strip_xml(replace_problem_char(strg)).split()
    pat = "[\W]*(\w+[\w\'-/.]*\w+|\w|&)[\W]*"    #gets also rid of all &
    regex = re.compile(pat)
    clean_lst_words = []
    for item in lst_words:
        mm = regex.match(item)
        if mm:
            clean_lst_words.append(mm.group(1).lower())
    return clean_lst_words
            
            
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

    
