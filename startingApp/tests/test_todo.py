"""
Unit tests for ToDoScreen features
Tests the expandable input functionality and task creation with header, description, and due date
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import from screens
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.metrics import dp
from kivymd.app import MDApp


class TestApp(MDApp):
    """Minimal test app for KivyMD initialization"""
    def build(self):
        pass


class TestToDoScreen(unittest.TestCase):
    """Test suite for ToDoScreen functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize KivyMD app once for all tests"""
        cls.app = TestApp()
        cls.app.theme_cls.primary_palette = "Blue"
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Import after app is created
        from screens.todo import ToDoScreen
        
        # Create screen instance
        self.screen = ToDoScreen()
        
        # Create a dict for ids
        mock_ids = {}
        
        mock_ids['input_box'] = Mock()
        mock_ids['input_box'].height = dp(60)
        
        mock_ids['new_task_input'] = Mock()
        mock_ids['new_task_input'].text = ""
        mock_ids['new_task_input'].opacity = 1
        mock_ids['new_task_input'].disabled = False
        
        mock_ids['task_header_input'] = Mock()
        mock_ids['task_header_input'].text = ""
        mock_ids['task_header_input'].opacity = 0
        
        mock_ids['task_description_input'] = Mock()
        mock_ids['task_description_input'].text = ""
        mock_ids['task_description_input'].opacity = 0
        
        mock_ids['task_date_input'] = Mock()
        mock_ids['task_date_input'].text = ""
        mock_ids['task_date_input'].opacity = 0
        
        mock_ids['todo_items_container'] = Mock()
        mock_ids['todo_items_container'].add_widget = Mock()
        
        # Assign the mock_ids dict
        self.screen.ids = mock_ids
    
    @patch('screens.todo.Animation')
    def test_expand_input_shows_detail_fields(self, mock_animation):
        """Test that expand_input() shows the header, description, and date fields"""
        # Call expand_input
        self.screen.expand_input()
        
        # Assert all detail fields are visible
        self.assertEqual(self.screen.ids['task_header_input'].opacity, 1)
        self.assertEqual(self.screen.ids['task_description_input'].opacity, 1)
        self.assertEqual(self.screen.ids['task_date_input'].opacity, 1)
    
    @patch('kivymd.uix.boxlayout.MDBoxLayout', return_value=Mock(add_widget=Mock()))
    @patch('kivymd.uix.label.MDLabel', return_value=Mock())
    @patch('screens.todo.ToDoScreen.collapse_input')
    def test_addTask_with_valid_header(self, mock_collapse, mock_label, mock_box):
        """Test that addTask() creates a task when header is provided"""
        # Set up input values
        self.screen.ids['task_header_input'].text = "Complete Project"
        self.screen.ids['task_description_input'].text = "Finish the study app"
        self.screen.ids['task_date_input'].text = "12/31/2025"
        
        # Call addTask
        self.screen.addTask()
        
        # Assert a widget was added to the container
        self.screen.ids['todo_items_container'].add_widget.assert_called_once()
    
    @patch('kivymd.uix.boxlayout.MDBoxLayout', return_value=Mock(add_widget=Mock()))
    @patch('kivymd.uix.label.MDLabel', return_value=Mock())
    def test_addTask_with_whitespace_only_header(self, mock_label, mock_box):
        """Test that addTask() does not add a task when header is only whitespace"""
        # Set up whitespace-only header
        self.screen.ids['task_header_input'].text = "   "
        self.screen.ids['task_description_input'].text = "Description"
        self.screen.ids['task_date_input'].text = "12/31/2025"
        
        # Call addTask
        self.screen.addTask()
        
        # Assert no widget was added
        self.screen.ids['todo_items_container'].add_widget.assert_not_called()
    
    @patch('kivymd.uix.boxlayout.MDBoxLayout', return_value=Mock(add_widget=Mock()))
    @patch('kivymd.uix.label.MDLabel', return_value=Mock())
    @patch('screens.todo.ToDoScreen.collapse_input')
    def test_addTask_with_header_only(self, mock_collapse, mock_label, mock_box):
        """Test that addTask() works with only header filled (description and date can be optional)"""
        # Set up only header
        self.screen.ids['task_header_input'].text = "Important Task"
        self.screen.ids['task_description_input'].text = ""
        self.screen.ids['task_date_input'].text = ""
        
        # Call addTask
        self.screen.addTask()
        
        # Assert a widget was added
        self.screen.ids['todo_items_container'].add_widget.assert_called_once()
    
    @patch('kivymd.uix.boxlayout.MDBoxLayout', return_value=Mock(add_widget=Mock()))
    @patch('kivymd.uix.label.MDLabel')
    @patch('screens.todo.ToDoScreen.collapse_input')
    def test_addTask_label_content(self, mock_collapse, mock_label, mock_box):
        """Test that addTask() creates labels with correct text content"""
        # Set up input values
        header_text = "MATH Chapter 6"
        desc_text = "Homework problems 6-10"
        date_text = "11/15/2025"
        
        self.screen.ids['task_header_input'].text = header_text
        self.screen.ids['task_description_input'].text = desc_text
        self.screen.ids['task_date_input'].text = date_text
        
        # Store the label creation calls
        label_calls = []
        def capture_label_call(**kwargs):
            label_calls.append(kwargs)
            return Mock()
        
        mock_label.side_effect = capture_label_call
        
        # Call addTask
        self.screen.addTask()
        
        # Assert labels were created with correct text
        self.assertEqual(len(label_calls), 3)
        self.assertEqual(label_calls[0]['text'], header_text)
        self.assertEqual(label_calls[1]['text'], desc_text)
        self.assertEqual(label_calls[2]['text'], date_text)


class TestToDoScreenIntegration(unittest.TestCase):
    """Integration tests for ToDoScreen workflow"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize KivyMD app once for all tests"""
        cls.app = TestApp()
        cls.app.theme_cls.primary_palette = "Blue"
    
    def setUp(self):
        """Set up test fixtures"""
        from screens.todo import ToDoScreen
        self.screen = ToDoScreen()
        
        # Create a dict for ids
        mock_ids = {}
        
        mock_ids['input_box'] = Mock()
        mock_ids['input_box'].height = dp(60)
        
        mock_ids['new_task_input'] = Mock()
        mock_ids['new_task_input'].text = ""
        mock_ids['new_task_input'].opacity = 1
        mock_ids['new_task_input'].disabled = False
        
        mock_ids['task_header_input'] = Mock()
        mock_ids['task_header_input'].text = ""
        mock_ids['task_header_input'].opacity = 0
        
        mock_ids['task_description_input'] = Mock()
        mock_ids['task_description_input'].text = ""
        mock_ids['task_description_input'].opacity = 0
        
        mock_ids['task_date_input'] = Mock()
        mock_ids['task_date_input'].text = ""
        mock_ids['task_date_input'].opacity = 0
        
        mock_ids['todo_items_container'] = Mock()
        mock_ids['todo_items_container'].add_widget = Mock()
        
        # Assign the mock_ids dict
        self.screen.ids = mock_ids
    
    @patch('kivymd.uix.boxlayout.MDBoxLayout', return_value=Mock(add_widget=Mock()))
    @patch('kivymd.uix.label.MDLabel', return_value=Mock())
    @patch('screens.todo.Animation')
    def test_multiple_tasks_workflow(self, mock_animation, mock_label, mock_box):
        """Test adding multiple tasks in sequence"""
        tasks = [
            ("Task 1", "Description 1", "01/01/2026"),
            ("Task 2", "Description 2", "01/02/2026"),
            ("Task 3", "Description 3", "01/03/2026")
        ]
        
        for header, desc, date in tasks:
            # Expand
            self.screen.expand_input()
            
            # Fill
            self.screen.ids['task_header_input'].text = header
            self.screen.ids['task_description_input'].text = desc
            self.screen.ids['task_date_input'].text = date
            
            # Add
            self.screen.addTask()
        
        # Verify all tasks were added
        self.assertEqual(self.screen.ids['todo_items_container'].add_widget.call_count, 3)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)