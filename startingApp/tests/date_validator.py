import re
from datetime import datetime

def validate_date(date: str) -> bool:
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", date):
        return False
    
    try:
        # Try to parse it — this automatically checks if day/month/year are valid
        parsed_date = datetime.strptime(date, "%m/%d/%Y").date()
    except ValueError:
        # Raised if day/month/year are out of bounds
        return False
    
    today = datetime.today().date()

    # Fail if the date is before today
    if parsed_date < today:
        return False
    
    return True