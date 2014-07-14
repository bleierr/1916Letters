'''
Created on 16 May 2014

@author: Bleier
'''
import xlrd, os, sys, getopt
import datetime
import shutil
from helper import item_to_pickle, get_text_files
from txt_classes import TxtItem, TxtCorpus, TxtItemLetterExcel, TxtItemTextFile
from settings import TIMESTAMP_COL, TRANSCRIPTION_COL, TXT_ID, PAGE_COL

def make_txt_corpus(texts, file_path, corpus_file_name=None, corpus_dict_name=None, corpus_vect_name=None):
    
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
    for idx, file_name in enumerate(documents):
        unique_name = file_name.split(".")[0]
        file_path_to_text_file = dir_path + os.sep + file_name
        t = TxtItemTextFile(file_path_to_text_file, unique_name)
        new_file_path = corpus_dir + os.sep + "txt" + os.sep + file_name
        t.add_new_filepath(new_file_path)
        
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
        t = TxtItemLetterExcel(unique_name, **row_dict)
        
        if t.unique_name not in text_location_dict:
            t.add_page(getattr(t, PAGE_COL), getattr(t, TIMESTAMP_COL), getattr(t, TRANSCRIPTION_COL)) #note: has to be tested if attributes are correctly imported!
            texts.append(t)
            #dictionary to map text ids with object location - for quick access of individual items
            text_location_dict[t.unique_name] = len(texts)-1
        else:
            # l.Translation - 'Translation' is the name that was given to the column in the Excel file - if the name changes the attribute will change too
            texts[text_location_dict[t.unique_name]].add_page(getattr(t, PAGE_COL), getattr(t, TIMESTAMP_COL), getattr(t, TRANSCRIPTION_COL))
    #add a txt file folder to each object
    file_path = corpus_dir + os.sep + "txt"
    for txt_item in texts:
        file_name = txt_item.unique_name + ".txt"
        txt_item.add_txt_file(file_path, file_name)
    return texts, text_location_dict


def main(mode, file_name_excel=None, corpus_dir=None, txt_dir_path=None):
    if not corpus_dir:
        current_dir = os.getcwd()
        corpus_dir = current_dir + os.sep + "corpus"
        print "No corpus directory was passed as argument. The corpus was created in {0}".format(corpus_dir)
        if os.path.isdir(corpus_dir):
            inp = raw_input("The directory already exists, shall it be overwritten?Y/N: ")
            if inp == "Y" or inp == "y":
                shutil.rmtree(corpus_dir)
                
            elif inp == "N" or inp == "n":
                return None
            else:
                print "Wrong input!"
                return None
        os.mkdir(corpus_dir)
    if mode == "excel":
        txtItems, id2texts = get_texts_from_Excel(file_name_excel, corpus_dir)
        item_to_pickle(corpus_dir + os.path.sep + "corpusfiles.pickle", txtItems)
    elif mode == "txt":
        txtItems, id2texts = get_texts_from_files(txt_dir_path, corpus_dir, file_ext=".txt")
        item_to_pickle(corpus_dir + os.sep + "corpusfiles.pickle", txtItems)
            

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "", ["mode=", "file_name_excel=", "corpus_dir=", "txt_dir_path="])
    print opts, args
    key_args = {}
    for key, value in opts:
        if key == "--mode":
            key_args["mode"] = value
        if key == "--file_name_excel":
            key_args["file_name_excel"] = value
        elif key == "--txt_dir_path":
            key_args["txt_dir_path"] = value
        if key == "--corpus_dir":
            key_args["corpus_dir"] = value
    main(**key_args)
