#This code is written to support the todo screen of the app.
#It works with the todo.kv file

from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen #works with screenmanager


class ToDoScreen(MDScreen):
        
    def addTask(self):
        
        #accepts text from the input
        textIn = self.ids.new_task_input.text.strip()
        
        if textIn:
            
            # Add the task as a OneLineListItem
            self.ids.todo_items_container.add_widget(OneLineListItem(text=textIn))
            
            #clears the input
            self.ids.new_task_input.text = ""
        
        else:
            print("No text entered")
            