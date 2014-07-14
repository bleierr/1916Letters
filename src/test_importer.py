'''
Created on 16 May 2014

@author: Bleier
'''
import unittest, os, shutil, xlwt, datetime
from txt_classes import TxtCorpus, TxtItem, TxtItemLetterExcel, TxtItemTextFile
from importer import get_texts_from_Excel, get_texts_from_files, make_txt_corpus
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

excel_data = [{"Text_ID":"txt1", "OtherAttr": "Ensures Bunch works", "Timestamp":datetime.datetime(2014, 7, 14, 13, 24, 14), "Page":1, "Text":"Text1 Page1"},
              {"Text_ID":"txt1", "OtherAttr": "Ensures Bunch works", "Timestamp":datetime.datetime(2014, 7, 14, 14, 25, 14), "Page":1, "Text":"Text1 Page1 Write2"},
              {"Text_ID":"txt1", "OtherAttr": "Ensures Bunch works", "Timestamp":datetime.datetime(2014, 7, 13, 0, 24, 14), "Page":2, "Text":"Text1 Page2"},
              {"Text_ID":"txt2", "OtherAttr": "Ensures Bunch works", "Timestamp":datetime.datetime(2014, 7, 12, 0, 24, 14), "Page":1, "Text":"Text2 Page1"},
              {"Text_ID":"txt2", "OtherAttr": "Ensures Bunch works", "Timestamp":datetime.datetime(2014, 7, 15, 0, 24, 14), "Page":1, "Text":"Text2 Page1 Write2"}
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
        self.c_from_excel = make_txt_corpus(self.excel_items, self.tempdir_excel)
        
        self.tempdir_txt = "tmp" + os.sep + "txtsource"
        if os.path.isdir(self.tempdir_txt):
            shutil.rmtree(self.tempdir_txt)
        os.mkdir(self.tempdir_txt)
        
        for idx, item in enumerate(documents):
            with open(self.tempdir_txt + os.sep + "testfile" + str(idx) + ".txt", "w") as f:
                f.write(item)
        #makes a text corpus from a number of text files
        self.txt_items, id2texts = get_texts_from_files(self.tempdir_txt, self.tempdir_txt, ".txt") 
        self.c_from_txt = make_txt_corpus(self.txt_items, self.tempdir_txt)
        
    def test_get_texts_from_Excel(self):
        """
        Tests the function get_texts_from_Excel, and ensures that a list of TxtItem objects is returned
        """
        self.assertTrue(isinstance(self.excel_items, list))
        msg1 = "Error: The item with number {0} is not of type TxtItem"
        msg2 = "Error: The item with number {0} is not of type TxtItemLetterItem"
        for idx, txt in enumerate(self.excel_items):
            self.assertTrue(isinstance(txt, TxtItem), msg1.format(idx))
            self.assertTrue(isinstance(txt, TxtItemLetterExcel), msg2.format(idx))

    def test_IDs_correct(self):
        for item in self.excel_items:
            self.assertTrue(item.unique_name in ["txt1", "txt2"])
            
    def test_Bunch_works(self):
        "Tests the the Bunch class in txt_classes imports all attributes correctly"
        for txt in self.excel_items:
            self.assertEqual(txt.OtherAttr, "Ensures Bunch works") #tests the Bunch class
                  
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
            
    def test_get_texts_from_files(self):
        """
        Tests if text from .txt files is imported correctly
        """
        for idx, txtitem in enumerate(self.txt_items):
            self.assertTrue(txtitem, TxtItem)
            self.assertTrue(txtitem, TxtItemTextFile)
            self.assertEqual(txtitem.unique_name, "testfile" + str(idx)) # tests the unique_name attribute
            if idx == 0:
                self.assertEqual(txtitem.unique_name, "testfile0")
                self.assertEqual(txtitem.txt_file_path, "tmp" + os.sep + "txtsource" + os.sep + "txt" +os.sep + "testfile0.txt")
                self.assertTrue(isinstance(txtitem.get_txt(), list))
                self.assertTrue("applications" in txtitem.get_txt())
                self.assertTrue("machine" in txtitem.get_txt())
            if idx == 8:
                self.assertEqual(txtitem.unique_name, "testfile8")
                self.assertEqual(txtitem.txt_file_path, "tmp" + os.sep + "txtsource" + os.sep + "txt" +os.sep + "testfile8.txt")
                self.assertTrue(isinstance(txtitem.get_txt(), list))
                self.assertTrue("minors" in txtitem.get_txt())
                self.assertTrue("survey" in txtitem.get_txt())
    
    def test_make_txt_corpus(self):
        self.assertTrue(isinstance(self.c_from_txt, TxtCorpus))
        self.assertTrue(len([item for item in self.c_from_txt]) == 9) 
        
        #test excel corpus
        self.assertTrue(isinstance(self.c_from_excel, TxtCorpus))
        self.assertTrue(len([item for item in self.c_from_excel]) == 2)
        for item in self.c_from_excel:
            self.assertTrue("write2" in item)
            self.assertTrue("page1" in item)
            if "text2" in item:
                self.assertFalse("text1" in item) #in text two there should be no 'text1' and also no second page
                self.assertFalse("page2" in item)
                 
    def test_make_txt_corpus_dictionary_correctly_added(self):
        """
        Tests the dictionary and vector corpus was correctly added
        """
        
        d = self.c_from_excel.get_dictionary()
        self.assertTrue(isinstance(d, corpora.Dictionary))
        self.assertEqual(len(d), 3) # the dictionary has only 3 items, because unique words in the corpus are eliminated when setting up the dictionary
        d = self.c_from_txt.get_dictionary()
        self.assertTrue(isinstance(d, corpora.Dictionary))
        self.assertEqual(len(d), 16) # the dictionary has only 16 items, because unique words in the corpus are eliminated when setting up the dictionary
        
        
    def tearDown(self):
        shutil.rmtree(self.tempdir_excel)
        shutil.rmtree(self.tempdir_txt)
        shutil.rmtree(self.tempdir)


if __name__ == "__main__":
    unittest.main()