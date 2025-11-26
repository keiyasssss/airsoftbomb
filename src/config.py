import pygame

# Screen Configuration
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FPS = 60

# Colors (Military/Terminal Palette)
BLACK = (10, 10, 10)          # Deep black
MILITARY_GREEN = (50, 205, 50) # Standard terminal green
DARK_GREEN = (20, 80, 20)     # Dimmed green for backgrounds/borders
ALERT_RED = (220, 20, 60)     # For errors or critical alerts
AMBER = (255, 191, 0)         # Warning/Secondary text
WHITE = (240, 240, 240)       # High contrast white
GRAY = (100, 100, 100)        # Disabled/Inactive

# Fonts
FONT_MAIN = None # Default system font for now, can load custom TTF later
FONT_SIZE_HEADER = 40
FONT_SIZE_NORMAL = 24
FONT_SIZE_SMALL = 18

# Hardware Configuration
PIN_BUTTON_UP = 17
PIN_BUTTON_DOWN = 27
PIN_BUTTON_SELECT = 22
PIN_BUTTON_BACK = 23
