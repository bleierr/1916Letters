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

def get_text_files(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".txt"):
            files.append(file)         
    return files

def txt_to_object(file_name, page, nr):
    f = open(file_name, "r")
    txt = f.read()
    f.close()
    l = Letter()
    l.add_attr("file", file_name)
    l.add_attr("Letter", file_name)
    l.add_page(page, nr, txt) # add also pagenumber and timestamp before the string!
    return l
    

def get_text_from_txt(path_name, corpus_file_path):
    """
    Gets text from an txt file and imports it, creating a letters file with all the text documents in it
    """
    documents = get_text_files(path_name)
    letters = {}
    for idx, item in enumerate(documents):
        l = txt_to_object(TEST_SHAKESPEAR_DIR + os.sep + item, "1", "12")
        letters[str(idx)+"_"+item] = l
        
    item_to_pickle(corpus_file_path, letters) 
    corpus = TxtCorpus(corpus_file_path)
    #make_word_dictionary(corpus, TEST_SHAKESPEAR_DICT)
    #make_vector_corpus(corpus, TEST_SHAKESPEAR_VECTOR_CORPUS)
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
    letters = {}
    
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
        name = l.get_id()
        if name not in letters:
            letters[name] = l
        # l.Translation - 'Translation' is the name that was given to the column in the Excel file - if the name changes the attribute will change too
        letters[name].add_page(l.Page, l.Timestamp_, l.Translation)
    #return dictionary of letter transcriptions
    return letters, wb

def make_vector_corpus(txt_corpus, vec_corpus_file):
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

def make_word_dictionary(txt_corpus, dict_file):
    l = []
    #get tokens returns a tuple of document id and text
    for item in txt_corpus.get_tokens():
        l.append(item[1])
    
    d = Dictionary(l)
    item_to_pickle(dict_file, d)
    txt_corpus.add_attr("dict_path", dict_file)


def make_text_corpus(excel_file, corpus_file_path):
    
    dict_of_Letters, wb = get_letters_from_Excel(excel_file)
    item_to_pickle(corpus_file_path, dict_of_Letters) 
    return TxtCorpus(corpus_file_path)



if __name__ == "__main__":
    #tests the import_letters function and get_letters function, from the get_letters function a list of letter.Letter items should be returned
    cProfile.run('get_letters_from_Excel('+FULL_LETTERS_EXCEL+')', 'tmp' + os.sep + 'importer_stats')
    cProfile.run('make_text_corpus('+FULL_LETTERS_EXCEL+')')
