#Terry Nguyen
#Unit test for timer based on equivalence partitions

import unittest
from timer_validator import validate_work_timer, validate_short_timer, validate_long_timer
class TestPomodoroTimer(unittest.TestCase):
    
    def test_valid_work_minutes(self):                           #tests if minutes for working are valid (15-60 minutes) 
         work_minutes = 15                                       #test with 15 minutes
         self.assertTrue(validate_work_timer(work_minutes))
         work_minutes = 60                                       #test with 60 minutes
         self.assertTrue(validate_work_timer(work_minutes))      

    def test_invalid_work_minutes(self):                         #tests if minutes for working are NOT valid (less than 15/greater than 60)
         work_minutes = 14                                       #test with 14 minutes
         self.assertFalse(validate_work_timer(work_minutes))
         work_minutes = 61                                       #test with 61 minutes
         self.assertFalse(validate_work_timer(work_minutes))

    def test_valid_short_break_minutes(self):                    #tests if minutes for short breaks are valid (3-15)
         short_break = 3                                         #test with 3 minutes
         self.assertTrue(validate_short_timer(short_break))
         short_break = 15                                        #test with 15 minutes
         self.assertTrue(validate_short_timer(short_break))

    def test_invalid_short_break_minutes(self):                  #tests if minutes for short breaks are NOT valid (less than 3/greater than 15)
         short_break = 2                                         #test with 2 minutes
         self.assertFalse(validate_short_timer(short_break))
         short_break = 16                                        #test with 16 minutes
         self.assertFalse(validate_short_timer(short_break))
         
    def test_valid_long_break_minutes(self):                     #tests if minutes for long breaks are valid (10-45)
         long_break = 10                                         #test with 10 minutes
         self.assertTrue(validate_long_timer(long_break))
         long_break = 45                                         #test with 45 minutes
         self.assertTrue(validate_long_timer(long_break))

    def test_invalid_long_break_minutes(self):                   #test if minutes for long breaks are NOT valid (less than 10/greater than 45)
         long_break = 9                                          #test with 9 minutes
         self.assertFalse(validate_long_timer(long_break))
         long_break = 46                                         #test with 46 minutes
         self.assertFalse(validate_long_timer(long_break))
         
# if all tests succeed, ends with 'OK'.

if __name__ == '__main__':
    unittest.main()