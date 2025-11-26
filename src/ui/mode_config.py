import pygame
from src import config
from src.ui.base import BaseView

class ModeConfigView(BaseView):
    """
    Generic configuration view for game modes.
    Shows editable parameters before starting the mode.
    """
    def __init__(self, manager, mode_name, mode_class, config_params):
        super().__init__(manager)
        self.mode_name = mode_name
        self.mode_class = mode_class
        self.config_params = config_params  # List of (name, key, default, min, max)
        self.values = {}
        
        # Initialize values
        for name, key, default, min_val, max_val in config_params:
            self.values[key] = default
        
        self.editing_field = None
        self.input_buffer = ""
        
    def handle_input(self, action):
        if self.editing_field is None:
            # Menu mode
            for i, (name, key, default, min_val, max_val) in enumerate(self.config_params):
                if action == str(i + 1):
                    self.editing_field = key
                    self.input_buffer = str(self.values[key])
                    return
            
            if action == 'SELECT' or action == '5':
                # Start game
                self._start_game()
            elif action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
        else:
            # Editing mode
            if action in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.input_buffer += action
            elif action == 'SELECT':
                self._save_edit()
            elif action == 'BACK':
                if self.input_buffer:
                    self.input_buffer = self.input_buffer[:-1]
                else:
                    self.editing_field = None
    
    def _save_edit(self):
        """Save the current edit"""
        if not self.input_buffer:
            self.editing_field = None
            return
        
        try:
            # Find the config param
            for name, key, default, min_val, max_val in self.config_params:
                if key == self.editing_field:
                    value = int(self.input_buffer)
                    if min_val <= value <= max_val:
                        self.values[key] = value
                    break
        except ValueError:
            pass
        
        self.editing_field = None
        self.input_buffer = ""
    
    def _start_game(self):
        """Start the game mode with configured values"""
        view = self.mode_class(self.manager)
        # Set configured values
        for key, value in self.values.items():
            if hasattr(view, key):
                setattr(view, key, value)
        self.manager.set_view(lambda mgr: view)
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text(self.mode_name, self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.editing_field:
            # Show editing screen
            field_name = ""
            for name, key, default, min_val, max_val in self.config_params:
                if key == self.editing_field:
                    field_name = name
                    break
            
            self.draw_text(f"EDIT: {field_name}", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 100, center=True)
            self.draw_text(self.input_buffer or "_", self.font_header, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 150, center=True)
            self.draw_text("ENTER TO CONFIRM", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 220, center=True)
            self.draw_text("MINUS (-) TO DELETE", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
        else:
            # Show configuration menu
            self.draw_text("CONFIGURATION:", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 80, center=True)
            
            start_y = 120
            line_spacing = 30
            
            for i, (name, key, default, min_val, max_val) in enumerate(self.config_params):
                value = self.values[key]
                text = f"{i + 1}. {name}: {value}"
                self.draw_text(text, self.font_small, config.MILITARY_GREEN, 
                              50, start_y + (i * line_spacing))
            
            # Start button
            button_y = config.SCREEN_HEIGHT - 80
            self.draw_text("PRESS ENTER (5) TO START", self.font_normal, config.AMBER, 
                          config.SCREEN_WIDTH // 2, button_y, center=True)
            button_rect = pygame.Rect(60, button_y - 20, config.SCREEN_WIDTH - 120, 50)
            pygame.draw.rect(self.screen, config.DARK_GREEN, button_rect)
            pygame.draw.rect(self.screen, config.MILITARY_GREEN, button_rect, 2)
            
            self.draw_text("PRESS NUMBER TO EDIT - MINUS (-) TO GO BACK", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20, center=True)
