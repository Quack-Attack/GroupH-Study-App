import unittest

def validate_string_list(string_list):
    if not isinstance(string_list, list):
        raise TypeError("Input must be a list of strings.")

    for s in string_list:
        if not isinstance(s, str):
            raise ValueError(f"All items must be strings. Found: {type(s)}")
        if not (0 < len(s) < 255):
            return False
    return True


class TestValidateStringList(unittest.TestCase):
    def test_valid_list(self):
        self.assertTrue(validate_string_list(["apple", "banana", "cherry"]))

    def test_empty_string(self):
        self.assertFalse(validate_string_list(["apple", ""]))

    def test_too_long_string(self):
        long_str = "a" * 255
        self.assertFalse(validate_string_list(["apple", long_str]))

    def test_non_string_item(self):
        with self.assertRaises(ValueError):
            validate_string_list(["apple", 123])

    def test_not_a_list(self):
        with self.assertRaises(TypeError):
            validate_string_list("not a list")


if __name__ == "__main__":
    unittest.main()
