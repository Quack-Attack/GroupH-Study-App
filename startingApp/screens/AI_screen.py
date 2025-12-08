from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivy.metrics import dp
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

KV = """
<AIWordScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20), dp(20), dp(20), dp(80)
        spacing: dp(20)

        MDLabel:
            text: "AI Word Helper"
            halign: "center"
            font_size: "28sp"
            size_hint_y: None
            height: dp(50)

        MDLabel:
            text: "Enter a word to get its definition:"
            halign: "center"
            font_size: "18sp"
            size_hint_y: None
            height: dp(40)

        MDTextField:
            id: word_input
            fill_color: 0, 0, 0, 0
            mode: "outlined"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
            
            MDTextFieldHintText:
                text: "Type a word here"

        MDButton:
            style: "elevated"
            size_hint: None, None
            width: dp(200)
            height: dp(50)
            pos_hint: {"center_x": 0.5}
            on_release: root.get_definition()
            
            MDButtonText:
                text: "Get Definition"
        
        Widget:
"""

class AIWordScreen(MDScreen):
    dialog = None
    current_word = ""
    current_definition = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize OpenAI client with API key from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("WARNING: OPENAI_API_KEY not found in environment variables!")
        self.client = OpenAI(api_key=api_key)

    def get_definition(self):
        word = self.ids.word_input.text.strip()
        
        if not word:
            self.show_dialog("Error", "Please enter a word!")
            return

        # Show loading message
        self.show_dialog("Loading", "Getting definition...")

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful dictionary assistant."},
                    {"role": "user", "content": f"Define the word '{word}' in one clear sentence."}
                ]
            )
            definition = response.choices[0].message.content
            
            # Store the word and definition
            self.current_word = word
            self.current_definition = definition
            
            self.show_dialog(f"Definition of '{word}'", definition, show_add_button=True)
        except Exception as e:
            self.show_dialog("Error", f"Could not get definition: {str(e)}")

    def show_dialog(self, title, text, show_add_button=False):
        """Show dialog using KivyMD 2.0 API"""
        if self.dialog:
            try:
                self.dialog.dismiss()
            except Exception:
                pass
        
        # Headline (title)
        headline = MDDialogHeadlineText(text=title, halign="left")
        
        # Content container with the message
        content = MDDialogContentContainer(
            orientation="vertical",
            spacing="10dp",
            padding="12dp"
        )
        
        # Add label with the definition text
        message_label = MDLabel(
            text=text,
            adaptive_height=True,
            padding=(dp(10), dp(10))
        )
        content.add_widget(message_label)
        
        # Button container
        btn_container = MDDialogButtonContainer(
            Widget(),  # Spacer to align buttons to the right
            spacing="8dp"
        )
        
        # Add "Add to Flash Cards" button if this is a definition dialog
        if show_add_button:
            add_flashcard_btn = MDButton(
                MDButtonText(text="ADD TO FLASH CARDS"),
                style="filled",
                on_release=self._add_to_flashcards
            )
            btn_container.add_widget(add_flashcard_btn)
        
        # Always add close button
        close_btn = MDButton(
            MDButtonText(text="CLOSE"),
            style="text",
            on_release=self._close_dialog
        )
        btn_container.add_widget(close_btn)
        
        # Build dialog with positional children
        self.dialog = MDDialog(
            headline,
            content,
            btn_container,
            scrim_color=(0, 0, 0, 0.5)
        )
        self.dialog.open()

    def _close_dialog(self, *args):
        """Close the dialog"""
        if self.dialog:
            try:
                self.dialog.dismiss()
            except Exception:
                pass

    def _add_to_flashcards(self, *args):
        """Add the current word and definition to the flashcards"""
        from kivy.app import App
        
        # Get the flashcards screen
        app = App.get_running_app()
        flashcards_screen = None
        
        # Try to get it from the screen manager
        try:
            screen_manager = app.root.ids.screen_manager_root
            flashcards_screen = screen_manager.get_screen('flashCards')
        except Exception as e:
            print(f"Error getting flashcards screen: {e}")
            self.show_dialog("Error", "Could not access flashcards. Please try again.")
            return
        
        # Add the card (front = word, back = definition)
        if flashcards_screen and self.current_word and self.current_definition:
            flashcards_screen.cards.append({
                "front": self.current_word,
                "back": self.current_definition
            })
            
            # If this is the first card, set the index
            if len(flashcards_screen.cards) == 1:
                flashcards_screen.current_index = 0
                flashcards_screen.showing_back = False
            
            # Update the display
            flashcards_screen._update_current_text()
            
            # Close the dialog and show success message
            self._close_dialog()
            self.show_dialog("Success", f"'{self.current_word}' has been added to your flashcards!")
        else:
            self.show_dialog("Error", "Could not add to flashcards. Please try again.")

# Load the KV string
Builder.load_string(KV)