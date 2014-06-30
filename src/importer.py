'''
Created on 16 May 2014

@author: Bleier
'''
import xlrd, os
import datetime
import cProfile
from helper import item_to_pickle
from txt_classes import TxtItem, TxtCorpus

def make_text_corpus(texts, file_path, corpus_file_name=None, corpus_dict_name=None, corpus_vect_name=None):
    
    if not corpus_file_name:
        corpus_file_name = "text_corpus.pickle"
    
    item_to_pickle(file_path + os.sep + corpus_file_name, texts) 
    corpus = TxtCorpus(file_path + os.sep + corpus_file_name)
    #make a dictionary of the words in the corpus
    if not corpus_dict_name:
        corpus_dict_name = file_path + os.sep + "text_corpus.dict"
    if not corpus_vect_name:
        corpus_vect_name = file_path + os.sep + "text_vect_corpus.pickle"
    corpus.add_vector_corpus_and_dictionary(corpus_vect_name, corpus_dict_name)
    return corpus

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

def txt_to_object(file_name, txt_id, page, nr):
    f = open(file_name, "r")
    txt = f.read()
    f.close()
    t = TxtItem()
    t.add_attr("file", file_name)
    t.add_attr("Letter", file_name)
    t.add_page(page, nr, txt) # add also pagenumber and timestamp before the string!
    t.unique_name = txt_id
    return t

def get_texts_from_files(dir_path, corpus_dir, file_ext=".txt", corpus_file_name=None, corpus_dict_name=None, corpus_vect_name=None):
    """
    Given a directory path and a file path the function gets first a list of text files form the location 'dir_path'
    The text of each text file will be stored in a TxtItem instance, and the instance will be stored in a list
    The list will be pickled to 'corpus_file_path' and TxtCorpus created that uses this pickle file as source data
    The TxtCorpus will be returned
    """
    documents = get_text_files(dir_path, file_ext)
    texts = []
    for idx, item in enumerate(documents):
        txt_id = str(idx)+"_"+item
        t = txt_to_object(dir_path + os.sep + item, txt_id, "1", "12")
        texts.append(t)
    corpus = make_text_corpus(texts, corpus_dir, corpus_file_name, corpus_dict_name, corpus_vect_name)
    return corpus

def get_texts_from_Excel(file_name_excel, corpus_dir, corpus_file_name=None, corpus_dict_name=None, corpus_vect_name=None):
    """
    The function gets data from an Excel file and turn it into a TxtCorpus
    The parameter file_name_excel is a valid file path to an excel file containing texts and metadata
    The function returns a TxtCorpus
    """
    #Creates an object of type Book from xlrd.book object
    wb = xlrd.open_workbook(filename=file_name_excel, encoding_override="utf-8")
    sheet = wb.sheet_by_index(0)
    texts = []
    text_location = {}
    for row in range(1,sheet.nrows):
        row_dict = {}
        for col in range(sheet.ncols):
            if sheet.cell(row,col).ctype == 3: # 1 is type text, 3 xldate
                date_tuple = xlrd.xldate_as_tuple(sheet.cell_value(row,col), wb.datemode)
                date_py = datetime.datetime(*date_tuple)
                row_dict.update({sheet.cell_value(0,col): date_py}) # a datetime.datetime obj is stored
            else:
                row_dict.update({sheet.cell_value(0,col):sheet.cell_value(row,col)})
        t = TxtItem(**row_dict)
        t.unique_name = t.Letter
        if t.unique_name not in text_location:
            t.add_page(t.Page, t.Translation_Timestamp, t.Translation) #note: has to be tested if attributes are correctly imported!
            texts.append(t)
            text_location[t.unique_name] = len(texts)-1
        else:
            # l.Translation - 'Translation' is the name that was given to the column in the Excel file - if the name changes the attribute will change too
            texts[text_location[t.unique_name]].add_page(t.Page, t.Translation_Timestamp, t.Translation)
    corpus = make_text_corpus(texts, corpus_dir, corpus_file_name, corpus_dict_name, corpus_vect_name)
    corpus.add_attr("text_location", text_location)
    return corpus


if __name__ == "__main__":
    pass
    #tests the import_letters function and get_letters function, from the get_letters function a list of letter.Letter items should be returned
    #cProfile.run('get_letters_from_Excel('+FULL_LETTERS_EXCEL+')', 'tmp' + os.sep + 'importer_stats')
    #cProfile.run('make_text_corpus('+FULL_LETTERS_EXCEL+')')
