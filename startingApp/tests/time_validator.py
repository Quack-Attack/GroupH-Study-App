import re
from datetime import datetime, timedelta

def validate_time(time_str: str) -> bool:
    # Check format first (exactly two digits:two digits)
    if not re.fullmatch(r"\d{2}:\d{2}", time_str):
        return False

    try:
        hours, minutes = map(int, time_str.split(":"))
        # Check that time is within valid range
        if not (0 <= hours < 24 and 0 <= minutes < 60):
            return False
    except ValueError:
        return False



    return True