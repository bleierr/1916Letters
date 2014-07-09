'''
Created on 13 May 2014

This module contains the letter class
@author: Bleier
'''
from settings import CLEANING_PATTERN, STOPWORD_LST, STOPWORD_FILE, SPELL_CHECK_PWL
from helper import item_to_shelve, item_from_shelve, get_text_files
from nltk import stem
import enchant
import re, os, shutil

def clean_with_pattern(strg):
    """
    cleans a text according to a pattern defined in settings.py
    The CLEANING_PATTERN is a list of tuples the first element of the tuple contains 'no-group' or 'use-group, the second a regex pattern to be used
    'no-group' means the text will be cleaned of occurrences of pattern, while 'use-group' will keep the pattern defined in the group  
    Possible uses: Strips xml markup from string, splits a string into word token, strips leading and trailing punctuation and white space
    Parameter strg is a string, the function returns a list of strings
    Returns the text as a list of lower-case words cleaned of the defined pattern(s)
    """
    for type, pat in CLEANING_PATTERN:
        if type == "no-group":
            strg = "".join(re.split(pat , strg))
        elif type == "use-group":
            regex = re.compile(pat)
            lst = []
            for item in strg.split():
                mm = regex.match(item)
                if mm:
                    lst.append(mm.group(1))
            strg = " ".join(lst)
    return strg.lower().split()

def remove_stopwords(wordlst):
    total_stopws = STOPWORD_LST
    if STOPWORD_FILE:
        with open(STOPWORD_FILE, "r") as f:
            imported_stopws = f.read().split()
        total_stopws += imported_stopws
    return [w for w in wordlst if w not in total_stopws]

def spell_checking(wordlst):
    d = enchant.DictWithPWL("en_US", SPELL_CHECK_PWL)
    err = []
    for w in wordlst:
        if not d.check(w):
            try:
                err.append((w, d.suggest(w)[0]))
            except IndexError:
                err.append((w, None))
    return err

def stemmer(wordlst):
        st = stem.PorterStemmer()
        stem_words = []
        for w in wordlst:
            stem_words.append((w, st.stem(w)))
        return stem_words

def clean_all(file_dir_path):
    stat_dir = "stat"
    if os.path.isdir(stat_dir):
            shutil.rmtree(stat_dir)
    os.mkdir(stat_dir)
    filenames = get_text_files(file_dir_path, ext=".txt")
    
    spell_err = ""
    stem_print = ""
    for filename in filenames:
        file_path = file_dir_path + os.sep + filename
        with open(file_path, "r") as f:
            strg = f.read()
    
        wordlst = clean_with_pattern(strg)
        wordlst = remove_stopwords(wordlst)
        item_to_shelve(stat_dir+os.sep+"wordlst.shelve", wordlst, filename)
        #check for spelling errors
        spell_err += "\n{0}:\n".format(filename)
        err_lst = spell_checking(wordlst)
        if not err_lst:
            spell_err += "No spelling errors found\n"
        for word, err in err_lst:
            spell_err += "{0}:{1}\n".format(word, err)
            
        #check for stemming
        stem_print += "\n{0}:\n".format(filename)
        stem_words = stemmer(wordlst)
        for word, stemw in stem_words:
            stem_print += "{0}:{1}\n".format(word, stemw)
    
    with open(stat_dir+os.sep+"spelling_errors.txt", "w") as f:
        f.write(spell_err)
        
    with open(stat_dir+os.sep+"stem_froms.txt", "w") as f:
        f.write(stem_print)
    
    
if __name__ == "__main__":
    clean_all("test_data_excel"+os.sep+"txt")    
    
    
            