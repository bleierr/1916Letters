'''
Created on 13 May 2014

This module contains the letter class
@author: Bleier
'''
from settings import CLEANING_PATTERN, STOPWORD_LST, STOPWORD_FILE, SPELL_CHECK_PWL
from helper import item_to_shelve, item_from_shelve, get_text_files
from nltk import stem
import enchant
import re, os, shutil, getopt, sys

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
            strg = " ".join(re.split(pat , strg))
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
    
    temp_pwl_file = "Temporary_pwl_file.txt"
    with open(SPELL_CHECK_PWL, "r") as f:
        all_pwl = f.read().lower()
        
    with open(temp_pwl_file, "w") as f:
        f.write(all_pwl)
        
    
    d = enchant.DictWithPWL("en_US", temp_pwl_file)
    err = []
    for w in wordlst:
        if not d.check(w):
            try:
                first_sug = d.suggest(w)[0]
                if w != first_sug.lower():
                    err.append((w, first_sug))
            except IndexError:
                err.append((w, None))
    os.remove(temp_pwl_file)
    return err

def stemmer(wordlst):
        st = stem.PorterStemmer()
        stem_words = []
        for w in wordlst:
            stem_words.append((w, st.stem(w)))
        return stem_words

def clean_all(file_dir_path, clean_files_dir, mode="pat+stop"):
    #make a directory for the cleaning log
    stat_dir = clean_files_dir + os.sep + "cleaninglog"
    os.mkdir(stat_dir)
    
    filenames = get_text_files(file_dir_path, ext=".txt")
    
    spell_err = ""
    stem_print = ""
    for filename in filenames:
        file_path = file_dir_path + os.sep + filename
        with open(file_path, "r") as f:
            strg = f.read()
        if mode == "pat+stop":
            wordlst = clean_with_pattern(strg)
            wordlst = remove_stopwords(wordlst)
        else:
            wordlst = strg.split()
        item_to_shelve(stat_dir+os.sep+"wordlst.shelve", wordlst, filename)
        #check for spelling errors
        err_lst = spell_checking(wordlst)
        if mode == "spell":
            words = " ".join(wordlst)
            for err, corr in err_lst:
                if corr:
                    words = words.split(" "+err+" ")
                    words = " "+corr+" ".join(words)
            wordlst = words.split()
        if err_lst:
            spell_err += "\n{0}:\n".format(filename)
        
            for err, corr in err_lst:
                spell_err += "{0}:{1}\n".format(err, corr)
            
        #check for stemming
        stem_words = stemmer(wordlst)
        if mode == "stem":
            words = []
            for word, stemw in stem_words:
                words.append(stemw)
            wordlst = words
        
        stem_print += "\n{0}:\n".format(filename)
        for word, stemw in stem_words:
            stem_print += "{0}:{1}\n".format(word, stemw)
        
        with open(clean_files_dir + os.sep + filename, "w") as f:
            f.write(" ".join(wordlst))
        
    with open(stat_dir+os.sep+"spelling_errors.log", "w") as f:
        f.write(spell_err)
        
    with open(stat_dir+os.sep+"stem_froms.log", "w") as f:
        f.write(stem_print)
    
        
def cleaner_main(file_dir_path=None, clean_files_dir=None, mode="pat+stop"):
    if not file_dir_path:
        print "No file path given for text files."
        return False
    if not clean_files_dir:
        clean_files_dir = os.path.split(os.path.abspath(file_dir_path))[0] + os.sep + "cleantxt"
        #make file dir for the clean txt files
    if os.path.isdir(clean_files_dir):
        inp = raw_input("The directory {0} does already exist. Overwrite?Y/N".format(clean_files_dir))
        if inp in ["Y", "y"]:
            shutil.rmtree(clean_files_dir)
        else:
            return False
    os.mkdir(clean_files_dir)
    
    clean_all(file_dir_path, clean_files_dir, mode=mode)
    
     
    
    
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "", ["mode=", "file_dir_path=", "clean_files_dir="])
    key_args = {}
    for key, value in opts:
        if key == "--mode": # mode values: "pat+stop" (default), 'spell', 'stem'
            key_args["mode"] = value
        if key == "--file_dir_path":
            key_args["file_dir_path"] = value
        elif key == "--clean_files_dir":
            key_args["clean_files_dir"] = value
    cleaner_main(**key_args)
               
    
    
            