import unittest
from datetime import datetime, timedelta
from date_validator import validate_date
from time_validator import validate_time
from datetime_validator import validate_datetime

class TestDateValidation(unittest.TestCase):
    def test_future_date(self):
        tomorrow = (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")             
        self.assertTrue(validate_date(tomorrow))
    def test_past_date(self):
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%m/%d/%Y")
        self.assertFalse(validate_date(yesterday))
    def test_current_date(self):
        today = datetime.today().strftime("%m/%d/%Y")
        self.assertTrue(validate_date(today))
    def test_empty_date(self):         
        self.assertFalse(validate_date(""))
    def test_impossible_date(self):           
        impossible_date = "13/32/2026"   
        self.assertFalse(validate_date(impossible_date))
    def test_malformed_date(self):           
        malformed_date = "10/27/20266"   
        self.assertFalse(validate_date(malformed_date))

class TestTimeValidation(unittest.TestCase):
    def test_valid_time(self):             
        currentTime = datetime.now()
        one_minute_later = (currentTime + timedelta(minutes=1)).strftime("%H:%M")
        self.assertTrue(validate_time(one_minute_later))
    def test_boundary_valid_empty_time(self):           
        empty_time = "00:00"
        self.assertTrue(validate_time(empty_time))
    def test_impossible_time(self):           
        impossible_time = "24:01"   
        self.assertFalse(validate_time(impossible_time))
    def test_malformed_time(self):           
        malformed_time = "12:61"   
        self.assertFalse(validate_time(malformed_time))

class TestDateTimeValidation(unittest.TestCase):
    def test_future_date_any_time_valid(self):
        future_date = (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
        self.assertTrue(validate_datetime(future_date, "00:00"))
        self.assertTrue(validate_datetime(future_date, "23:59"))
    def test_today_future_time_valid(self):
        today = datetime.today().strftime("%m/%d/%Y")
        future_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
        self.assertTrue(validate_datetime(today, future_time))
    def test_today_past_time_invalid(self):
        today = datetime.today().strftime("%m/%d/%Y")
        past_time = (datetime.now() - timedelta(minutes=1)).strftime("%H:%M")
        self.assertFalse(validate_datetime(today, past_time))
    def test_past_date_invalid(self):
        past_date = (datetime.today() - timedelta(days=1)).strftime("%m/%d/%Y")
        self.assertFalse(validate_datetime(past_date, "12:00"))
    def test_invalid_format(self):
        self.assertFalse(validate_datetime("1/1/2025", "12:00"))
        self.assertFalse(validate_datetime("01/01/2025", "12:60"))

if __name__ == '__main__':
    unittest.main()