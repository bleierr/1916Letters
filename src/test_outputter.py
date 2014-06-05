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
        [("doc_id1", [(0, 0.5),(1, 0.8)]), ("doc_id2", [(0, 0.3),(1, 0.9)])],
        {"sample1.txt": ["file1.txt: 0.98", "file2.txt: 078"], "sample2.txt": ["file1.txt: 0.54", "file2.txt: 1.2"]}
        ]


class Test(unittest.TestCase):


    def test_prepare_output(self):
        returned = prepare_output(data)
        self.assertTrue("file1.txt" in returned)
        self.assertTrue('Topic 0 : 0.501*"richard" + 0.413*"bolingbroke"' in returned)
        self.assertTrue('The text in file: sample1.txt' in returned)
        


if __name__ == "__main__":
    unittest.main()