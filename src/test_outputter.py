'''
Created on 4 Jun 2014

@author: Bleier
Unittest module to test outputter.py
'''
import unittest
from outputter import prepare_output

# the first is a list of file names, the second is a list of topics (returned by lsi.show_topics(n), third item is a dictionary filename - similarity stat -zip(corpus_ids, sims)
data = [["file1.txt", "file2.txt"], 
        [u'0.501*"richard" + 0.413*"bolingbroke" + 0.285*"buckingham"', 
         u'0.227*"york" + 0.208*"elizabeth" + 0.201*"aumerle" + 0.184*"hastings"'],
        {"sample1.txt": ["file1.txt: 0.98", "file2.txt: 078"], "sample2.txt": ["file1.txt: 0.54", "file2.txt: 1.2"]}
        ]


class Test(unittest.TestCase):


    def test_prepare_output(self):
        returned = prepare_output(data)
        expected = """file1.txt\nfile2.txt\nTopic 00.501*"richard" + 0.413*"bolingbroke" + 0.285*"buckingham"\nTopic 10.227*"york" + 0.208*"elizabeth" + 0.201*"aumerle" + 0.184*"hastings"\n\nThe text in file: sample2.txt has the following similarities to the corpus texts:\nfile1.txt: 0.54\nfile2.txt: 1.2\nThe text in file: sample1.txt has the following similarities to the corpus texts:\nfile1.txt: 0.98\nfile2.txt: 078"""
        self.assertEqual(returned, expected)


if __name__ == "__main__":
    unittest.main()