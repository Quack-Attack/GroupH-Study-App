import unittest
from sourcetext_validator import validate_sourcetext

class TestDeckValidator(unittest.TestCase):
    def test_valid_deck(self):
        self.assertTrue(validate_deck(5))

    def test_invalid_deck(self):
        self.assertFalse(validate_deck(None))

    def test_valid_large_deck(self):
        large_deck = 10_000  # large integer
        self.assertTrue(validate_deck(large_deck))


if __name__ == '__main__':
    unittest.main()