import unittest
from deck_validator import validate_deck

class TestDeckValidator(unittest.TestCase):
    def test_valid_deck(self):
        self.assertTrue(validate_deck(1))    # check edge case, this is 1

    def test_invalid_deck(self):
        self.assertFalse(validate_deck(None))    # check edge case, this is 0

    def test_valid_large_deck(self):
        large_deck = 10_000  # large integer, should be able to add as many cards in the deck as they want
        self.assertTrue(validate_deck(large_deck))


if __name__ == '__main__':
    unittest.main()
