# test_settings.py

import unittest
from dndValidator import Settings, DNDManager

class TestDNDManager(unittest.TestCase):

    def test_dnd_blocked_when_auto_not_allowed_and_feature_in_use(self):
        """DND should NOT turn on when feature is in use and auto DND is disallowed."""
        settings = Settings(allow_auto_dnd=False)
        manager = DNDManager(settings=settings, feature_in_use=True)
        result = manager.enable_dnd()

        self.assertFalse(result, "DND should not be enabled")
        self.assertFalse(manager.dnd_on, "DND flag should remain False")
        
        
        print("\nTest 1 ensures the devce's Do Not Disturb is not turned on by the feature.\n Test 1 fails successfully ✅")

    def test_dnd_allowed_when_auto_allowed_even_with_feature_in_use(self):
        """DND should turn on when auto DND is allowed, even if feature is active."""
        settings = Settings(allow_auto_dnd=True)
        manager = DNDManager(settings=settings, feature_in_use=True)
        result = manager.enable_dnd()

        self.assertTrue(result, "DND should be enabled")
        self.assertTrue(manager.dnd_on, "DND flag should be True")
        
        print("\nTest 2 ensures that Do Not Disturb works when the feature is active.\n Test 2 failed successfully ✅")

    def test_dnd_allowed_when_feature_not_in_use(self):
        """DND should always be allowed when feature is not in use."""
        settings = Settings(allow_auto_dnd=False)
        manager = DNDManager(settings=settings, feature_in_use=False)
        result = manager.enable_dnd()

        self.assertTrue(result, "DND should be enabled when feature is inactive")
        self.assertTrue(manager.dnd_on, "DND flag should be True")

        print("\nTest 3 ensures that Do Not Disturb turns off when the feature is inactive.\n Test 3 failed successfully ✅")

if __name__ == '__main__':
    unittest.main()
