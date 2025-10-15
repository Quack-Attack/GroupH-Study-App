def validate_work_timer(time):
    if time >= 15 and time <= 60:
        return True
    return False
def validate_short_timer(time):
    if time >= 3 and time <= 15:
        return True
    return False
def validate_long_timer(time):
    if time >= 10 and time <= 45:
        return True
    return False