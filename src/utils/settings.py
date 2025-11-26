import json
import os

class GameSettings:
    """
    Global settings manager for the Airsoft Bomb system.
    Handles loading, saving, and accessing game configuration.
    """
    
    def __init__(self):
        self.settings_file = "bomb_settings.json"
        self.defaults = {
            "bomb_code": "7355608",
            "countdown_time": 45,
            "sound_enabled": True,
            "brightness": 100,
            "beep_enabled": True,
            "domination_target_time": 60,
            "hold_button_capture_speed": 0.2,
            "hold_button_decay_speed": 0.05,
            "hacking_rounds": 3,
            "hacking_max_attempts": 5
        }
        self.current = self.defaults.copy()
        self.load()
    
    def load(self):
        """Load settings from file, or use defaults if file doesn't exist"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    self.current.update(loaded)
                print(f"[SETTINGS] Loaded from {self.settings_file}")
            except Exception as e:
                print(f"[SETTINGS] Error loading: {e}, using defaults")
        else:
            print("[SETTINGS] No settings file found, using defaults")
    
    def save(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.current, f, indent=2)
            print(f"[SETTINGS] Saved to {self.settings_file}")
            return True
        except Exception as e:
            print(f"[SETTINGS] Error saving: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.current = self.defaults.copy()
        self.save()
        print("[SETTINGS] Reset to defaults")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.current.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.current[key] = value
    
    def get_all(self):
        """Get all current settings"""
        return self.current.copy()

# Global settings instance
_settings_instance = None

def get_settings():
    """Get the global settings instance"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = GameSettings()
    return _settings_instance
