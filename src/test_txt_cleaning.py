'''
Created on 16 May 2014

@author: Bleier
'''
import unittest
import txt_cleaning


text = "Human machine interface for lab abc computer applications. A survey of user opinion of computer system response time"

class Test(unittest.TestCase):
    
    def test_clean_with_pattern(self):
        #remove punctuation
        txt = "Okay, this is a simple test."
        return_txt = txt_cleaning.clean_with_pattern(txt)
        self.assertEqual(return_txt, ["okay", "this", "is", "a", "simple", "test"])
        #remove XML-like markup
        txt = "This <i>is</i> a sim<test>ple test<!-- Comment -->"
        return_txt = txt_cleaning.clean_with_pattern(txt)
        self.assertEqual(return_txt, ["this", "is", "a", "simple", "test"])
    
    def test_remove_stopwords(self):
        stop_txt = "This is a simple test".split()
        return_txt = txt_cleaning.remove_stopwords(stop_txt)
        self.assertEqual(["This", "simple", "test"], return_txt)
        
    def test_spell_checking(self):
        test_txt = "This wi worgn writtten 123d".split()
        #the string '123d' is not found and no alternative is provided, None will be matched with the word
        return_errors = txt_cleaning.spell_checking(test_txt)
        self.assertEqual(return_errors, [('wi', 'WI'), ('worgn', 'wrong'), ('writtten', 'written'), ('123d', None)])
        
        
    def test_stemmer(self):
        test_txt = "saying this would be kids women savings".split()
        stem_lst = txt_cleaning.stemmer(test_txt)
        self.assertEqual(stem_lst[0], ('saying', 'say'))
        self.assertEqual(stem_lst[1], ('this', 'thi'))
        self.assertEqual(stem_lst[2], ('would', 'would'))
        self.assertEqual(len(stem_lst), 7)
  

if __name__ == "__main__":
    unittest.main()