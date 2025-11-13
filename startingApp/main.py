

'''This is the management script.
    Here, all screens are imported and added 
    as widgets. Each has a button that is also 
    built and used throuought the screens. The
    script ends with the all important run statement.'''


from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import FloatLayout #this imports the FloatLayout from study.kv

from screens.todo import ToDoScreen #ToDo screen is incomplete, but this is the import call for the todo screen
from screens.flashCards import FlashCardsScreen #FlashCards screen is incomplete, but this is the import call for the flash cards screen
from screens.timer import TimerScreen #Timer screen is incomplete, but this is the import call for the flash cards screen
from screens.settings import SettingsScreen #to be activated when the Settings screen is online

#from kivy.lang import Builder #this line and the one below would be needed if the .kv file for main were named
                                #something other than 'study' because kivy likes the name to be the same as the 
#Builder.load_file('study.kv')  #class name without the 'App' part

#class WindowManager(ScreenManager):
#    pass

#class RootWidget(FloatLayout):
#    pass

class StudyApp(MDApp):
    def build(self):
        
      
        sm = MDScreenManager() #building and naming the app's main manager
        
        sm.add_widget(ToDoScreen(name = "todo")) #adds the ToDo screen widget
        sm.add_widget(FlashCardsScreen(name = "flashCards")) #adds the flashcards screen widget
        sm.add_widget(TimerScreen(name = "time  r")) #adds the timer screen widget
        sm.add_widget(SettingsScreen(name = "settings")) #adds the settings screen widget

        sm.current = "todo"
        
        # returns root widget from study.kv
        from kivy.factory import Factory
        return Factory.RootWidget()
    
if __name__ == "__main__":
    StudyApp().run()