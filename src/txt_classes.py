'''
Created on 13 May 2014

This module contains the letter class
@author: Bleier
'''
from helper import item_to_pickle, item_from_pickle
import os
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
        self.pages = {}
        self.unique_name = unique_name
        
    def add_page(self, page_nr, time_stamp, strg): #think about a generalis. of importer???
        """adds a page to self.txt, 
        a string parameter is expected that will be cleaned of xml markup and transformed into a list
        of word tokens"""
        #self.txt += clean_txt(strg)
        if page_nr in self.pages:
            self.pages[page_nr].append((time_stamp, strg))
        else:
            self.pages.update({page_nr:[(time_stamp, strg)]})
                 
    def get_txt(self):
        """
        Returns the list of pages of letter text. Each page is a list of word tokens
        Returned: self.txt
        """
        if hasattr(self, "txt_file_path"):
            with open(self.txt_file_path) as f:
                txt = f.read().lower().split()
        else:
            txt = []
            for key, page in self.pages.items():
                most_recent_txt = sorted(page, reverse=True)[0][1]
                txt += most_recent_txt.lower().split()
        return [w for w in txt]
    
    def add_txt_file(self, file_path, file_name):
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        with open(file_path + os.sep + file_name, "w") as f:
            t = " ".join(self.get_txt())
            t = replace_problem_char(t).encode("utf-8")
            print t
            f.write(t)
        self.add_attr("txt_file_path", file_path + os.sep + file_name)
    
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
    
    def get_pages(self):
        return self.pages
         
    def add_attr(self, name, value):
        """After checking if such an attribute does not yet exist, adds a single attribute to the object.
        If the attribute name is already used an error is thrown
        """
        if hasattr(self, name):
            raise AttributeError("API conflict: '%s' is already part of the '%s' API" % (name, self.__class__.__name__))
        else:
            setattr(self, name, value)


class TxtCorpus(object):
    def __init__(self, file_name):
        self.file = file_name
    
    def __iter__(self):
        for item in item_from_pickle(self.file):
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            yield item.get_txt() 
            
    def get_txtitems(self):
        for item in item_from_pickle(self.file):
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            yield item
            
    def get_tokens(self):
        for item in item_from_pickle(self.file):
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            yield [w for w in item.get_txt()] 
            
    def add_attr(self, name, value):
        """After checking if such an attribute does not yet exist, adds a single attribute to the object.
        If the attribute name is already used an error is thrown
        """
        if hasattr(self, name):
            raise AttributeError("API conflict: '%s' is already part of the '%s' API" % (name, self.__class__.__name__))
        else:
            setattr(self, name, value)
            
    def get_dict(self):
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
        dictionary = self.get_dict()
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

