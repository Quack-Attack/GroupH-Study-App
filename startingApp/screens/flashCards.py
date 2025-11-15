from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

# KivyMD imports
try:
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.button import MDFlatButton
    from kivymd.uix.textfield import MDTextField
    from kivymd.uix.label import MDLabel
except Exception:
    # If KivyMD not available for any reason, fall back to plain Kivy widgets.
    MDDialog = None
    MDFlatButton = None
    MDTextField = None
    from kivy.uix.label import Label as MDLabel  # fallback to plain label

class _AddCardContent(BoxLayout):
    """Small helper class used as the MDDialog content_cls.
    This has two MDTextField children accessible as front_field/back_field.
    """
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=8, **kwargs)
        # Use MDTextField if available, otherwise Kivy TextInput
        if MDTextField is not None:
            self.front_field = MDTextField(hint_text="Front (question)", required=False)
            self.back_field = MDTextField(hint_text="Back (answer)", required=False)
        else:
            from kivy.uix.textinput import TextInput
            self.front_field = TextInput(hint_text="Front (question)", multiline=False)
            self.back_field = TextInput(hint_text="Back (answer)", multiline=False)
        self.add_widget(self.front_field)
        self.add_widget(self.back_field)

class FlashCardsScreen(Screen):
    cards = ListProperty([])

    def on_pre_enter(self, *args):
        """Populate RV and register this screen on the App for easy access from KV."""
        # register self on the running app so KV can call app.flashcards_screen
        try:
            App.get_running_app().flashcards_screen = self
        except Exception:
            pass

        rv = self.ids.get("rv")
        if rv is not None:
            rv.data = [{"front": c.get("front", ""), "back": c.get("back", "")} for c in self.cards]

    # -------------------------
    # Add-card dialog workflow
    # -------------------------
    def open_add_dialog(self):
        """Open a material dialog to add a new flashcard."""
        # If MDDialog is available, create the content_cls; otherwise fallback to a simple dialog
        self._add_content = _AddCardContent()
        # Buttons: Cancel and Confirm
        if MDFlatButton is not None and MDDialog is not None:
            cancel_btn = MDFlatButton(text="CANCEL", on_release=self._on_add_cancel)
            confirm_btn = MDFlatButton(text="CONFIRM", on_release=self._on_add_confirm)
            self._add_dialog = MDDialog(
                title="Add Flashcard",
                type="custom",
                content_cls=self._add_content,
                buttons=[cancel_btn, confirm_btn],
                auto_dismiss=False,
            )
            self._add_dialog.open()
        else:
            # Fallback: use a plain popup-like MDDialog substitute if possible; emulate behavior
            from kivy.uix.popup import Popup
            from kivy.uix.button import Button
            content = BoxLayout(orientation="vertical", spacing=10, padding=10)
            content.add_widget(self._add_content)
            btn_row = BoxLayout(size_hint_y=None, height=40, spacing=8)
            btn_cancel = Button(text="Cancel")
            btn_confirm = Button(text="Confirm")
            btn_cancel.bind(on_release=lambda *_: self._on_add_cancel())
            btn_confirm.bind(on_release=lambda *_: self._on_add_confirm())
            btn_row.add_widget(btn_cancel)
            btn_row.add_widget(btn_confirm)
            content.add_widget(btn_row)
            self._add_dialog = Popup(title="Add Flashcard", content=content, size_hint=(0.9, None), height=320, auto_dismiss=False)
            self._add_dialog.open()

    def _on_add_cancel(self, *args):
        """Cancel handler for add-dialog."""
        if getattr(self, "_add_dialog", None) is not None:
            try:
                self._add_dialog.dismiss()
            except Exception:
                pass
        # clear fields for next time
        if getattr(self, "_add_content", None) is not None:
            try:
                self._add_content.front_field.text = ""
                self._add_content.back_field.text = ""
            except Exception:
                pass

    def _on_add_confirm(self, *args):
        """Confirm handler: validate and add card."""
        front = ""
        back = ""
        if getattr(self, "_add_content", None) is not None:
            front = (getattr(self._add_content.front_field, "text", "") or "").strip()
            back = (getattr(self._add_content.back_field, "text", "") or "").strip()

        if not front:
            # focus front field so user fills it
            try:
                self._add_content.front_field.focus = True
            except Exception:
                pass
            return

        # append to cards and update rv immediately
        self.cards.append({"front": front, "back": back})
        rv = self.ids.get("rv")
        if rv is not None:
            rv.data.append({"front": front, "back": back})

        # dismiss dialog & clear fields
        if getattr(self, "_add_dialog", None) is not None:
            try:
                self._add_dialog.dismiss()
            except Exception:
                pass
        if getattr(self, "_add_content", None) is not None:
            try:
                self._add_content.front_field.text = ""
                self._add_content.back_field.text = ""
            except Exception:
                pass

    # -------------------------
    # Show back popup (flip)
    # -------------------------
    def show_back_dialog(self, front, back):
        """Show the back of a flashcard using an MDDialog (or fallback)."""
        front_text = str(front) if front is not None else "Flashcard"
        back_text = (str(back).strip() if back is not None else "") or "(no back text)"

        if MDDialog is not None:
            # a simple dialog with a single close button
            close_btn = MDFlatButton(text="CLOSE", on_release=lambda *_: self._back_dialog.dismiss())
            # content_cls expects a widget; use a BoxLayout with MDLabel
            content = BoxLayout(orientation="vertical", padding=12)
            content.add_widget(MDLabel(text=back_text))
            self._back_dialog = MDDialog(title=front_text, type="custom", content_cls=content, buttons=[close_btn], auto_dismiss=False)
            self._back_dialog.open()
        else:
            # fallback to Popup
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            content = BoxLayout(orientation="vertical", padding=12, spacing=10)
            content.add_widget(Label(text=back_text))
            close_btn = Button(text="Close", size_hint_y=None, height=40)
            content.add_widget(close_btn)
            dlg = Popup(title=front_text, content=content, size_hint=(0.8, 0.45), auto_dismiss=False)
            close_btn.bind(on_release=lambda *_: dlg.dismiss())
            dlg.open()