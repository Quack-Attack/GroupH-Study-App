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
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp


class FlashCardsScreen(MDScreen):
    cards = ListProperty([])
    current_index = NumericProperty(0)
    showing_back = BooleanProperty(False)
    current_text = StringProperty("No cards yet. Add one!")
    view_mode = StringProperty("single")  # "single" or "grid"

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
    # View Mode Toggle
    # ----------------------------
    def toggle_view_mode(self):
        """Toggle between single card and grid view"""
        if self.view_mode == "single":
            self.view_mode = "grid"
            self._show_grid_view()
        else:
            self.view_mode = "single"
            self._show_single_view()

    def _show_single_view(self):
        """Show single card view, hide grid"""
        try:
            single_container = self.ids.get('single_card_container')
            grid_container = self.ids.get('grid_view_container')
            left_arrow = self.ids.get('single_card_container_left_arrow')
            right_arrow = self.ids.get('single_card_container_right_arrow')
            view_btn = self.ids.get('view_toggle_btn')
            
            if single_container:
                single_container.opacity = 1
                single_container.disabled = False
            
            if left_arrow:
                left_arrow.opacity = 1
                left_arrow.disabled = False
            
            if right_arrow:
                right_arrow.opacity = 1
                right_arrow.disabled = False
            
            if grid_container:
                grid_container.opacity = 0
                grid_container.disabled = True
                grid_container.size_hint_y = None
                grid_container.height = 0
            
            if view_btn:
                for child in view_btn.children:
                    if isinstance(child, MDButtonText):
                        child.text = "View All Cards"
            
            self._update_current_text()
        except Exception as e:
            print(f"Error showing single view: {e}")

    def _show_grid_view(self):
        """Show grid view, hide single card"""
        try:
            single_container = self.ids.get('single_card_container')
            grid_container = self.ids.get('grid_view_container')
            grid_scroll = self.ids.get('grid_scroll_view')
            left_arrow = self.ids.get('single_card_container_left_arrow')
            right_arrow = self.ids.get('single_card_container_right_arrow')
            view_btn = self.ids.get('view_toggle_btn')
            
            # Hide single view
            if single_container:
                single_container.opacity = 0
                single_container.disabled = True
            
            # Hide arrows
            if left_arrow:
                left_arrow.opacity = 0
                left_arrow.disabled = True
            
            if right_arrow:
                right_arrow.opacity = 0
                right_arrow.disabled = True
            
            # Show grid view
            if grid_container:
                grid_container.opacity = 1
                grid_container.disabled = False
                grid_container.size_hint_y = 1
                grid_container.height = dp(0)  # ignored when size_hint_y=1
            
            # Update button text
            if view_btn:
                for child in view_btn.children:
                    if isinstance(child, MDButtonText):
                        child.text = "Back to Card"
            
            # Build the grid
            if grid_scroll:
                self._build_grid(grid_scroll)
            else:
                print("grid_scroll_view not found!")
                
        except Exception as e:
            print(f"Error showing grid view: {e}")

    def _build_grid(self, scroll_view):
        """Build the grid of cards"""
        # Clear existing content
        scroll_view.clear_widgets()
        
        if not self.cards:
            # Show "no cards" message
            no_cards = MDLabel(
                text="No flashcards yet. Add some to get started!",
                halign="center",
                valign="middle",
            )
            scroll_view.add_widget(no_cards)
            return
        
        # Create grid layout
        grid = GridLayout(
            cols=2,
            spacing=dp(15),
            padding=dp(15),
            size_hint_y=None,
        )
        grid.bind(minimum_height=grid.setter('height'))
        
        # Add each card to grid
        for index, card in enumerate(self.cards):
            card_widget = self._create_card_preview(card, index)
            grid.add_widget(card_widget)
        
        scroll_view.add_widget(grid)

    def _create_card_preview(self, card, index):
        """Create a clickable preview card for the grid"""
        # Get card text (front side)
        front_text = card.get("front", "")
        
        # Truncate if too long
        if len(front_text) > 60:
            display_text = front_text[:60] + "..."
        else:
            display_text = front_text
        
        # Create card widget
        card_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(120),
        )
        
        card_widget = MDCard(
            orientation="vertical",
            padding=dp(15),
            size_hint_y=None,
            height=dp(120),
            ripple_behavior=True,
            style="elevated",
        )
        
        # Card number
        number_label = MDLabel(
            text=f"Card {index + 1}",
            size_hint_y=None,
            height=dp(20),
            font_size="12sp",
            theme_text_color="Secondary",
        )
        
        # Card content
        content_label = MDLabel(
            text=display_text,
            halign="center",
            valign="middle",
            font_size="14sp",
        )
        
        card_widget.add_widget(number_label)
        card_widget.add_widget(content_label)
        
        # Make clickable
        card_widget.bind(on_release=lambda x: self._jump_to_card(index))
        
        card_box.add_widget(card_widget)
        return card_box

    def _jump_to_card(self, index):
        """Jump to specific card and return to single view"""
        self.current_index = index
        self.showing_back = False
        self.view_mode = "single"
        self._show_single_view()

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