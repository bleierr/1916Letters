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
from settings import FULL_LETTERS_EXCEL


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
    texts = txt_corpus.get_tokens()
    vec_corpus = [dictionary.doc2bow(text) for text in texts]
    item_to_pickle(vec_corpus_file, vec_corpus)
    txt_corpus.add_attr("vector_corpus", vec_corpus_file)

def make_word_dictionary(txt_corpus, dict_file):
    l = []
    for item in txt_corpus.get_tokens():
        l.append(item)
    
    d = Dictionary(l)
    item_to_pickle(dict_file, d)
    txt_corpus.add_attr("dict_path", dict_file)


def make_text_corpus(excel_file, corpus_data_file):
    
    dict_of_Letters, wb = get_letters_from_Excel(excel_file)
    item_to_pickle(corpus_data_file, dict_of_Letters) 
    return TxtCorpus(corpus_data_file)



if __name__ == "__main__":
    #tests the import_letters function and get_letters function, from the get_letters function a list of letter.Letter items should be returned
    cProfile.run('get_letters_from_Excel('+FULL_LETTERS_EXCEL+')', 'tmp' + os.sep + 'importer_stats')
    cProfile.run('make_text_corpus('+FULL_LETTERS_EXCEL+')')
