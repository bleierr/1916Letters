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
    lsi, topics, doc2topics = make_lsi(vector_corpus, dictionary, 2)
    sims = []
    for text in compare_texts:
        vec_corpus = dictionary.doc2bow(text.get_txt())
        vec_lsi = lsi[vec_corpus]
        sims.append(doc_similarity(vec_lsi, lsi, vector_corpus))
    return sims, topics, doc2topics

def main(corpus_file_path, dict_file_path, vec_corpus_file_path, excel_file=None, path_name=None):
    """
    The main function that starts the analysis process
    """
    
    c = main_dataimporter(corpus_file_path, dict_file_path, vec_corpus_file_path, excel_file=excel_file, path_name=path_name)
    
    corpus_ids, vector_corpus = c.get_vector_corpus()
    dictionary = c.get_dict()
    
    
    TEST_SAMPLE_GENSIM = "test_data" + os.sep + "gensim"
    
    compare_texts = []
    sample_files = get_text_files(TEST_SAMPLE_GENSIM, ".txt")
    for file_name in sample_files:
        compare_texts.append(txt_to_object(TEST_SAMPLE_GENSIM + os.sep + file_name, "page", "nr"))
        
    
    sims, topics, doc2topics = main_analyser(vector_corpus, dictionary, compare_texts)
    
    
    #prepare data for outputter
    output_data = {}
    if excel_file:
        output_data["filenames"] = [excel_file]
    elif path_name:
        output_data["filenames"]= get_text_files(path_name, ".txt")
    
    word_freq = [] 
    for item in c.get_letters():
        file_name = item.get_id()
        text_dict = item.get_dict()
        word_freq.append((file_name, sorted(list(text_dict.items()), key=lambda x:x[1], reverse=True)[:10]))
    
    output_data["word_freq"] = word_freq
    output_data["topics"] = topics
    
    #corpus to topic list, list of tuples (corpus id, topic relevance)
    docId2topicsLst = zip(corpus_ids, doc2topics)
    output_data["topic_sim"] = docId2topicsLst
    
    sample_results = {}
    #compare_texts is the actual sample file object
    for sample_file, sim, sample_obj in zip(sample_files, sims, compare_texts):
        text_sim = []
        for file_name, sim_index in sorted(zip(corpus_ids, sim)):
            text_sim.append((int(file_name.split("_")[0]), file_name.split("_"), sim_index))
        sample_results[sample_file + "; " +str(len(sample_obj.get_txt())) + " words; "] = text_sim
    output_data["sample_result"] = sample_results
    
    out =  prepare_output(output_data)
    
    f = open("stat.txt", "w")
    f.write(out)
    f.close()
    
    for item in c.get_letters():
        if "chain" in item.get_dict():
            print item.get_id() + "count; " + str(item.get_dict()["chain"])
        else:
            print "Not in: " + str(item.get_id())
    
    print "Works okay!"
    #returns a nltk freq dist obj
    #fdist_no_stop, total_words, most_freq_word, hapaxes = letter_analyser.make_analysis(letters)
    
        
    
    
if __name__ == "__main__":
    #main("1916letters_all_latest_translations.xlsx")
    #main(TEST_EXCEL, TEST_CORPUS, TEST_WORD_DICT, TEST_VECTOR_CORPUS)
    main(TEST_SHAKESPEAR_CORPUS, TEST_SHAKESPEAR_DICT, TEST_SHAKESPEAR_VECTOR_CORPUS, path_name=TEST_SHAKESPEAR_DIR)