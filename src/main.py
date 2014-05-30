'''
Created on 23 May 2014
main.py: This is the main interface of the Letter 1916 Analyser

@author: Bleier
'''
from importer import make_text_corpus, make_word_dictionary, make_vector_corpus
import os
from helper import item_from_pickle
from settings import TEST_EXCEL, TEST_CORPUS, TEST_WORD_DICT, TEST_VECTOR_CORPUS




def main_dataimporter(excel_file, corpus_file, dict_file, vec_corpus_file):
    c = make_text_corpus(excel_file, corpus_file)   # the corpus_file is located on filepath corpus_file
    make_word_dictionary(c, dict_file)              # the word dictionary can be found on filepath dict_name
    d = item_from_pickle(dict_file)
    make_vector_corpus(c, vec_corpus_file)
    return c    #returns a corpus object
    

def main(excel_file, corpus_file, dict_file, vec_corpus_file):
    """
    The main function that starts the analysis process
    """
    
    c = main_dataimporter(excel_file, corpus_file, dict_file, vec_corpus_file)
    
    
    
    #returns a nltk freq dist obj
    #fdist_no_stop, total_words, most_freq_word, hapaxes = letter_analyser.make_analysis(letters)
    
        
    
    
if __name__ == "__main__":
    #main("1916letters_all_latest_translations.xlsx")
    main(TEST_EXCEL, TEST_CORPUS, TEST_WORD_DICT, TEST_VECTOR_CORPUS)