#Terry Nguyen
#validates minutes in the unit test for timer

def validate_work_timer(time):          #validates minutes for working
    if time >= 15 and time <= 60:       #true if minutes are greater or equal to 15 and less or equal to 60
        return True
    return False                        #otherwise false

def validate_short_timer(time):         #validates minutes for short breaks
    if time >= 3 and time <= 15:        #true if minutes are greater or equal to 3 and less or equal to 15
        return True
    return False                        #otherwise false

def validate_long_timer(time):          #validates minutes for long breaks
    if time >= 10 and time <= 45:       #true if minutes are greater or equal to 10 and less or equal to 45
        return True
    return False                        #otherwise false