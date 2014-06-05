'''
Created on 4 Jun 2014

@author: Bleier
outputter.py
'''

def prepare_output(data):
    output = ""
    
    #first print the corpus training files
    output += "Training files:\n"
    for item in data[0]:
        output += item + "\n"
    
    #print the topics
    output += "\n"
    for idx, item in enumerate(data[1]):
        output += "Topic " + str(idx) + " : " + item + "\n"
        
    #print topics per document
    output += "\nTopics Per Document:\n"
    for doc_id, topic_list in data[2]:
        output += "\nRelevance of the topics to Document: " + str(doc_id) + "\n"
        for topic, distribution in topic_list:
            output += "{0}: {1}; ".format(topic, distribution)
            
    
    #print sample-texts and how close they are to the individual training texts
    for name, lst in data[3].items():
        output += "\n\nThe text in file: " + name + " has the following similarities to the corpus texts:\n"
        for sim_text in lst:
            output += sim_text + "\n"
    return output
        
        