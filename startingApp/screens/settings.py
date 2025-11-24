#This code is written to support the settings screen of the app.
#It works with the settings.kv file

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen #Wworks with screenmanager
from kivy.uix.button import Button #this imports the Button from settings.kv


class SettingsScreen(Screen):
    dark_mode = False

    def toggle_dark_mode(self):
        root = App.get_running_app().root  # RootWidget instance

        if not self.dark_mode:
            root.bg_source = "assets/DarkBackground.png"
            self.dark_mode = True
            print("Dark Mode enabled")
        else:
            root.bg_source = "assets/StandardBackground.png"
            self.dark_mode = False
            print("Dark Mode disabled")
