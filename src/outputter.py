'''
Created on 4 Jun 2014

@author: Bleier
outputter.py
'''
import os, random, re



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


def data_to_output_string(data):   
    output = ''
    #first print the corpus training files
    if "filenames" in data.keys():
        output += "Training files:\n"
        for idx, item in enumerate(data["filenames"]):
            output += str(idx) + "  " + str(item) + "\n"
    
    if "word_freq" in data.keys():   
        #word freq
        for file_id, freq_lst in data["word_freq"]:
            output += "\n{0}:\n".format(file_id)
            for item in freq_lst:
                output += "{0}; ".format(item)
        
        output += "\n"
    
    if "topics" in data.keys():
        #print the topics
        output += "\n"
        for idx, item in enumerate(data["topics"]):
            output += "Topic " + str(idx) + " : " + str(item) + "\n"
               
        
    if "topic_sim" in data.keys():
    #print topics per document
        output += "\nTopics Per Document:\n"
        for idx, text2topic in enumerate(data["topic_sim"]):
            output += "\nRelevance of the topics to document " + str(idx) + "\n"
            for topic, distribution in text2topic:
                output += "{0}: {1}\n".format(topic, distribution)
            output += print_histo(10, [abs(round(item[1]*10,1)) for item in text2topic], [item[0] for item in text2topic])
            
    
    if "doc_sim" in data.keys():
        #print sample-texts and how close they are to the individual training texts
        name, lst = data["doc_sim"]
        output += "\n\nThe text in file: " + name + " has the following similarities to the corpus texts:\n"
        for sim, file_name in sorted(lst, reverse=True):
            output += "{0}: {1}   ".format(file_name, sim)
        output += print_histo(10, [abs(round(float(item[0])*10, 1)) for item in lst], [item[1] for item in lst], name)
        
    return output



#Following is code for mallet2gephi transformation#

def get_distribution_quote(lst):
    max_val = max(lst)*100
    min_val = min(lst)*100
    return 100/(max_val - min_val)

def calculate_value_via_quote(quote, min_value, num):
    return (num*100 - min_value*100) * quote / 100

def get_topic_comp(imp_file_comp, limit=0.1):
    with open(imp_file_comp, "r") as f:
        id2topics = {}
        for item in f:
            try:
                topic_comp_lst = item.split("\t")
                file_name = topic_comp_lst[1]
                mm = re.search("txt/(\d+.0).txt", file_name)
                if mm:
                    name = mm.group(1)
                    topic_lst = []
                    
                    #get only edges if they have certain relevance to topic
                    for num, i in enumerate(topic_comp_lst[3::2]):
                        previous_item = num*2 + 3 - 1
                        if float(i) > limit:
                            topic_lst.append((topic_comp_lst[previous_item], float(i)))
                    id2topics[name] = topic_lst   
                else:
                    print "no match found"
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
        quota = get_distribution_quote(value_lst)
    
    for name, topic_lst in t.items():
        if len(topic_lst) > 0:
            for topic, value in topic_lst:
                random_id = name + str(random.random())
                if dist0to1:
                    value = calculate_value_via_quote(quota, min_value, value)
                write_strg += "\n{0},T{1},Undirected,{2},{3}".format(name, topic, random_id, value)
    #write gephi edges data to file
    with open(exp_file, "w") as f:
        f.write(write_strg)



if __name__ == "__main__":
    imp_file_comp = "Mallet_T12"+os.sep+"letters-compostion_T12.txt"
    
    exp_file = "Mallet_T12"+os.sep+"letters_edges_T12.csv"
    path_to_corpus = "c:"+os.sep+"TestTexts"+os.sep+"letterCorpus"+os.sep+"topic-compostion.txt"
    path_to_corpus = "c:"+os.sep+"TestTexts"+os.sep+"letterCorpus"+os.sep+"gensim-letters-edges_T4.csv"
    
        