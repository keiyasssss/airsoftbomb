"""
Sound manager for the Airsoft Bomb system.
Currently mocked - will play actual sounds when deployed to RPi.
"""

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        
    def load_sound(self, name, filepath):
        """Load a sound file (mocked for now)"""
        print(f"[SOUND] Loading {name} from {filepath}")
        self.sounds[name] = filepath
        
    def play(self, name):
        """Play a sound (mocked for now)"""
        if self.enabled and name in self.sounds:
            print(f"[SOUND] Playing {name}")
            
    def stop(self, name):
        """Stop a sound (mocked for now)"""
        if name in self.sounds:
            print(f"[SOUND] Stopping {name}")
            
    def set_enabled(self, enabled):
        """Enable or disable sounds"""
        self.enabled = enabled
        print(f"[SOUND] Sound {'enabled' if enabled else 'disabled'}")
