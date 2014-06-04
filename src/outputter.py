'''
Created on 4 Jun 2014

@author: Bleier
outputter.py
'''

def prepare_output(data):
    output = ""
    
    #first print the corpus data files
    for item in data[0]:
        output += item + "\n"
        
    for idx, item in enumerate(data[1]):
        output += "Topic " + str(idx) + " : " + item + "\n"
        
    for name, lst in data[2].items():
        output += "\nThe text in file: " + name + " has the following similarities to the corpus texts:"
        for sim_text in lst:
            output += "\n" + sim_text
    return output
        
        