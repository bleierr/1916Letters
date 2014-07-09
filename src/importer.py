'''
Created on 16 May 2014

@author: Bleier
'''
import xlrd, os
import datetime
import shutil
from helper import item_to_pickle, get_text_files
from txt_classes import TxtItem, TxtCorpus
from settings import TIMESTAMP_COL, TRANSCRIPTION_COL, TXT_ID, PAGE_COL

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

def get_texts_from_files(dir_path, corpus_dir, file_ext=".txt"):
    """
    Given a directory path and a file path the function gets first a list of text files form the location 'dir_path'
    The text of each text file will be stored in a TxtItem instance, and the instance will be stored in a list
    The list will be pickled to 'corpus_file_path' and TxtCorpus created that uses this pickle file as source data
    The TxtCorpus will be returned
    """
    documents = get_text_files(dir_path, file_ext)
    text_location_dict = {}
    texts = []
    for idx, file_path in enumerate(documents):
        unique_name = str(idx)+"_"+file_path
        t = TxtItem(unique_name, file_path)
        file_path = corpus_dir + os.sep + "txt"
        file_name = unique_name + ".txt"
        t.add_txt_file(file_path, file_name)
        texts.append(t)
        try:
            #dictionary to map text ids with object location - for quick access of individual items
            text_location_dict[unique_name] = len(texts)-1
        except KeyError: ("Error: The unique name for the object is already used. The imported text files seem to have the same name.")
    return texts, text_location_dict

def get_texts_from_Excel(file_name_excel, corpus_dir):
    """
    The function gets data from an Excel file and turn it into a TxtCorpus
    The parameter file_name_excel is a valid file path to an excel file containing texts and metadata
    The function returns a TxtCorpus
    """
    #Creates an object of type Book from xlrd.book object
    wb = xlrd.open_workbook(filename=file_name_excel, encoding_override="utf-8")
    sheet = wb.sheet_by_index(0)
    texts = []
    text_location_dict = {}
    for row in range(1,sheet.nrows):
        row_dict = {}
        for col in range(sheet.ncols):
            if sheet.cell(row,col).ctype == 3: # 1 is type text, 3 xldate
                date_tuple = xlrd.xldate_as_tuple(sheet.cell_value(row,col), wb.datemode)
                date_py = datetime.datetime(*date_tuple)
                row_dict.update({sheet.cell_value(0,col): date_py}) # a datetime.datetime obj is stored
            else:
                row_dict.update({sheet.cell_value(0,col):sheet.cell_value(row,col)})
        unique_name = str(row_dict[TXT_ID])
        t = TxtItem(unique_name, **row_dict)
        
        if t.unique_name not in text_location_dict:
            t.add_page(getattr(t, PAGE_COL), getattr(t, TIMESTAMP_COL), getattr(t, TRANSCRIPTION_COL)) #note: has to be tested if attributes are correctly imported!
            texts.append(t)
            #dictionary to map text ids with object location - for quick access of individual items
            text_location_dict[t.unique_name] = len(texts)-1
        else:
            # l.Translation - 'Translation' is the name that was given to the column in the Excel file - if the name changes the attribute will change too
            texts[text_location_dict[t.unique_name]].add_page(getattr(t, PAGE_COL), getattr(t, TIMESTAMP_COL), getattr(t, TRANSCRIPTION_COL))
        file_path = corpus_dir + os.sep + "txt"
        file_name = unique_name + ".txt"
        t.add_txt_file(file_path, file_name)
    return texts, text_location_dict

if __name__ == "__main__":
    file_name_excel = "test_data" + os.sep + "all_transcriptions_until_16_06_2014.xlsx"
    corpus_dir = "test_data_excel"
    if os.path.isdir(corpus_dir):
            shutil.rmtree(corpus_dir)
    os.mkdir(corpus_dir)
    texts, id2texts = get_texts_from_Excel(file_name_excel, corpus_dir) 
    corpus = make_text_corpus(texts, corpus_dir) 
    item_to_pickle(corpus_dir +os.path.sep + "corpusfile.pickle", corpus)

