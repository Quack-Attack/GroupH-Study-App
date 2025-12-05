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
from datetime import datetime, timedelta
from typing import List

from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox  # <-- NEW

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


# ==================== INPUT VALIDATION FUNCTIONS (CWE-20) ====================

def validate_task_title(title: str) -> tuple[bool, str]:
    """
    Validate task title to prevent injection attacks (CWE-20).
    Returns: (is_valid, error_message)
    """
    if not title or not isinstance(title, str):
        return False, "Task title cannot be empty!"
    
    # Enforce length constraints
    if len(title) < 1 or len(title) > 100:
        return False, "Task title must be between 1 and 100 characters!"
    
    # Check for potentially dangerous patterns
    dangerous_patterns = ['<script', '</script>', 'javascript:', 'onerror=', 
                         'onclick=', '<iframe', 'eval(', 'DROP TABLE', 
                         'DELETE FROM', '--', '/*', '*/']
    
    title_lower = title.lower()
    for pattern in dangerous_patterns:
        if pattern in title_lower:
            return False, f"Task title contains dangerous pattern: {pattern}"
    
    # Allow only safe characters: letters, numbers, spaces, and basic punctuation
    if not re.match(r'^[a-zA-Z0-9\s\.,!?\-\(\)\'\"]+$', title):
        return False, "Task title contains invalid characters!"
    
    return True, ""


def validate_task_description(description: str) -> tuple[bool, str]:
    """
    Validate task description with stricter limits (CWE-20).
    Returns: (is_valid, error_message)
    """
    if not description:
        return True, ""  # Description is optional
    
    if not isinstance(description, str):
        return False, "Invalid description format!"
    
    # Enforce maximum length to prevent resource exhaustion
    if len(description) > 500:
        return False, "Description too long! Maximum 500 characters allowed."
    
    # Check for dangerous patterns (XSS/SQL injection)
    dangerous_patterns = ['<script', '</script>', 'javascript:', 'onerror=',
                         'onclick=', '<iframe', 'eval(', 'DROP TABLE',
                         'DELETE FROM', 'INSERT INTO', 'UPDATE ', '--', '/*']
    
    desc_lower = description.lower()
    for pattern in dangerous_patterns:
        if pattern in desc_lower:
            return False, f"Description contains dangerous pattern: {pattern}"
    
    return True, ""


def validate_due_date(due_date: str) -> tuple[bool, str]:
    """
    Validate due date format and logical constraints (CWE-20).
    Accepts MM/DD/YYYY format (current UI format).
    Returns: (is_valid, error_message)
    """
    if not due_date or not isinstance(due_date, str):
        return True, ""  # Date is optional
    
    # Remove whitespace
    due_date = due_date.strip()
    
    if not due_date:  # Empty after stripping
        return True, ""
    
    # Validate format: MM/DD/YYYY (matching current UI format)
    if not re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(\d{4})$', due_date):
        return False, "Invalid date format! Use MM/DD/YYYY (e.g., 12/31/2025)"
    
    # Parse and validate the date
    try:
        parsed_date = datetime.strptime(due_date, '%m/%d/%Y')
    except ValueError:
        return False, "Invalid date! Please check the day/month values."
    
    # Check if date is not too far in the past (allow up to 1 day in past for flexibility)
    if parsed_date < datetime.now() - timedelta(days=1):
        return False, "Due date cannot be in the past!"
    
    # Prevent unreasonably far future dates (max 5 years)
    if parsed_date > datetime.now() + timedelta(days=1825):
        return False, "Due date too far in the future! Maximum 5 years allowed."
    
    return True, ""


def validate_tags(tags: List[str]) -> tuple[bool, str]:
    """
    Validate tags list to prevent injection (CWE-20).
    Returns: (is_valid, error_message)
    """
    if not tags:
        return True, ""  # Tags are optional
    
    if not isinstance(tags, list):
        return False, "Tags must be provided as a list!"
    
    # Limit number of tags
    if len(tags) > 10:
        return False, "Too many tags! Maximum 10 tags allowed."
    
    for tag in tags:
        if not isinstance(tag, str):
            return False, "Each tag must be a string!"
        
        # Validate each tag
        if len(tag) < 1 or len(tag) > 20:
            return False, "Each tag must be 1-20 characters!"
        
        # Only allow alphanumeric and hyphens
        if not re.match(r'^[a-zA-Z0-9\-]+$', tag):
            return False, f"Invalid tag '{tag}'! Use only letters, numbers, and hyphens."
    
    return True, ""


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

    def show_error(self, message):

        view = ModalView(size_hint=(0.8, 0.4), auto_dismiss=False)

        card = MDCard(
            orientation="vertical",
            padding=20,
            spacing=20,
            style="elevated",
            size_hint=(1, 1),
        )

        # Title (use role="large" instead of "headline")
        card.add_widget(
            MDLabel(
                text="Invalid Input",
                halign="center",
                role="large"
            )
        )

        # Main message (no role needed)
        card.add_widget(
            MDLabel(
                text=message,
                halign="center"
            )
        )

        # OK button
        ok_btn = MDButton(
            MDButtonText(text="OK"),
            style="elevated",
            pos_hint={"center_x": 0.5}
        )
        ok_btn.bind(on_release=view.dismiss)

        card.add_widget(ok_btn)

        view.add_widget(card)
        view.open()

    # --- Unified add + save ---
    def addTask(self):
        """
        Adds a task (both to the UI and saved JSON).
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

        # Do not add blank-header tasks
        if not header:
            print("No header detected.")
            return

        # ========== INPUT VALIDATION (CWE-20) ==========
        
        # Validate task title
        is_valid, error_msg = validate_task_title(header)
        if not is_valid:
            self.show_error(f"\n\n{error_msg}\n\n")
            return
        
        # Validate description
        is_valid, error_msg = validate_task_description(description)
        if not is_valid:
            self.show_error(f"\n\n{error_msg}\n\n")
            return
        
        # Validate due date
        is_valid, error_msg = validate_due_date(due_date)
        if not is_valid:
            self.show_error(f"\n\n{error_msg}\n\n")
            return

        # ========== END VALIDATION ==========

        # Build task dictionary and append
        task = {
            "header": header,
            "description": description,
            "due_date": due_date,
            "completed": False,      # <-- NEW field
        }
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

    # ---------- NEW: reordering logic ----------

    def move_task_up(self, index: int):
        """Move a task one position up (if possible)."""
        if index <= 0 or index >= len(self.task_list):
            return
        self.task_list[index - 1], self.task_list[index] = \
            self.task_list[index], self.task_list[index - 1]
        save_tasks(self.task_list)
        self.render_tasks()

    def move_task_down(self, index: int):
        """Move a task one position down (if possible)."""
        if index < 0 or index >= len(self.task_list) - 1:
            return
        self.task_list[index + 1], self.task_list[index] = \
            self.task_list[index], self.task_list[index + 1]
        save_tasks(self.task_list)
        self.render_tasks()

    # ---------- NEW: completion / checkbox logic ----------

    def toggle_task_complete(self, index: int, value: bool):
        """Mark a task as complete/incomplete and save."""
        if 0 <= index < len(self.task_list):
            self.task_list[index]["completed"] = bool(value)
            save_tasks(self.task_list)
            self.render_tasks()

    def _make_checkbox(self, index: int, completed: bool) -> MDCheckbox:
        cb = MDCheckbox(
            size_hint=(None, None),
            size=(dp(32), dp(32)),
            active=completed,
        )

        def on_active_cb(checkbox, value):
            self.toggle_task_complete(index, value)

        cb.bind(active=on_active_cb)
        return cb

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

    # ---------- move buttons ----------

    def _make_move_up_btn(self, index: int) -> MDIconButton:
        btn = MDIconButton(
            icon="chevron-up",
            size_hint=(None, None),
            size=(dp(36), dp(36)),
        )

        if index == 0:
            # First item can't move up
            btn.disabled = True
            btn.opacity = 0.3
        else:
            btn.bind(on_release=lambda w: self.move_task_up(index))
        return btn

    def _make_move_down_btn(self, index: int, total: int) -> MDIconButton:
        btn = MDIconButton(
            icon="chevron-down",
            size_hint=(None, None),
            size=(dp(36), dp(36)),
        )

        if index == total - 1:
            # Last item can't move down
            btn.disabled = True
            btn.opacity = 0.3
        else:
            btn.bind(on_release=lambda w: self.move_task_down(index))
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
            placeholder = MDLabel(
                text="No tasks yet",
                halign="center",
                size_hint_y=None,
                height=dp(40),
            )
            container.add_widget(placeholder)
            return

        # Build each row
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel

        total = len(self.task_list)

        for index, task in enumerate(self.task_list):
            completed = task.get("completed", False)

            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(50),
                padding=[dp(10), dp(5)],
                spacing=dp(10),
            )

            # Checkbox first
            row.add_widget(self._make_checkbox(index, completed))

            # header
            header_text = task.get("header", "")
            if completed:
                header_text = f"[s]{header_text}[/s]"
            header_label = MDLabel(
                text=header_text,
                size_hint_x=0.3,
                bold=True,
                valign="middle",
                markup=True,  # enable [s]...[/s]
            )
            row.add_widget(header_label)

            # description
            desc_text = task.get("description", "")
            if completed:
                desc_text = f"[s]{desc_text}[/s]"
            desc_label = MDLabel(
                text=desc_text,
                size_hint_x=0.5,
                valign="middle",
                markup=True,
            )
            row.add_widget(desc_label)

            # due date, right aligned (no strikethrough needed, but you can add it if you want)
            row.add_widget(
                MDLabel(
                    text=task.get("due_date", ""),
                    size_hint_x=0.2,
                    halign="right",
                    valign="middle",
                )
            )

            # move up / move down buttons
            row.add_widget(self._make_move_up_btn(index))
            row.add_widget(self._make_move_down_btn(index, total))

            # delete button
            row.add_widget(self._make_delete_btn(index))

            container.add_widget(row)