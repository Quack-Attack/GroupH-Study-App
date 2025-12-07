from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from openai import OpenAI

KV = """
<AIWordScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Enter a word:"
            halign: "center"
            font_style: "H5"

        MDTextField:
            id: word_input
            hint_text: "Type one word"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}

        MDRectangleFlatButton:
            text: "Get Definition"
            pos_hint: {"center_x": 0.5}
            on_release: root.get_definition()
"""

class AIWordScreen(Screen):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize OpenAI client
        self.client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")  # Replace with your key

    def get_definition(self):
        word = self.ids.word_input.text.strip()
        if not word:
            self.show_dialog("Please enter a word!")
            return

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a helpful dictionary assistant."},
                    {"role": "user", "content": f"Define the word '{word}' in one clear sentence."}
                ]
            )
            definition = response.choices[0].message.content
        except Exception as e:
            definition = f"Error: {str(e)}"

        self.show_dialog(definition)

    def show_dialog(self, text):
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="Definition",
            text=text,
            size_hint=(0.8, None),
            height=200,
            buttons=[
                MDRectangleFlatButton(
                    text="Close",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

# Load the KV string
from kivy.lang import Builder
Builder.load_string(KV)
