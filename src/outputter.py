'''
Created on 4 Jun 2014

@author: Bleier
outputter.py
'''

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


def prepare_output(data):
    output = ""
    
    #first print the corpus training files
    if "filenames" in data.keys():
        output += "Training files:\n"
        for item in data["filenames"]:
            output += item + "\n"
    
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
            output += "Topic " + str(idx) + " : " + item + "\n"
               
        
    if "topic_sim" in data.keys():
    #print topics per document
        output += "\nTopics Per Document:\n"
        for doc_id, topic_list in data["topic_sim"]:
            output += "\nRelevance of the topics to Document: " + str(doc_id) + "\n"
            for topic, distribution in topic_list:
                output += "{0}: {1}; ".format(topic, distribution)
            output += print_histo(10, [abs(round(item[1]*10,1)) for item in topic_list], [item[0] for item in topic_list], doc_id)
            
    
    if "doc_sim" in data.keys():
        #print sample-texts and how close they are to the individual training texts
        for name, lst in data["doc_sim"].items():
            output += "\n\nThe text in file: " + name + " has the following similarities to the corpus texts:\n"
            for doc_nr, doc_name, sim in sorted(lst):
                output += "{0}: {1}: {2}   ".format(doc_nr, doc_name[3], sim)
            output += print_histo(10, [abs(round(float(item[2])*10, 1)) for item in lst], [item[0] for item in lst], name)
        
    return output




       
        