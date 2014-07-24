#-*- coding: utf-8 -*-
'''
Created on 17 May 2014

@author: Bleier
'''
import unittest
from helper import replace_problem_char


class Test(unittest.TestCase):


    def test_replace_problem_char(self):
        strg = "This is a ’ test"
        returned = replace_problem_char(strg)
        expected = "This is a ' test"
        self.assertEqual(returned, expected)
    
    def test_strip_xml(self):
        strg = "This is <name>Hugo</name> and <another xml> <!-- Comment -->"
        returned = strip_xml(strg)
        expected = "This is Hugo and"
        self.assertEqual(returned, expected)
        
    def test_clean_txt(self):
        strg = "This’ is <name>Hugo</name> and <another xml> <!-- Comment -->"
        returned = clean_txt(strg)
        expected = ["this", "is", "hugo", "and"]
        self.assertEqual(returned, expected)


if __name__ == "__main__":
    unittest.main()