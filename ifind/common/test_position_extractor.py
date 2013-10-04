__author__ = 'rose'
import unittest
import logging
import sys
from position_query_extractor import PositionQueryExtractor

class TestPositionExtractor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestStructuredExtractor")
        html = ' <html> <div id="header"><h1>hello world</h1>' \
               '</div><div id="content"><p>this is important</p>' \
               '<p> study computing it is fun</p></div>' \
               '<div id="footer"> <h2>byes</h2></div> </html> '
        div_ids=[]
        self.extractor = PositionQueryExtractor(html=html, div_ids=div_ids)

    def test_remove_div_content(self):

        div_id=["header"]
        self.extractor.set_div_ids(div_id)
        expected = "this is important study computing it is fun byes"
        result = self.extractor.remove_div_content()
        self.process_test_equals(expected,result)
        div_id=["content"]
        expected = "hello world byes"
        self.extractor.set_div_ids(div_id)
        result = self.extractor.remove_div_content()
        self.process_test_equals(expected,result)
        #test multiple div removal
        ignore_divs = ['header','footer']
        self.extractor.set_div_ids(ignore_divs)
        result = self.extractor.remove_div_content()
        expected = 'this is important study computing it is fun'
        self.process_test_equals(expected, result)

    def test_get_subtext(self):
        text = "this is a sentence which has some words in it"
        result = self.extractor.get_subtext(text,num_words=2)
        expected = "this is"
        self.process_test_equals(expected,result)
        #test greater than length returns whole text
        result = self.extractor.get_subtext(text, num_words=12)
        self.process_test_equals(text, result)

    def test_generate_queries(self):
        #test removing div content and generating queries from result
        expected = ['this important','important study','study computing','computing fun']
        self.extractor.set_div_ids(["header","footer"])
        main_text = self.extractor.remove_div_content()
        result = self.extractor.generate_queries(main_text)
        self.process_test_equals(expected, result)
        #test removing div content, and then using only first 4 words
        #todo this looks at words before cleaned, should we be cleaning
        #them first, cleaning happens in query gen
        expected = ["this important",'important study']
        reduced_text = self.extractor.get_subtext(main_text,4)
        result = self.extractor.generate_queries(reduced_text)
        self.process_test_equals(expected,result)

    def process_test_equals(self, expected, result):
        msg = 'expected  but got ', expected,result
        self.assertItemsEqual(expected, result, msg)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestPositionExtractor").setLevel(logging.DEBUG)
    unittest.main(exit=False)
