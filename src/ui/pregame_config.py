import pygame
from src import config
from src.ui.base import BaseView

class PreGameConfigView(BaseView):
    """
    Pre-game configuration screen shown before starting a game mode.
    Displays current settings and allows starting the game.
    """
    def __init__(self, manager, mode_name, mode_class, settings_keys):
        super().__init__(manager)
        self.mode_name = mode_name
        self.mode_class = mode_class
        self.settings_keys = settings_keys  # List of setting keys relevant to this mode
        
        from src.utils.settings import get_settings
        self.settings = get_settings()
        
    def handle_input(self, action):
        if action == 'SELECT' or action == '5':
            # Start the game
            self.manager.set_view(self.mode_class)
        elif action == 'BACK':
            from src.ui.menu import MainMenuView
            self.manager.set_view(MainMenuView)
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text(self.mode_name, self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        # Current settings
        self.draw_text("CURRENT SETTINGS:", self.font_normal, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 80, center=True)
        
        start_y = 120
        line_spacing = 25
        
        for i, key in enumerate(self.settings_keys):
            value = self.settings.get(key)
            # Format the key name nicely
            display_name = key.replace('_', ' ').title()
            
            # Format the value
            if isinstance(value, bool):
                display_value = "ON" if value else "OFF"
            elif key.endswith('_time'):
                display_value = f"{value}s"
            elif key == 'brightness':
                display_value = f"{value}%"
            else:
                display_value = str(value)
            
            text = f"{display_name}: {display_value}"
            self.draw_text(text, self.font_small, config.WHITE, 
                          config.SCREEN_WIDTH // 2, start_y + (i * line_spacing), center=True)
        
        # Start button
        button_y = config.SCREEN_HEIGHT - 80
        self.draw_text("PRESS ENTER (5) TO START", self.font_normal, config.AMBER, 
                      config.SCREEN_WIDTH // 2, button_y, center=True)
        
        # Draw button box
        button_rect = pygame.Rect(60, button_y - 20, config.SCREEN_WIDTH - 120, 50)
        pygame.draw.rect(self.screen, config.DARK_GREEN, button_rect)
        pygame.draw.rect(self.screen, config.MILITARY_GREEN, button_rect, 2)
        
        # Footer
        self.draw_text("MINUS (-) TO GO BACK", self.font_small, config.GRAY, 
                      config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20, center=True)
