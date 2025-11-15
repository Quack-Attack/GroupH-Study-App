# todo.py
# Supports the To-Do screen defined in your todo.kv

from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock

import re
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.button import MDIconButton

import json
from pathlib import Path
from functools import partial

# Save file next to this python file (safer than CWD)
DATA_FILE = Path(__file__).parent / "todo_items.json"

def load_tasks():
    """Load JSON tasks, return list on success or empty list on error."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception as e:
        # If the file is corrupted or unreadable, warn and return empty list.
        print(f"Warning: couldn't load tasks ({e}). Starting with empty list.")
    return []

def save_tasks(task_list):
    """Save list of tasks to JSON (pretty-printed)."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(task_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving tasks: {e}")


class ToDoScreen(MDScreen):
    def on_kv_post(self, base_widget):
        """
        Called after kv rules are applied and ids exist.
        Load tasks and set initial UI visibility for input fields.
        """
        # Ensure UI changes happen after anything else finishes
        Clock.schedule_once(self._post_kv_setup, 0)

    def _post_kv_setup(self, dt):
        # Load saved tasks
        self.task_list = load_tasks()

        # Ensure input fields exist in kv (defensive)
        try:
            # Start with compact state: show single-line new_task_input only
            self.ids.task_header_input.opacity = 0
            self.ids.task_header_input.disabled = True

            self.ids.task_description_input.opacity = 0
            self.ids.task_description_input.disabled = True

            self.ids.task_date_input.opacity = 0
            self.ids.task_date_input.disabled = True

            self.ids.new_task_input.opacity = 1
            self.ids.new_task_input.disabled = False
        except Exception as e:
            print("Warning: input fields not found in kv:", e)

        # Render any loaded tasks
        self.render_tasks()

    def expand_input(self):
        """Expands the input section to show all task fields"""
        input_box = self.ids.input_box

        # Hide the initial "Add a new task..." field
        self.ids.new_task_input.opacity = 0
        self.ids.new_task_input.disabled = True

        # Animate height expansion
        anim = Animation(height=dp(200), duration=0.18)
        anim.start(input_box)

        # Show and enable the additional fields
        for idn in ("task_header_input", "task_description_input", "task_date_input"):
            try:
                self.ids[idn].opacity = 1
                self.ids[idn].disabled = False
            except Exception:
                pass

    def collapse_input(self):
        """Collapses the input section back to minimal size"""
        input_box = self.ids.input_box

        # Hide additional fields and disable them
        for idn in ("task_header_input", "task_description_input", "task_date_input"):
            try:
                self.ids[idn].opacity = 0
                self.ids[idn].disabled = True
            except Exception:
                pass

        # Show the initial "Add a new task..." field again
        try:
            self.ids.new_task_input.opacity = 1
            self.ids.new_task_input.disabled = False
        except Exception:
            pass

        # Animate height collapse
        anim = Animation(height=dp(60), duration=0.18)
        anim.start(input_box)

    from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogButtonContainer,
    )
    from kivymd.uix.button import MDButton, MDButtonText

    def show_error(self, message):
        self.dialog = MDDialog(
            children=[
                MDDialogHeadlineText(
                    text="Invalid Input",
                ),
                MDDialogButtonContainer(
                    children=[
                        MDButton(
                            style="elevated",
                            on_release=lambda btn: self.dialog.dismiss(),
                            children=[
                                MDButtonText(text="OK")
                            ],
                        )
                    ]
                ),
            ],
            text=message,  # <-- this is allowed because children is ONE argument
        )
        self.dialog.open()

    # --- Unified add + save ---
    def addTask(self):
        """
        Adds a task (both to the UI and saved JSON).
        This name matches your KV call: on_release: root.addTask()
        """
        # Defensive: ensure attributes exist
        header = ""
        description = ""
        due_date = ""
        try:
            header = self.ids.task_header_input.text.strip()
            description = self.ids.task_description_input.text.strip()
            due_date = self.ids.task_date_input.text.strip()
        except Exception:
            print("Input fields missing or not ready.")
            return

        if not header:
            # Do not add blank-header tasks
            print("No header entered")
            return
        
        # Compile the expected formatting for the due dates
        DATE_REGEX = re.compile(
            r"^(0[1-9]|1[0-2])/?([0-2][0-9]|3[0-1])/?([0-9]{4})$"
            )

        date_text = self.ids.task_date_input.text.strip()
        if date_text and not DATE_REGEX.match(date_text):
            self.show_error("\n\nDate must be MM/DD/YYYY\n\n")
            return  # stop saving the task

        # Build task dictionary and append
        task = {"header": header, "description": description, "due_date": due_date}
        if not hasattr(self, "task_list"):
            self.task_list = load_tasks()
        self.task_list.append(task)

        # Persist
        save_tasks(self.task_list)

        # Refresh UI
        self.render_tasks()

        # Clear inputs
        try:
            self.ids.task_header_input.text = ""
            self.ids.task_description_input.text = ""
            self.ids.task_date_input.text = ""
        except Exception:
            pass

        # Collapse input box back
        self.collapse_input()

    def delete_task(self, index):
        """Removes a task from the list and re-saves it (safe against bad indexes)."""
        try:
            # Safe pop: check range
            if 0 <= index < len(self.task_list):
                self.task_list.pop(index)
                save_tasks(self.task_list)
                self.render_tasks()
            else:
                print("delete_task: index out of range:", index)
        except Exception as e:
            print("Error deleting task:", e)

    def _make_delete_btn(self, index: int) -> MDIconButton:
        # Create the button
        btn = MDIconButton(
            icon="delete",
            # Optional, depending on theme
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),  # red delete button
            size_hint=(None, None),
            size=(dp(36), dp(36)),
        )

        # Bind the callback AFTER creation
        def on_release_handler(btn_widget):
            self.delete_task(index)

        btn.bind(on_release=on_release_handler)
        return btn
        
    def render_tasks(self):
        """Clear and rebuild the task list display"""
        # Defensive: ensure we have a container and task_list
        try:
            container = self.ids.todo_items_container
        except Exception as e:
            print("render_tasks: missing todo_items_container in kv:", e)
            return

        container.clear_widgets()

        # If no tasks, show a placeholder label (optional)
        if not getattr(self, "task_list", None):
            from kivymd.uix.label import MDLabel
            placeholder = MDLabel(text="No tasks yet", halign="center", size_hint_y=None, height=dp(40))
            container.add_widget(placeholder)
            return

        # Build each row
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel

        for index, task in enumerate(self.task_list):
            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(50),
                padding=[dp(10), dp(5)],
                spacing=dp(10),
            )

            # header
            row.add_widget(
                MDLabel(text=task.get("header", ""), size_hint_x=0.3, bold=True, valign="middle")
            )

            # description
            row.add_widget(
                MDLabel(text=task.get("description", ""), size_hint_x=0.5, valign="middle")
            )

            # due date, right aligned
            row.add_widget(
                MDLabel(text=task.get("due_date", ""), size_hint_x=0.2, halign="right", valign="middle")
            )

            row.add_widget(self._make_delete_btn(index))

            container.add_widget(row)

    
