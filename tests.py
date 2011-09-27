# -*- coding: utf-8 -*-
import unittest
from name_tr_mod import UnihanDict


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.unihan = UnihanDict()
        self.unihan.load()
        self.unihan.set_pinyin_type(pinyin=1)
    def test_pinyin(self):
        hanzi = u"æ¼¢"
        pinyin = self.unihan.convert(hanzi)
        print hanzi + " : " + pinyin
        self.assertEqual(pinyin, u"æ¼¢	(han4-tan1)")

        
if __name__ == '__main__':
    unittest.main()
