# screens/flashCards.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class FlashCardsScreen(Screen):
    cards = ListProperty([])   # safe default

    def on_pre_enter(self, *args):
        # Called right before the screen is shown
        # Populate the RecycleView data safely here (so KV parsing didn't need root.cards)
        rv = self.ids.get('rv')
        if rv is not None:
            rv.data = [{'front': c.get('front', ''), 'back': c.get('back', '')} for c in self.cards]

    def open_add_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.front_input = TextInput(hint_text='Front', multiline=False, size_hint_y=None, height=40)
        self.back_input = TextInput(hint_text='Back', multiline=False, size_hint_y=None, height=40)
        btn_row = BoxLayout(size_hint_y=None, height=40, spacing=10)
        confirm = Button(text='Confirm')
        cancel = Button(text='Cancel')
        btn_row.add_widget(confirm)
        btn_row.add_widget(cancel)

        content.add_widget(Label(text='Add Flashcard'))
        content.add_widget(self.front_input)
        content.add_widget(self.back_input)
        content.add_widget(btn_row)

        self._popup = Popup(title='Add Flashcard', content=content, size_hint=(0.9, None), height=300, auto_dismiss=False)
        confirm.bind(on_release=lambda *_: self.confirm_add())
        cancel.bind(on_release=lambda *_: self.cancel_add())
        self._popup.open()

    def confirm_add(self):
        front = (self.front_input.text or '').strip()
        back = (self.back_input.text or '').strip()
        if not front:
            self.front_input.focus = True
            return
        self.cards.append({'front': front, 'back': back})
        # Update RV immediately (if visible)
        rv = self.ids.get('rv')
        if rv is not None:
            rv.data.append({'front': front, 'back': back})
        self._popup.dismiss()
        self.front_input.text = ''
        self.back_input.text = ''

    def cancel_add(self):
        if hasattr(self, '_popup'):
            self._popup.dismiss()

    def show_back_popup(self, front, back):
        """
        Safely show the back of a flashcard in a popup.
        This method lives on the FlashCardsScreen class so KV can call it via the ScreenManager.
        """
        try:
            front_text = str(front) if front is not None else "Flashcard"
        except Exception:
            front_text = "Flashcard"
        try:
            back_text = str(back).strip() if back is not None else ""
        except Exception:
            back_text = ""

        if not back_text:
            back_text = "(no back text)"

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=back_text))
        close_btn = Button(text='Close', size_hint_y=None, height=40)
        content.add_widget(close_btn)

        popup = Popup(title=front_text, content=content, size_hint=(0.8, 0.45), auto_dismiss=False)
        close_btn.bind(on_release=lambda *_: popup.dismiss())
        popup.open()