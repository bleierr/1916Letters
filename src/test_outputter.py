'''
Created on 4 Jun 2014

@author: Bleier
Unittest module to test outputter.py
'''
import unittest
from outputter import data_to_output_string

# the first is a list of file names, the second is a list of topics (returned by lsi.show_topics(n), third is a list of topic similarity, forth is a dictionary filename - similarity stat -zip(corpus_ids, sims)
data = {"filenames": ["file1.txt", "file2.txt"], 
        "topics": [u'0.501*"richard" + 0.413*"bolingbroke" + 0.285*"buckingham"', 
         u'0.227*"york" + 0.208*"elizabeth" + 0.201*"aumerle" + 0.184*"hastings"'],
        "topic_sim": [("doc_id1", [(0, 0.5),(1, 0.8)]), ("doc_id2", [(0, 0.3),(1, 0.9)])],
        "doc_sim": {"sample1.txt": [(1, "file1.txt", 0.98), (2, "file2.txt", 0.78)], "sample2.txt": [(1, "file1.txt", 0.28), (2, "file2.txt", 0.43)]}
        }


class Test(unittest.TestCase):


    def test_prepare_output(self):
        returned = data_to_output_string(data)
        self.assertTrue("file1.txt" in returned)
        self.assertTrue('Topic 0 : 0.501*"richard" + 0.413*"bolingbroke"' in returned)
        self.assertTrue('The text in file: sample1.txt' in returned)
        


if __name__ == "__main__":
    unittest.main()