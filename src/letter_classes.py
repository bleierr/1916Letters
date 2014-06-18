'''
Created on 13 May 2014

This module contains the letter class
@author: Bleier
'''
from helper import clean_txt, item_to_pickle, item_from_pickle
import cProfile, os
from settings import STOPWORD_LST

class Bunch(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                raise AttributeError("API conflict: '%s' is part of the '%s' API" % (key, self.__class__.__name__))
            else:
                setattr(self, key, value)


class Letter(Bunch):
    def __init__(self, *args, **kwargs):
        super(Letter, self).__init__(*args, **kwargs)
        self.pages = {}
        
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
        txt = []
        
        for key, page in self.pages.items():
            most_recent_txt = sorted(page, reverse=True)[0][1]
            txt += clean_txt(most_recent_txt)                
        return [w for w in txt if w not in STOPWORD_LST]
    
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
        """Returns the ID of the current letter object"""
        return self.Letter
    
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
        for key, item in item_from_pickle(self.file).items():
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            yield item.get_txt() 
            
    def get_letters(self):
        for key, item in item_from_pickle(self.file).items():
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            yield item
            
    def get_tokens(self):
        for key, item in item_from_pickle(self.file).items():
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            yield key, [w for w in item.get_txt() if w not in STOPWORD_LST] 
            
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
            return self.corpus_id_map, item_from_pickle(self.vector_corpus)
        else:
            raise AttributeError("No attribute with the name dict_path found.")
        
    def get_ids(self):
        for key in item_from_pickle(self.file).keys():
            # returns the transcriptions stored as lists of pages and word token from the letter object's txt attribute
            yield key
        
            
            


        

if __name__ == "__main__":
    xml_data = """<p><s>It's time to go to <place>school</place>.</s>
                <s>This piece of xml is from <name>letter.py</name>.</s></p>"""
                
    xml_data2 = """<p><s>Go> <place>home</place>.<!-- comment--></s>
                <s>What? No. text_file _ -ok.</s></p>"""
                
    def test():
        L1 = Letter(**{"Publisher" : "publ", "House": "my house"})
        L1.add_page(xml_data)
        L1.add_page(xml_data2)
        L1.add_attr("xml", "This is a test")
        item_to_pickle("tmp" + os.sep + "corpus.pickle", {"Letter1": L1})
        print(L1.Publisher)
    
    #test()
    C = TxtCorpus("tmp" + os.sep + "corpus.shelve")
    for item in C:
        print(item)
    print(C)
    #cProfile.run("test()")
    