import unittest
from sourcetext_validator import validate_sourcetext
from deck_validator import validate_deck


class TestSourceText(unittest.TestCase):
    def test_valid_source_text(self):
        self.assertTrue(validate_sourcetext("a"))

    def test_invalid_sourcetext(self):
        self.assertFalse(validate_sourcetext(""))

    def test_valid_long_sourceText(self):
        long_source = "a" * 10000
        self.assertTrue(validate_sourcetext(long_source))


if __name__ == '__main__':
    unittest.main()
