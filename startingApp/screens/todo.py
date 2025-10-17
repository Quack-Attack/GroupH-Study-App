#This code is written to support the todo screen of the app.
#It works with the todo.kv file

#from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen #works with screenmanager


class ToDoScreen(Screen):
        
    def addTask(self):
        print("addTask running") #debug line
        #holds text from the input
        textIn = self.ids.new_task_input.text.strip()
        
        if textIn:
            
            #each task gets a new label
            newTask = Label(text = textIn, size_hint_y = None, height = 30)
            #Adds it to the todo_items_container built in study.kv
            self.ids.todo_items_container.add_widget(newTask)
            #clears the input
            self.ids.new_task_input.text = ""
        
        else:
            print("No text entered")
            