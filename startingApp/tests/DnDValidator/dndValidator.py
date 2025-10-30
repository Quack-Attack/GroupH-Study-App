

class Settings:
    """
    Represents the app's settings related to Do Not Disturb (DND) behavior.
    """
    def __init__(self, allow_auto_dnd: bool):
        self.allow_auto_dnd = allow_auto_dnd


class DNDManager:
    """
    Manages whether DND can be turned on or off depending on the user's settings.
    """
    def __init__(self, settings: Settings, feature_in_use: bool = False):
        self.settings = settings
        self.feature_in_use = feature_in_use
        self.dnd_on = False

    def can_enable_dnd(self):
        """
        Determines if DND can be enabled given current settings and feature usage.
        """
        # if the feature is active but auto DND is not allowed, DND cannot be turned on automatically
        if self.feature_in_use and not self.settings.allow_auto_dnd:
            return False
        return True

    def enable_dnd(self):
        """
        Attempts to turn on DND.
        Returns True if successful, False if blocked by settings.
        """
        if self.can_enable_dnd():
            self.dnd_on = True
            return True
        else:
            self.dnd_on = False
            return False

