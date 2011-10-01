# -*- coding: utf-8 -*-
import unittest
from UnihanDictDesktop import UnihanDictDesktop as UnihanDict


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.unihan = UnihanDict()
        self.unihan.load()
        self.unihan.set_pinyin_type(pinyin=1)
        
    def test_unihan_dict(self):
        u = self.unihan.unihan_dict
        self.assertEqual(u['u6f22'], 'han4 tan1') # pinyin of \u6f22 is: han4 tan1

        
    def test_convert(self):
        hanzi = u"\u6F22"
        pinyin = self.unihan.convert(hanzi)
        print hanzi + " : " + pinyin
        self.assertEqual(pinyin, u"\u6F22	(han4-tan1)") # test output of convert

        
if __name__ == '__main__':
    unittest.main()
