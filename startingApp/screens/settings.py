#This code is written to support the settings screen of the app.
#It works with the settings.kv file

#from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen #Wworks with screenmanager
from kivy.uix.button import Button #this imports the Button from settings.kv


class SettingsScreen(Screen):
    def GoToToDo(self):
        #goes back to the ToDo screen
        
        print("I'm losing it")
        
        self.manager.current = "todo" #calls the todo screen