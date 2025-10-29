import re
from datetime import datetime
from date_validator import validate_date
from time_validator import validate_time

def validate_datetime(date_str: str, time_str: str) -> bool:
    """Validates date and time together.
       - Ensures date/time are formatted correctly and valid.
       - Fails if date is today and time is before now.
    """
    if not (validate_date(date_str) and validate_time(time_str)):
        return False

    try:
        combined = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M")
        now = datetime.now()
        today = now.date()

        # If it's today, reject if time is before now
        if combined.date() == today and combined < now:
            return False

        # If date is valid and not before today, it's fine
        return combined.date() >= today
    except ValueError:
        return False