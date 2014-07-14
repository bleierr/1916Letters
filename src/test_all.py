'''
Created on 18 Jun 2014

@author: Bleier
'''

from gensim import models, corpora, similarities, interfaces
from txt_classes import TxtCorpus, TxtItem, TxtItemLetterExcel, TxtItemTextFile
import importer, cleaner, analyse, outputter
import os

path_to_excel = "C:"+os.sep+"TestTexts"+os.sep+"TestData"+os.sep+"all_transcriptions_until_16_06_2014.xlsx"
corpus_dir = "C:"+os.sep+"TestTexts"+os.sep+"letterCorpus"
corpus_txt_files = "C:"+os.sep+"TestTexts"+os.sep+"letterCorpus"+os.sep+"txt"
corpus_txt_cleanfiles = "C:"+os.sep+"TestTexts"+os.sep+"letterCorpus"+os.sep+"cleanfiles"

if __name__ == "__main__":
    #importer.importer_main("excel", path_to_excel, corpus_dir)
    cleaner.cleaner_main(corpus_txt_files, corpus_txt_cleanfiles, "pat+stop")