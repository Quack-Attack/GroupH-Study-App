#This code is written to support the todo screen of the app.
#It works with the todo.kv file

from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivy.metrics import dp


class ToDoScreen(MDScreen):
    
    def expand_input(self):
        """Expands the input section to show all task fields"""
        input_box = self.ids.input_box
        
        # Hide the initial "Add a new task..." field
        self.ids.new_task_input.opacity = 0
        self.ids.new_task_input.disabled = True
        
        # Animate height expansion
        anim = Animation(height=dp(200), duration=0.3)
        anim.start(input_box)
        
        # Show the additional fields
        self.ids.task_header_input.opacity = 1
        self.ids.task_description_input.opacity = 1
        self.ids.task_date_input.opacity = 1
        
    def addTask(self):
        """Adds a task with header, description, and due date"""
        
        # Get text from all inputs
        header = self.ids.task_header_input.text.strip()
        description = self.ids.task_description_input.text.strip()
        due_date = self.ids.task_date_input.text.strip()
        
        if header:
            # Add the task as a custom widget
            from kivymd.uix.boxlayout import MDBoxLayout
            from kivymd.uix.label import MDLabel
            
            task_row = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(50),
                padding=[dp(10), dp(5)],
                spacing=dp(10)
            )
            
            # Task Header (left side)
            header_label = MDLabel(
                text=header,
                size_hint_x=0.3,
                bold=True
            )
            
            # Task Description (middle)
            desc_label = MDLabel(
                text=description,
                size_hint_x=0.5
            )
            
            # Due Date (right side)
            date_label = MDLabel(
                text=due_date,
                size_hint_x=0.2,
                halign='right'
            )
            
            task_row.add_widget(header_label)
            task_row.add_widget(desc_label)
            task_row.add_widget(date_label)
            
            self.ids.todo_items_container.add_widget(task_row)
            
            # Clear all inputs
            self.ids.task_header_input.text = ""
            self.ids.task_description_input.text = ""
            self.ids.task_date_input.text = ""
            
            # Collapse the input box back
            self.collapse_input()
        
        else:
            print("No header entered")
    
    def collapse_input(self):
        """Collapses the input section back to minimal size"""
        input_box = self.ids.input_box
        
        # Hide additional fields
        self.ids.task_header_input.opacity = 0
        self.ids.task_description_input.opacity = 0
        self.ids.task_date_input.opacity = 0
        
        # Show the initial "Add a new task..." field again
        self.ids.new_task_input.opacity = 1
        self.ids.new_task_input.disabled = False
        
        # Animate height collapse
        anim = Animation(height=dp(60), duration=0.3)
        anim.start(input_box)
            