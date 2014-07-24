# -*- coding: utf-8 -*-
'''
Created on 13 May 2014

This module contains the letter class
@author: Bleier
'''
from helper import item_to_pickle, item_from_pickle
import os, codecs, shutil
from gensim.corpora import Dictionary
from helper import replace_problem_char

class Bunch(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                raise AttributeError("API conflict: '%s' is part of the '%s' API" % (key, self.__class__.__name__))
            else:
                setattr(self, key, value)


class TxtItem(Bunch):
    def __init__(self, unique_name, *args, **kwargs):
        super(TxtItem, self).__init__(*args, **kwargs)
        self.unique_name = unique_name
    
    def get_dict(self):
        txt = self.get_txt()
        dict = {}
        for item in txt:
            if item not in dict:
                dict[item] = 1
            if item in dict:
                dict[item] += 1
        return dict
    
    def get_id(self):
        """Returns the ID / unique name of the current TxtItem"""
        return self.unique_name
       
    def add_attr(self, name, value):
        """After checking if such an attribute does not yet exist, adds a single attribute to the object.
        If the attribute name is already used an error is thrown
        """
        if hasattr(self, name):
            raise AttributeError("API conflict: '%s' is already part of the '%s' API" % (name, self.__class__.__name__))
        else:
            setattr(self, name, value)

class TxtItemLetterExcel(TxtItem):
    """
    This customization of the TxtItem class allows for the storage and retrieval of multi-page letters (for the Excel data file of the 1916 letters project),
     with multiple edits distinguished by timestamps.
    """
    def __init__(self, *args, **kwargs):
        super(TxtItemLetterExcel, self).__init__(*args, **kwargs)
        self.pages = {}
        
    def add_page(self, page_nr, time_stamp, strg): 
        """Adds a page to the dict self.pages. A page number, timestamp and a string are expected as arguments.        
        """
        if page_nr in self.pages:
            self.pages[page_nr].append((time_stamp, strg))
        else:
            self.pages.update({page_nr:[(time_stamp, strg)]})
            
    def get_pages(self):
        return self.pages
    
    def add_txt_file(self, file_path, file_name):
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        with codecs.open(file_path + os.sep + file_name, "w", "utf-8") as f:
            t = " ".join(self.get_txt())
            t = replace_problem_char(t)
            f.write(t)
        self.txt_file_path = file_path + os.sep + file_name
        
        txt = []
        for key, page in self.pages.items():
            most_recent_txt = sorted(page, reverse=True)[0][1]
            txt += most_recent_txt.lower().split()
        return txt
    
    def get_txt(self):
        """
        Returns the list of pages of letter text. Each page is a list of word tokens
        Returned: self.txt
        """
        if hasattr(self, "txt_file_path"):
            with codecs.open(self.txt_file_path, "r", "utf-8") as f:
                txt = f.read().lower().split()
        else:
            txt = []
            for key, page in self.pages.items():
                most_recent_txt = sorted(page, reverse=True)[0][1]
                txt += most_recent_txt.lower().split()
        return txt
    
class TxtItemTextFile(TxtItem):
    """
    This customization of the TxtItem class allows for the storage and retrieval of multi-page letters (for the Excel data file of the 1916 letters project),
     with multiple edits distinguished by timestamps.
    """
    def __init__(self, txt_filename, *args, **kwargs):
        super(TxtItemTextFile, self).__init__(*args, **kwargs)
        self.txt_file_path = txt_filename
        
    def add_new_filepath(self, filepath): 
        """Adds a new file path.        
        """
        #tests if path already exists, if yes the attribute will be assigned the new filepath
        if os.path.isfile(filepath):
            self.txt_file_path = filepath
        #tests if the directory already exists, if not it will be created
        dirname = os.path.dirname(filepath)
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        self.make_file_copy(filepath)
        self.txt_file_path = filepath
            
    def make_file_copy(self, new_filepath):
        shutil.copyfile(self.txt_file_path, new_filepath)
    
    def get_txt(self):
        """
        Returns the list of pages of letter text. Each page is a list of word tokens
        Returned: self.txt
        """
        if hasattr(self, "txt_file_path"):
            with codecs.open(self.txt_file_path, "r", "utf-8") as f:
                txt = f.read().lower().split()
            return txt
        else:
            raise AttributeError

class TxtCorpus(object):
    def __init__(self, file_name):
        self.file = file_name
    
    def __iter__(self):
        for item in item_from_pickle(self.file):
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            yield item.get_txt() 
            
    def get_txtitems(self):
        items = []
        for item in item_from_pickle(self.file):
            items.append(item)
        return items
            
    def get_tokens(self):
        words = []
        for item in item_from_pickle(self.file):
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            words.append(item.get_txt())
        return words 
            
    def add_attr(self, name, value):
        """After checking if such an attribute does not yet exist, adds a single attribute to the object.
        If the attribute name is already used an error is thrown
        """
        if hasattr(self, name):
            raise AttributeError("API conflict: '%s' is already part of the '%s' API" % (name, self.__class__.__name__))
        else:
            setattr(self, name, value)
            
    def get_dictionary(self):
        if hasattr(self, "dict_path"):
            return item_from_pickle(self.dict_path)
        else:
            raise AttributeError("No attribute with the name dict_path found.")
        
    def get_vector_corpus(self):
        if hasattr(self, "vector_corpus"):
            return item_from_pickle(self.vector_corpus)
        else:
            raise AttributeError("No attribute with the name dict_path found.")
        
    def add_vector_corpus_and_dictionary(self, vec_corpus_file, dict_file):
        """
        Method that adds a vector corpus: documents represented as sparse vectors
        and a dictionary out of the words in the docs in the corpus
        vec_corpus_file is path where the vector corpus file will be stored
        dict_file is the path where the dictionary will be stored
        """
        texts = self.get_tokens()
        #remove all the token that exist only once
        all_tokens = sum(texts, [])
        tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
        texts = [[word for word in text if word not in tokens_once]
                 for text in texts]
        d = Dictionary(texts)
        #d.filter_extremes(no_below=10)
        item_to_pickle(dict_file, d)
        self.add_attr("dict_path", dict_file)
        dictionary = self.get_dictionary()
        #returns a list of tuples of (id, text)
        texts = self.get_tokens() 
        vec_corpus = [dictionary.doc2bow(text) for text in texts] 
        item_to_pickle(vec_corpus_file, vec_corpus)
        if hasattr(self, "vector_corpus"):
            self.vector_corpus = vec_corpus_file
        else:
            self.add_attr("vector_corpus", vec_corpus_file)
        
    
                
    def number_of_txts(self):
        return len(self.get_vector_corpus())

