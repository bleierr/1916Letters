'''
Created on 4 Jun 2014

@author: Bleier
outputter.py
'''
import os, random, re, getopt, sys
from helper import item_from_pickle

def print_histo(rows, column_fill, labels=None, document_name=""):
    """
    rows is the number of rows the histogram is high
    column_fill is a list of numbers that determine how much of each column in the histogram is filled up
    labels for the columns
    document name for header
    """
    histo = "\n"
    for item in column_fill:
        histo += "{0: ^5}".format("_"*5)
    histo += "\n{0}\n\n".format(document_name)
    if labels:
        for item in labels:
            histo += "{0: ^5}".format(item)
        histo += "\n"
    for row in reversed(range(rows)):
        for num in column_fill:
            if num >= row+1:
                histo += "{0: ^5}".format("***")
            else:
                histo += "{0: ^5}".format(" ")
        histo += "\n"
    for item in column_fill:
        histo += "{0: ^5}".format("_"*5)
    histo += "\n\n"
    return histo


def data_to_output_string(file_names=None, name_and_lst=None, print_o_lst=None): 
    """
    first parameter file_names is the list of file names of the trainings corpus
    name_and_lst should a list of tuples e.g. (file_name, word_freq_list)
    print_o_lst should a list of values - values will be printed in an ordered list
    """  
    output = ''
    #first print the corpus training files
    if file_names:
        output += "Training files:\n"
        for idx, name in enumerate(file_names):
            output += str(idx) + "  " + str(name) + "\n"
    
    if name_and_lst:   
        #name_and_list is a tuple of name and a list of values, name is printed and the values in a new line
        for name, lst in name_and_lst:
            output += "\n{0}:\n".format(name)
            for item in lst:
                output += "{0}; ".format(item)
        
        output += "\n"
    
    if print_o_lst:
        #print an ordered list, e.g. list of  topics
        output += "\n"
        for idx, item in enumerate(print_o_lst):
            output += "Topic " + str(idx) + " : " + str(item) + "\n"
               
    return output



#Following is code for mallet2gephi transformation#

def get_percent_of_diff(lst):
    """
    given a list of values between 0 and 1, if finds the highest and lowest value, calculates the difference
    and calculates percent of the difference. 
    """
    max_val = max(lst)*100
    min_val = min(lst)*100
    return 100/(max_val - min_val)

def distribute_values(p, min_value, num):
    """
    in combination with get_one_per_centcent_of_diff this function distributes values between a certain range wider - e.g. in order to 
    help with strong, unreadable clusters in the Gephi output.
    usually Mallet or Gensim return probability values like 0.25435, 0.3453, 0.2344, if visulized these values would cluster to strongly together in
    Gephi, therefore the they have to be distributed over 0 (0%) to 1 (100%).
    p, is a float value calculated by get_percent_of_diff
    min_value is a float between 0 and 1, the lowest value in a list of float values between 0 and 1
    num is the float (between 0 and 1) who's value should be re-calculated if the range would be 0-1
    """
    return (num*100 - min_value*100) * p / 100

def get_topic_comp(imp_file_comp, limit=0.1):
    with open(imp_file_comp, "r") as f:
        id2topics = {}
        for item in f.readlines()[1:]:
            try:
                topic_comp_lst = item.split("\t")
                file_name = topic_comp_lst[1]
                print file_name
                if "//" in file_name:
                    #cut out name from file name string - used for mallet files
                    mm = re.search("txt/(\d+.0).txt", file_name)
                    if mm:
                        name = mm.group(1)
                    else:
                        print "no match found"   
                else:
                    name = file_name
                    topic_lst = []
                    
                    #get only edges if they have certain relevance to topic
                    for num, i in enumerate(topic_comp_lst[3::2]):
                        previous_item = num*2 + 3 - 1
                        if float(i) > limit:
                            topic_lst.append((topic_comp_lst[previous_item], float(i)))
                    id2topics[name] = topic_lst   
                    
            except IndexError:
                print "index error"
    return id2topics

def mallet2gephi_edges(imp_file_comp, exp_file, limit=0.1, dist0to1=False):
    """
    transforms a mallet compostion txt file into a gephi edges file
    The layout of the mallet file should be as follows:
        'doc'\t'name'\t'topic'\t'proportion'\t'topic'\t'proportion'...
    topics are integer, proportion are floats between 0 and 1
    The parameter limit is the threshold below which proportions will not be included in the output
    If dist0to1 is set to 'True' the mallet proportions will be distributed from 0-1
    """
    t = get_topic_comp(imp_file_comp, limit=limit)

    value_lst = []
    for topic_lst in t.values():
        if len(topic_lst) > 0:
            for topic, value in topic_lst:
                value_lst.append(value)

    #head of gephi csv file
    write_strg = "Source,Target,Type,Id,Weight"
    
    if dist0to1:
        #for dist graph
        min_value = min(value_lst)
        p = get_percent_of_diff(value_lst)
    
    for name, topic_lst in t.items():
        if len(topic_lst) > 0:
            for topic, value in topic_lst:
                random_id = name + str(random.random())
                if dist0to1:
                    value = distribute_values(p, min_value, value)
                write_strg += "\n{0},T{1},Undirected,{2},{3}".format(name, topic, random_id, value)
    #write gephi edges data to file
    with open(exp_file, "w") as f:
        f.write(write_strg)


def search_TxtCorpus(corpus_file_path, attrs, python_expr, to_file=False):
    """
    corpus_file_path is the file path to a valid TxtCorpus file
    attrs is a list of attributes of the instance that should be included in the print out
    python_expr is a Python expression that is used to search for certain texts, e.g. ''
    """
    c = item_from_pickle(corpus_file_path)
    head, tail = os.path.split(corpus_file_path)
    #search
    search_result_strg = ""
    print c
    for item in c.get_txtitems():
        if eval(python_expr):
            search_result_strg += "{0}, {1}\n".format(item.unique_name, " ".join([item[a] for a in attrs]))
 
    if to_file:           
        with open(head + os.sep + "search_results.txt", "w") as f:
            f.write(search_result_strg)
    else:
        print search_result_strg
    
def outputter_main(mode="search", corpus_file_path=None, attrs=None, python_expr=None, to_file=False, imp_file_comp=None, exp_file=None, limit=0.1, dist0to1=False):
    if mode == "search":
        if corpus_file_path == None or attrs == None or python_expr == None:
            print "Error: if mode is set to 'search' the parameters 'corpus_file_path', 'python_expr' and 'attrs' are required!"
            return None
        search_TxtCorpus(corpus_file_path=corpus_file_path, attrs=attrs, python_expr=python_expr, to_file=to_file)
    elif mode == "gephi":
        if imp_file_comp == None or exp_file == None:
            print "Error: if mode is set to 'gephi' the parameters 'imp_file_comp' and 'exp_file' are required!"
            return None
        mallet2gephi_edges(imp_file_comp, exp_file, limit=limit, dist0to1=dist0to1)
        

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "", ["mode=", "path_to_corpus=", "num_topics=", "path_to_txt_items=", "new_text_dir="]) 
    key_args = {}
    for key, value in opts:
        if key == "--mode": #possible mode valuse: 'replace', 'lsi'
            key_args["mode"] = value
        if key == "--path_to_corpus":
            key_args["path_to_corpus"] = value
        if key == "--num_topics":
            key_args["num_topics"] = value
        if key == "--path_to_txt_items":
            key_args["path_to_txt_items"] = value   
        if key == "--new_text_dir":
            key_args["new_text_dir"] = value
    
    outputter_main(**key_args)
    #imp_file_comp = "Mallet_T12"+os.sep+"letters-compostion_T12.txt"
    
    #exp_file = "Mallet_T12"+os.sep+"letters_edges_T12.csv"
    #path_to_input = "c:"+os.sep+"TestTexts"+os.sep+"letterCorpus"+os.sep+"topic-compostion.txt"
    #path_to_result = "c:"+os.sep+"TestTexts"+os.sep+"letterCorpus"+os.sep+"gensim-letters-edges_T16.csv"
    
    #mallet2gephi_edges(path_to_input, path_to_result, limit=0.25, dist0to1=False)
    
    corpus_file_path = "c:"+os.sep+"TestTexts"+os.sep+"letterCorpus"+os.sep+"text_corpus.pickle"
    search_TxtCorpus(corpus_file_path,['Language'], "item.Language!='English'")
    
    
    
        