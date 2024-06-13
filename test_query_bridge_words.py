import unittest
import numpy as np
from main import process_text_file, queryBridgeWords


class TestQueryBridgeWords(unittest.TestCase):
    def setUp(self):
        # 文本预处理
        processed_words = process_text_file("a.txt")
        print(processed_words)
        if not processed_words:
            print("There are no words.")
            exit(0)

        # 生成单词表
        wordlist = []
        for i in processed_words:
            if i not in wordlist:
                wordlist.append(i)

        # 将文本用数字数组表示
        wordnumber = []
        for i in processed_words:
            for j in range(len(wordlist)):
                if wordlist[j] == i:
                    wordnumber.append(j)

        # 生成有向图矩阵
        digraph = np.zeros((len(wordlist), len(wordlist)))
        print(digraph.shape)
        for i in range(len(wordnumber) - 1):
            temp1 = wordnumber[i]
            temp2 = wordnumber[i + 1]
            digraph[temp1][temp2] = digraph[temp1][temp2] + 1

        self.wordlist = wordlist
        self.digraph = digraph

    def test_case1(self):
        str1 = "as"
        str2 = "sun"
        expected_output = [1]
        actual_output = queryBridgeWords(str1, str2, self.wordlist, self.digraph)
        print(f"actual_output : {actual_output}")
        self.assertEqual(expected_output, actual_output)

    def test_case2(self):
        str1 = "they"
        str2 = "faces"
        expected_output = []
        actual_output = queryBridgeWords(str1, str2, self.wordlist, self.digraph)
        print(f"actual_output : {actual_output}")
        self.assertEqual(expected_output, actual_output)

    def test_case3(self):
        str1 = "behind"
        str2 = "one"
        expected_output = []
        actual_output = queryBridgeWords(str1, str2, self.wordlist, self.digraph)
        print(f"actual_output : {actual_output}")
        self.assertEqual(expected_output, actual_output)

    def test_case4(self):
        str1 = "on"
        str2 = "on"
        expected_output = []
        actual_output = queryBridgeWords(str1, str2, self.wordlist, self.digraph)
        print(f"actual_output : {actual_output}")
        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()

