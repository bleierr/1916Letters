'''
Created on 16 May 2014

@author: Bleier
'''
import unittest, os, shutil, xlwt, datetime
from txt_classes import TxtCorpus, TxtItem
from importer import get_texts_from_Excel, get_texts_from_files
from gensim import corpora


documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

"""In order for the tests to work the global variables in settings.py have to be set as follows:
TIMESTAMP = True
TIMESTAMP_COL = "Timestamp"
PAGE_COL = "Page"
TRANSCRIPTION_COL = "Text"
TXT_ID = "Text_ID"
"""

excel_data = [{"Text_ID":"txt1", "Timestamp":datetime.datetime(2014, 7, 14, 13, 24, 14), "Page":1, "Text":"Text1 Page1"},
              {"Text_ID":"txt1", "Timestamp":datetime.datetime(2014, 7, 14, 14, 25, 14), "Page":1, "Text":"Text1 Page1 Write2"},
              {"Text_ID":"txt1", "Timestamp":datetime.datetime(2014, 7, 13, 0, 24, 14), "Page":2, "Text":"Text1 Page2"},
              {"Text_ID":"txt2", "Timestamp":datetime.datetime(2014, 7, 12, 0, 24, 14), "Page":1, "Text":"Text2 Page1"},
              {"Text_ID":"txt2", "Timestamp":datetime.datetime(2014, 7, 15, 0, 24, 14), "Page":1, "Text":"Text2 Page1 Write2"}
              ]



class Test(unittest.TestCase):
    
    def setUp(self):
        self.tempdir = "tmp"
        if os.path.isdir(self.tempdir):
            shutil.rmtree("tmp")
        os.mkdir(self.tempdir)
        #create excel file for testing
        self.tempdir_excel = "tmp" + os.sep + "excel" 
        if os.path.isdir(self.tempdir_excel):
            shutil.rmtree(self.tempdir_excel)
        os.mkdir(self.tempdir_excel)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Test Table")
        for idx, key in enumerate(excel_data[0]):
            sheet.write(0, idx, key)
        for idx, item in enumerate(excel_data):
            row = idx+1 #the row is the index + the header row
            col = 0
            for key, value in item.items():
                if key == "Timestamp":
                    style = xlwt.XFStyle()
                    style.num_format_str = 'D-MMM-YY' 
                    sheet.write(row, col, value, style)
                else:
                    sheet.write(row, col, value)
                col += 1
        workbook.save(self.tempdir_excel + os.sep + "test_excel.xls")
            
        excel_file = self.tempdir_excel + os.sep + "test_excel.xls"
        
        # makes the test corpus from an excel file
        self.excel_items, id2texts = get_texts_from_Excel(excel_file, self.tempdir_excel) 
        #self.c_from_excel = make_text_corpus(texts, self.tempdir_excel)
        
        self.tempdir_txt = "tmp" + os.sep + "txt"
        if os.path.isdir(self.tempdir_txt):
            shutil.rmtree(self.tempdir_txt)
        os.mkdir(self.tempdir_txt)
        
        for idx, item in enumerate(documents):
            f = open(self.tempdir_txt + os.sep + "testfile" + str(idx) + ".txt", "w")
            f.write(item)
            f.close()
        #makes a text corpus from a number of text files
        self.txt_items, id2texts = get_texts_from_files(self.tempdir_txt, self.tempdir_txt, ".txt") 
        #self.c_from_txt = make_text_corpus(texts, self.tempdir_txt)
        
    def test_get_texts_from_Excel(self):
        """
        Tests the function get_texts_from_Excel, and ensures that a list of TxtItem objects is returned
        """
        self.assertTrue(isinstance(self.excel_items, list))
        msg = "Error: The item with number {0} is not of type TxtItem"
        for idx, txt in enumerate(self.excel_items):
            self.assertTrue(isinstance(txt, TxtItem), msg.format(idx))

    def test_IDs_correct(self):
        for item in self.excel_items:
            self.assertTrue(item.unique_name in ["txt1", "txt2"])
            
        
    def test_excel_pages_added(self):
        for item in self.excel_items:
            for key, pages  in item.get_pages().items():
                if int(key) == 1:
                    self.assertTrue(len(pages) == 2)
                elif int(key) == 2:
                    self.assertTrue(len(pages) == 1)
                else:
                    raise KeyError ("The page writes in the TxtItems objecs are not correct. Should be either 1 or 2, {0} found.").format(len(pages))
                self.assertTrue(isinstance(pages, list))
                self.assertTrue(isinstance(pages[0], tuple)) #timestamp tuple (timestamp, page text as string)
                self.assertTrue(isinstance(pages[0][0], datetime.datetime)) # the timestamp as float
                self.assertTrue(isinstance(pages[0][1], unicode))   # the page content as string
                self.assertTrue(pages[0][1][:4], "Text")    # ensures text is stored in the pages, all test pages start with 'Text'
            #check timestamps
            if item.unique_name == "txt1":
                self.assertTrue("text1" in item.get_txt())
                self.assertFalse("text2" in item.get_txt())
                self.assertTrue("page1" in item.get_txt())
                self.assertTrue("page2" in item.get_txt())
                for key, pages in item.get_pages().items():
                    if int(key) == 2:
                        self.assertTrue(pages[0][0] == datetime.datetime(2014, 7, 13, 0, 24, 14), "Error: timestamps are not correctly added")
            if item.unique_name == "txt2":
                self.assertTrue("text2" in item.get_txt())
                self.assertFalse("text1" in item.get_txt())
                self.assertTrue("page1" in item.get_txt())
                self.assertTrue("write2" in item.get_txt())
            
            
         
    def test_make_text_corpus(self):
        """
        Tests if corpus, dictionary and text-dictionary mapping corpus is created correctly
        
        self.assertTrue(isinstance(self.c_from_excel, TxtCorpus))
        d = self.c_from_excel.get_dict()
        vec = d.doc2bow(["this", "a"])"""
        pass
        
    def test_make_word_dictionary(self):
        """
        Tests the dictionary for the words
        
        d = self.c_from_excel.get_dict()
        self.assertTrue(isinstance(d, corpora.Dictionary))
        #self.assertTrue("gold" in d.token2id)    #token2id reverses key - value in dictionary: 32: "house" ==> "house": 32
        self.assertFalse("all" in d.token2id)
        msg = "Error: The filepath to the gensim Dictionary stored in the TxtCorpus {0} is not the same as: {1}"
        self.assertEqual(self.c_from_excel.dict_path, self.tempdir_excel + os.sep + "text_corpus.dict", msg.format(self.c_from_excel.dict_path, self.tempdir_excel + os.sep + "text_corpus.dict"))
        """
        pass

    def test_corpusImportedCorrectly(self):
        pass
        #self.assertTrue(isinstance(self.c_from_txt, TxtCorpus))
        #self.assertTrue(len([item for item in self.c_from_txt]), 9)
        
    def tearDown(self):
        shutil.rmtree(self.tempdir_excel)
        shutil.rmtree(self.tempdir_txt)
        shutil.rmtree(self.tempdir)


if __name__ == "__main__":
    unittest.main()