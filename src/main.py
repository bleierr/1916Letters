'''
Created on 23 May 2014
main.py: This is the main interface of the Letter 1916 Analyser

@author: Bleier
'''
from importer import *
import os
from helper import item_from_pickle
from settings import *
from analyser import make_lsi, doc_similarity
from outputter import prepare_output



def main_dataimporter(corpus_file_path, dict_file, vec_corpus_file, excel_file=None, path_name=None):
    if excel_file:
        c = make_text_corpus(excel_file, corpus_file_path) # the corpus_file is located on filepath corpus_file_path
    elif path_name:
        c = get_text_from_txt(path_name, corpus_file_path) # the corpus_file is located on filepath corpus_file_path
          
    make_word_dictionary(c, dict_file)              # the word dictionary can be found on filepath dict_name
    d = item_from_pickle(dict_file)
    make_vector_corpus(c, vec_corpus_file)
    return c    #returns a corpus object
    

def main_analyser(vector_corpus, dictionary, compare_texts):
    lsi, corpus_tfidf, topics = make_lsi(vector_corpus, dictionary)
    sims = []
    for text in compare_texts:
        vec_corpus = dictionary.doc2bow(text.get_txt())
        vec_lsi = lsi[vec_corpus]
        sims.append(doc_similarity(vec_lsi, lsi, vector_corpus))
    return topics, sims

def main(corpus_file_path, dict_file_path, vec_corpus_file_path, excel_file=None, path_name=None):
    """
    The main function that starts the analysis process
    """
    
    c = main_dataimporter(corpus_file_path, dict_file_path, vec_corpus_file_path, excel_file=excel_file, path_name=path_name)
    
    corpus_ids, vector_corpus = c.get_vector_corpus()
    dictionary = c.get_dict()
    
    
    
    
    compare_texts = []
    sample_files = [TEST_SAMPLE_DIR + os.sep + "sample_errors.txt"]
    for file_name in sample_files:
        compare_texts.append(txt_to_object(file_name, "page", "nr"))
    
    topics, sims = main_analyser(vector_corpus, dictionary, compare_texts)
    
    #prepare data for outputter
    data = [["file1.txt", "file2.txt"], 
        [u'0.501*"richard" + 0.413*"bolingbroke" + 0.285*"buckingham"', 
         u'0.227*"york" + 0.208*"elizabeth" + 0.201*"aumerle" + 0.184*"hastings"'],
        {"sample1.txt": ["file1.txt: 0.98", "file2.txt: 078"], "sample2.txt": ["file1.txt: 0.54", "file2.txt: 1.2"]}
        ]
    output_data = []
    if excel_file:
        output_data.append(excel_file)
    elif path_name:
        output_data.append(get_text_files(path_name))
    
    output_data.append(topics)
    
    sample_results = {}
    for sample_file, sim in zip(sample_files, sims):
        text_sim = []
        for file_name, sim_index in sorted(zip(corpus_ids, sim)):
            text_sim.append("{0}: {1}".format(file_name, sim_index))
        sample_results[sample_file] = text_sim
    output_data.append(sample_results)
    
    print prepare_output(output_data)
    print "Works okay!"
    #returns a nltk freq dist obj
    #fdist_no_stop, total_words, most_freq_word, hapaxes = letter_analyser.make_analysis(letters)
    
        
    
    
if __name__ == "__main__":
    #main("1916letters_all_latest_translations.xlsx")
    #main(TEST_EXCEL, TEST_CORPUS, TEST_WORD_DICT, TEST_VECTOR_CORPUS)
    main(TEST_SHAKESPEAR_CORPUS, TEST_SHAKESPEAR_DICT, TEST_SHAKESPEAR_VECTOR_CORPUS, path_name=TEST_SHAKESPEAR_DIR)