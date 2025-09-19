import time

def pomodoro_timer(work_minutes, short_break, long_break, sessions):
    for session in range(1, sessions + 1):
        print(f"\nSession {session} - Work for {work_minutes} minutes!")                #timer for working
        countdown(work_minutes * 60)
        

        if session < sessions:
            print(f"\nTake a short break for {short_break} minutes!")                   #timer for short break
            countdown(short_break * 60)
        else:
            print(f"\nGreat job! Take a long break for {long_break} minutes!")          #timer for long break for last session
            countdown(long_break * 60)
        session += 1                                                                    #goes to next session

def countdown(seconds):                                                                 #timer
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print("00:00")

if __name__ == "__main__":
    try:
        sessions = int(input("How many work sessions would you like? \n"))              #asks amount of sessions
    except ValueError:
        print("Invalid input, defaulting to 4 sessions.")                               #if invalid, sets to 4 by default
        sessions = 4
    print("\nPomodoro Timer Started!")                                                  #states the timer has started
    pomodoro_timer(1,1,2,sessions)                                                      #starts timer w/ default testing values 