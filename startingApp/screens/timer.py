#This code is written to support the timer screen of the app.
#It works with the timer.kv file

#from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen #Wworks with screenmanager
from kivy.uix.button import Button #this imports the Button from timer.kv


class TimerScreen(Screen):
    def OnSubmit(self):
        TextInput = self.ids.TextInput
        InputText = TextInput.text
        OutputLabel = self.ids.OutputLabel
        OutputLabel.text = InputText
        TextInput.text = ""
        
        self.add_widget(Label(text = "Tempus Fugits"))
        ToDoButton = Button(text='Wait')
        
        print("No, Go!")