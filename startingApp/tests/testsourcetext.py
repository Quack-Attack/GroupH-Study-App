import unittest
from sourcetext_validator import validate_sourcetext


class TestSourceText(unittest.TestCase):
    def test_valid_source_text(self):
        self.assertTrue(validate_sourcetext("a"))    # test a short text, 1 char

    def test_invalid_sourcetext(self):
        self.assertFalse(validate_sourcetext(""))    # test no text

    def test_valid_long_sourceText(self):
        long_source = "a" * 10000
        self.assertTrue(validate_sourcetext(long_source))    # test a long test, user should be able to use a text as long as they want


if __name__ == '__main__':
    unittest.main()
