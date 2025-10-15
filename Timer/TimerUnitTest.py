import unittest
from timer_validator import validate_work_timer, validate_short_timer, validate_long_timer
class TestPomodoroTimer(unittest.TestCase):
    def test_valid_work_minutes(self):
         work_minutes = 15
         self.assertTrue(validate_work_timer(work_minutes))
    def test_invalid_work_minutes(self):
         work_minutes = 14
         self.assertFalse(validate_work_timer(work_minutes))
    def test_valid_short_break_minutes(self):
         short_break = 3
         self.assertTrue(validate_short_timer(short_break))
    def test_invalid_short_break_minutes(self):
         short_break = 2
         self.assertFalse(validate_short_timer(short_break))
    def test_valid_long_break_minutes(self):
         long_break = 10        
         self.assertTrue(validate_long_timer(long_break))
    def test_invalid_long_break_minutes(self):
         long_break = 9
         self.assertFalse(validate_long_timer(long_break))
if __name__ == '__main__':
    unittest.main()