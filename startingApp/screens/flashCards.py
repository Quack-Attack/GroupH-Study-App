from kivymd.uix.screen import MDScreen
from kivy.properties import ListProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.widget import MDWidget
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel


class FlashCardsScreen(MDScreen):
    cards = ListProperty([])
    current_index = NumericProperty(0)
    showing_back = BooleanProperty(False)
    current_text = StringProperty("No cards yet. Add one!")

    # ----------------------------
    # Screen Lifecycle
    # ----------------------------
    def on_pre_enter(self, *args):
        App.get_running_app().flashcards_screen = self

        if self.current_index >= len(self.cards):
            self.current_index = max(0, len(self.cards) - 1)

        self.showing_back = False
        self._update_current_text()

    # ----------------------------
    # Card Updating
    # ----------------------------
    def _update_current_text(self):
        if not self.cards:
            self.current_text = "No cards yet. Use + to add a flashcard."
            return

        idx = max(0, min(self.current_index, len(self.cards) - 1))
        card = self.cards[idx]

        if self.showing_back:
            text = card.get("back") or "(no back text)"
        else:
            text = card.get("front") or "(no front text)"

        self.current_text = text

    def flip_card(self):
        if not self.cards:
            return
        self.showing_back = not self.showing_back
        self._update_current_text()

    def next_card(self):
        if not self.cards:
            return
        self.current_index = (self.current_index + 1) % len(self.cards)
        self.showing_back = False
        self._update_current_text()

    def prev_card(self):
        if not self.cards:
            return
        self.current_index = (self.current_index - 1) % len(self.cards)
        self.showing_back = False
        self._update_current_text()

    def on_cards(self, *args):
        if self.current_index >= len(self.cards):
            self.current_index = max(0, len(self.cards) - 1)
        self.showing_back = False
        self._update_current_text()

    # ----------------------------
    # Add Flashcard Dialog
    # ----------------------------
    def open_add_dialog(self):
        """
        Build MDDialog using the 1.2.x API break format:
        MDDialog(
            MDDialogHeadlineText(...),
            MDDialogContentContainer(...),
            MDDialogButtonContainer(...),
        )
        """
        # Content container for text fields
        content = MDDialogContentContainer(orientation="vertical", spacing="10dp", padding="12dp")

        # Create fields and add to content
        self.front_field = MDTextField(hint_text="Front (question)", size_hint_y=None, height="48dp")
        self.back_field = MDTextField(hint_text="Back (answer)", size_hint_y=None, height="48dp")
        content.add_widget(self.front_field)
        content.add_widget(self.back_field)

        # Buttons: use a Widget() spacer so buttons align to the right (as shown in docs)
        btn_container = MDDialogButtonContainer(
            Widget(),
            MDButton(MDButtonText(text="CANCEL"), style="text", on_release=self._close_dialog),
            MDButton(MDButtonText(text="ADD"), style="filled", on_release=self._confirm_add),
            spacing="8dp",
        )

        # Headline (title)
        headline = MDDialogHeadlineText(text="Add Flashcard", halign="left")

        # Build dialog (positional children)
        self._add_dialog = MDDialog(headline, content, btn_container, scrim_color=(0, 0, 0, 0.5))
        self._add_dialog.open()


    def _close_dialog(self, *args):
        """Close the dialog (callback receives the button instance)."""
        if getattr(self, "_add_dialog", None):
            try:
                self._add_dialog.dismiss()
            except Exception:
                pass


    def _confirm_add(self, *args):
        """
        Callback for ADD button. Accepts the event arg(s) that Kivy passes.
        Validates and appends the card, then closes the dialog.
        """
        front = (getattr(self, "front_field", None).text or "").strip()
        back = (getattr(self, "back_field", None).text or "").strip()

        if not front:
            # mark error on the field (MDTextField has .error property)
            try:
                self.front_field.error = True
            except Exception:
                pass
            return

        # add card
        self.cards.append({"front": front, "back": back})

        if len(self.cards) == 1:
            self.current_index = 0
            self.showing_back = False

        # update display and close dialog
        self._update_current_text()
        try:
            if getattr(self, "_add_dialog", None):
                self._add_dialog.dismiss()
        except Exception:
            pass
