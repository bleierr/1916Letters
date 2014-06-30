'''
Created on 18 Jun 2014

@author: Bleier
'''

from gensim import models, corpora, similarities, interfaces
from txt_classes import TxtCorpus, TxtItem
import unittest, shutil
import importer, analyse, outputter
import os, sys


args = sys.argv
print args
