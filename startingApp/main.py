# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 17:55:57 2025

@author: rnpeo
"""

'''This is the management script.
    Here, all screens are imported and added 
    as widgets. Each has a button that is also 
    built and used throuought the screens. The
    script ends with the all important run statement.'''

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
#from kivy.uix.button import Button #this imports the Button from study.kv

from screens.todo import ToDoScreen #ToDo screen is incomplete, but this is the import call for the todo screen
from screens.flashCards import FlashCardsScreen #FlashCards screen is incomplete, but this is the import call for the flash cards screen
from screens.timer import TimerScreen #Timer screen is incomplete, but this is the import call for the flash cards screen
from screens.settings import SettingsScreen #to be activated when the Settings screen is online

#from kivy.lang import Builder #this line and the one below would be needed if the .kv file for main were named
                                #something other than 'study' because kivy likes the name to be the same as the 
#Builder.load_file('study.kv')  #class name without the 'App' part

class WindowManager(ScreenManager):
    pass

class ToDoScreen(Screen):
    pass

class FlashCardsScreen(Screen):
    pass

class TimerScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass    

class StudyApp(App):
    def build(self):
       
        sm = WindowManager() #building and naming the app's main manager
        
        sm.add_widget(ToDoScreen(name = "todo")) #adds the ToDo screen widget
        sm.add_widget(FlashCardsScreen(name = "flashCards")) #adds the flashcards screen widget
        sm.add_widget(TimerScreen(name = "timer")) #adds the timer screen widget
        sm.add_widget(SettingsScreen(name = "settings")) #adds the settings screen widget

        sm.current = "todo"
        
        return sm
    
if __name__ == "__main__":
    StudyApp().run()