'''
Created on 19 May 2014

@author: Rombli
'''
import unittest, datetime,os
from letter_classes import Letter, TxtCorpus
from helper import item_to_pickle
from settings import TEST_CORPUS


class Test(unittest.TestCase):
    
    def setUp(self):
        dictionary = {}
        d1 = datetime.datetime(2014, 1, 15, 14, 12, 34 )
        page1 = "32"
        text1 = "This is page 32: unittest supports test automation, sharing of setup and shutdown code for tests"
        d2 = datetime.datetime(2014, 1, 13, 5, 7, 28 )
        page2 = "33"
        text2 = "This is page 33: unittest supports test automation, sharing of setup and shutdown code for tests"
        self.l1 = Letter(**{"Publisher": "Tester1", "Book": "Bookname1"})
        self.l1.add_page(d1, page1, text1)
        dictionary["Letter1"] = self.l1
        self.l2 = Letter(**{"Publisher": "Tester2", "Book": "Bookname2"})
        self.l2.add_page(d2, page2, text2)
        dictionary["Letter2"] = self.l2
        item_to_pickle(TEST_CORPUS, dictionary)


    def test_LetterClass(self): 
        self.assertEqual(self.l1.Publisher, "Tester1")
        self.assertEqual(self.l2.Book, "Bookname2")
        self.assertTrue(isinstance(self.l1, Letter))

    
    def test_TxtCorpusClass(self):
        c = TxtCorpus(TEST_CORPUS)
        self.assertTrue(isinstance(c, TxtCorpus))
        count = []
        for item in c:
            self.assertTrue("this" in item)
            self.assertTrue(isinstance(item, list))
            self.assertTrue(isinstance(item[0], str))
            count.append(len(item))
        count2 = []
        for item in c.get_tokens():
            self.assertFalse("a" in item)
            self.assertFalse("&" in item)
            self.assertFalse("this" in item)
            count2.append(len(item))
        self.assertTrue(count[0] > count2[0])
        self.assertTrue(count[1] > count2[1])
    
    def tearDown(self):
        os.remove(TEST_CORPUS)


if __name__ == "__main__":
    unittest.main()