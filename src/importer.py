'''
Created on 16 May 2014

@author: Bleier
'''
import xlrd, os
import datetime
import cProfile
from helper import item_to_pickle
from letter_classes import Letter, TxtCorpus
from gensim.corpora import Dictionary
from settings import *

def get_text_files(dir, ext):
    """
    given a directory path the function returns a list of files in this directory
    the second parameter 'ext' is a string containing the file extension of the files that should be returned, e.g. ".txt"
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(ext):
            files.append(file)         
    return files

def txt_to_object(file_name, page, nr):
    f = open(file_name, "r")
    txt = f.read()
    #print txt
    f.close()
    l = Letter()
    l.add_attr("file", file_name)
    l.add_attr("Letter", file_name)
    l.add_page(page, nr, txt) # add also pagenumber and timestamp before the string!
    return l
    

def get_text_from_txt(path_name, corpus_file_path):
    """
    The function gets first a list of text files form the location 'path_name'
    The text of each text file will be stored in an Letter obj., and the object will itself be stored in a dictionary
    The dictionary will be pickled to 'corpus_file_path' and TxtCorpus created that uses this pickle file as source data
    The TxtCorpus will be returned
    """
    documents = get_text_files(path_name, ".txt")
    letters = []
    for idx, item in enumerate(documents):
        l = txt_to_object(path_name + os.sep + item, "1", "12")
        txt_id = str(idx)+"_"+item
        l.add_attr("id", txt_id)
        letters.append(l)
        
    corpus_file_name = corpus_file_path + os.sep + "text_corpus.pickle"
    item_to_pickle(corpus_file_name, letters) 
    corpus = TxtCorpus(corpus_file_name)
    #make a dictionary of the words in the corpus
    corpus_dict_name = corpus_file_path + os.sep + "text_corpus.dict"
    corpus_vect_name = corpus_file_path + os.sep + "text_vect_corpus.pickle"
    make_vector_corpus_and_dictionary(corpus, corpus_vect_name, corpus_dict_name)
    return corpus
        
    
        

def get_letters_from_Excel(file_path):
    """
    The parameter file_path is a valid file path to an excel file containing letter transcriptions and metadata
    The function returns a dictionary of letter transcriptions
    The dictionary is stored in a shelve file
    """
    #Creates an object of type Book from xlrd.book object
    wb = xlrd.open_workbook(filename=file_path, encoding_override="utf-8")
    sheet = wb.sheet_by_index(0)
    letters = []
    for row in range(1,sheet.nrows):
        row_dict = {}
        for col in range(sheet.ncols):
            if sheet.cell(row,col).ctype == 3: # 1 is type text, 3 xldate
                date_tuple = xlrd.xldate_as_tuple(sheet.cell_value(row,col), wb.datemode)
                date_py = datetime.datetime(*date_tuple)
                row_dict.update({sheet.cell_value(0,col): date_py}) # a datetime.datetime obj is stored
            else:
                row_dict.update({sheet.cell_value(0,col):sheet.cell_value(row,col)})
        l = Letter(**row_dict)
        txt_id = l.get_id()
        for item in letters:
            if txt_id == item.get_id():
                # l.Translation - 'Translation' is the name that was given to the column in the Excel file - if the name changes the attribute will change too
                item.add_page(l.Page, l.Timestamp_, l.Translation)
            else:
            # l.Translation - 'Translation' is the name that was given to the column in the Excel file - if the name changes the attribute will change too
                l.add_page(l.Page, l.Timestamp_, l.Translation)
                letters.append(l)
    #return dictionary of letter transcriptions
    return letters, wb

def make_vector_corpus_and_dictionary(txt_corpus, vec_corpus_file, dict_file):
    """
    Function to create a vector corpus: documents represented as sparse vectors
    and a dictionary out of the words in the docs
    docs is a list of documents, each document is a list of words
    file_path is the file path where the mmcorpus will be saved
    """
    #get tokens returns a tuple of document id and text
    d = Dictionary([i[1] for i in txt_corpus.get_tokens()])
    item_to_pickle(dict_file, d)
    txt_corpus.add_attr("dict_path", dict_file)
    dictionary = txt_corpus.get_dict()
    #returns a list of tuples of (id, text)
    id_and_text = txt_corpus.get_tokens() 
    texts = []
    text_ids = []
    for text_id, text in id_and_text:
        texts.append(text)
        text_ids.append(text_id)
    vec_corpus = [dictionary.doc2bow(text) for text in texts] 
    item_to_pickle(vec_corpus_file, vec_corpus)
    txt_corpus.add_attr("vector_corpus", vec_corpus_file)
    
    txt_corpus.add_attr("corpus_id_map", text_ids)


def make_text_corpus(excel_file, corpus_file_path):
    
    dict_of_Letters, wb = get_letters_from_Excel(excel_file)
    item_to_pickle(corpus_file_path, dict_of_Letters) 
    return TxtCorpus(corpus_file_path)



if __name__ == "__main__":
    #tests the import_letters function and get_letters function, from the get_letters function a list of letter.Letter items should be returned
    cProfile.run('get_letters_from_Excel('+FULL_LETTERS_EXCEL+')', 'tmp' + os.sep + 'importer_stats')
    cProfile.run('make_text_corpus('+FULL_LETTERS_EXCEL+')')
