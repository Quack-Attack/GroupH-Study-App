#This code is written to support the todo screen of the app.
#It works with the todo.kv file

#from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen #works with screenmanager
from kivy.uix.button import Button #this imports the Button from todo.kv


class ToDoScreen(Screen):
    def OnSubmit(self):
        TextInput = self.ids.TextInput
        InputText = TextInput.text
        OutputLabel = self.ids.OutputLabel
       
        OutputLabel.text = InputText
        TextInput.text = ""
        
        print("entered todo screen")
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="ToDo Screen Loaded!"))
        
    def GoToSettings(self):
        print("going to settings..")
        self.manager.current = "settings"