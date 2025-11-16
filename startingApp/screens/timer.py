#This code is written to support the timer screen of the app.
#It works with the timer.kv file

#from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen #Works with screenmanager
from kivy.uix.button import Button #this imports the Button from timer.kv
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen


class TimerScreen(MDScreen):
    # Timer string to display on screen
    timer_text = StringProperty("00:00")

    # internal timer counters
    remaining_seconds = NumericProperty(0)

    # session states
    current_session = 0
    total_sessions = 4
    mode = "work"           # work / short_break / long_break

    # Clock event
    clock_event = None

    def start_pomodoro(self):
        """Starts or resumes the timer."""
        if self.clock_event:      # If already running, ignore
            return

        # If timer is at 0, we need to initialize a new cycle
        if self.remaining_seconds == 0:
            self._load_current_session_time()

        # Start ticking
        self.ids.timer_display.text = self.timer_text
        self.clock_event = Clock.schedule_interval(self._update_timer, 1)
        self._update_timer(0)
    
    def stop_pomodoro(self):
        """Stops (pauses) the timer."""
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event = None

    def reset_pomodoro(self):
        """Resets everything to initial state."""
        self.stop_pomodoro()
        self.remaining_seconds = 0
        self.current_session = 0
        self.mode = "work"
        self.timer_text = "00:00"
        self.ids.status_label.text = "Press Start to begin."

    # ------------------------------
    #      SESSION / TIMER LOGIC
    # ------------------------------

    def _load_current_session_time(self):
        """Loads timer duration based on mode."""
        work = float(self.ids.work_minutes_input.text) * 60
        short_break = float(self.ids.short_break_minutes_input.text) * 60
        long_break = float(self.ids.long_break_minutes_input.text) * 60

        self.total_sessions = int(self.ids.sessions_input.text)

        if self.mode == "work":
            self.remaining_seconds = work

        elif self.mode == "short_break":
            self.remaining_seconds = short_break

        elif self.mode == "long_break":
            self.remaining_seconds = long_break

        self.update_status_label()

    def _update_timer(self, dt):
        """Called every second; updates countdown & screen text."""
        if self.remaining_seconds <= 0:
            self._move_to_next_phase()
            return

        self.remaining_seconds -= 1
        self._update_timer_display()


    def _move_to_next_phase(self):
    # stop ticking to avoid double-calls
        self.stop_pomodoro()

        # If work is done and it isn't the last session, go to short break
        if self.mode == "work" and self.current_session < self.total_sessions - 1:
            self.mode = "short_break"
            
        # If work is done and it is the last session, go to long break
        elif self.mode == "work":
            self.mode = "long_break"

        # If short break is done, go back to work
        elif self.mode == "short_break":
            self.current_session += 1
            self.mode = "work"

        # If long break is done, stop completely and reset
        elif self.mode == "long_break":
            self.stop_pomodoro()
            self.remaining_seconds = 0
            self.current_session = 0
            self.mode = "work"
            self.timer_text = "00:00"
            self.ids.status_label.text = "All Pomodoro sessions completed!"
            return

    # Load time for the next mode and restart timer
        self._load_current_session_time()
        self.update_status_label()
        self.start_pomodoro()

    # ------------------------------
    #          UI UPDATE
    # ------------------------------

    def _update_timer_display(self):
        minutes = int(self.remaining_seconds // 60)
        seconds = int(self.remaining_seconds % 60)
        self.timer_text = f"{minutes:02d}:{seconds:02d}"

        # Display on actual label
        self.ids.timer_display.text = self.timer_text

    def update_status_label(self):
        mode_pretty = {
            "work": "Work Session",
            "short_break": "Short Break",
            "long_break": "Long Break",
        }[self.mode]

        self.ids.status_label.text = (
            f"{mode_pretty} — Session {self.current_session + 1} of {self.total_sessions}"
        )

    def OnSubmit(self):
        
        self.add_widget(Label(text = "Tempus Fugits"))
        