"""
Author: Phyo Thiha
Last Modified Date: April 13, 2017
Description:
Different similarity metrics wrapped in one module. The metrics are:
 1. Jaccard similarity
 2. Common word count
 3. Longest common subsequence
 4. Damerau Levenshtein (normalized)
 5. Jaro-Winkler

Note: 'Jellyfish' library is needed. For that, just install by:
>> pip install jellyfish
"""

import unittest
from collections import Counter

from jellyfish import damerau_levenshtein_distance,jaro_distance


class WordSimilarity(object):

    @staticmethod
    def jaccard_similarity_score(w1, w2):
        intersection = len(set.intersection(*[set(w1), set(w2)]))
        union = len(set.union(*[set(w1), set(w2)]))
        return intersection / float(union)

    @staticmethod
    def common_char_count_ratio(w1, w2):
        return WordSimilarity.calculate_common_ratio(list(w1), list(w2))

    @classmethod
    def calculate_common_ratio(cls, w1, w2):
        l1 = Counter(list(w1))
        l2 = Counter(list(w2))
        common_chars = set.intersection(set(l1.keys()), set(l2.keys()))
        sum_of_least_common_chars_count = sum([(lambda c: min(l1[c],l2[c]))(c) for c in common_chars])
        return sum_of_least_common_chars_count / float(max(len(w1), len(w2))) # float(len(w1)+len(w2))

    @classmethod
    def longest_common_substring(cls, s1, s2):
        """
        From: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python_3
        """
        m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
        longest, x_longest = 0, 0
        for x in range(1, 1 + len(s1)):
            for y in range(1, 1 + len(s2)):
                if s1[x - 1] == s2[y - 1]:
                    m[x][y] = m[x - 1][y - 1] + 1
                    if m[x][y] > longest:
                        longest = m[x][y]
                        x_longest = x
                else:
                    m[x][y] = 0
        return s1[x_longest - longest: x_longest]

    @staticmethod
    def lcs_score(w1, w2):
        """
        Inspired by:
        http://www.oracle.com/webfolder/technetwork/data-quality/edqhelp/Content/processor_library/matching/comparisons/longest_common_substring_percentage.htm
        """
        lcs = WordSimilarity.longest_common_substring(w1, w2)
        return len(lcs) / float(max(len(w1), len(w2)))

    @staticmethod
    def damerau_levenshtein_score(w1, w2):
        d_leven = damerau_levenshtein_distance(w1, w2)
        return 1.0 - (d_leven / float(max(len(w1), len(w2))))

    @staticmethod
    def jaro_winkler_score(w1, w2):
        return jaro_distance(w1, w2) # jellyfish's method name for Jaro-Winkler is just jaro_distance()


class TestOutputSimilarityScores(unittest.TestCase):

    def test_expected_scores(self):
        o = WordSimilarity()
        sa = 'abcc'
        sb = 'cdeff'
        sc = 'ccdeff'
        sd = 'Hallo'
        se = 'Hello'

        self.assertEqual(o.jaccard_similarity_score(sa, sb), 1 / 6.0)
        self.assertEqual(o.common_char_count_ratio(sa, sb), 1 / 5.0)
        self.assertEqual(o.common_char_count_ratio(sa, sc), 1 / 3.0)
        self.assertEqual(o.longest_common_substring(sa, sc), 'cc')
        self.assertEqual(o.lcs_score(sa, sc), 1 / 3.0)
        self.assertEqual(o.longest_common_substring(sa, sb), 'c')
        self.assertEqual(o.lcs_score(sa, sb), 1 / 5.0)
        self.assertEqual(o.damerau_levenshtein_score(sa, sa), 1.0)
        self.assertEqual(o.damerau_levenshtein_score(sa, sb), 0)
        self.assertEqual(o.damerau_levenshtein_score(sa, sc), 0)

        # Jaro distance sometimes suffers when prefixes (up to half of max string length) don't match
        self.assertEqual(o.jaro_winkler_score(sa, sb), 0)
        # but in cases like below, it does just fine
        self.assertEqual(o.jaro_winkler_score(sa, sc), 0.611111111111111)
        self.assertEqual(o.jaro_winkler_score(sd, se), 0.8666666666666667)


if __name__ == "__main__":
    unittest.main()
