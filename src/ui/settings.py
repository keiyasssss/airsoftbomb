import pygame
from src import config
from src.ui.base import BaseView
from src.utils.settings import get_settings

class SettingsView(BaseView):
    """
    Settings screen for configuring game parameters
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.settings = get_settings()
        self.menu_items = [
            "1. BOMB CODE",
            "2. COUNTDOWN TIME",
            "3. SOUND",
            "4. BRIGHTNESS",
            "5. RESET DEFAULTS",
            "6. SAVE & EXIT"
        ]
        self.editing_mode = None
        self.input_buffer = ""
        
    def handle_input(self, action):
        if self.editing_mode:
            # Handle editing mode
            if action in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.input_buffer += action
            elif action == 'SELECT':
                self._save_edit()
            elif action == 'BACK':
                if self.input_buffer:
                    self.input_buffer = self.input_buffer[:-1]
                else:
                    self.editing_mode = None
        else:
            # Handle menu selection
            if action == '1':
                self.editing_mode = 'bomb_code'
                self.input_buffer = str(self.settings.get('bomb_code'))
            elif action == '2':
                self.editing_mode = 'countdown_time'
                self.input_buffer = str(self.settings.get('countdown_time'))
            elif action == '3':
                # Toggle sound
                current = self.settings.get('sound_enabled')
                self.settings.set('sound_enabled', not current)
            elif action == '4':
                self.editing_mode = 'brightness'
                self.input_buffer = str(self.settings.get('brightness'))
            elif action == '5':
                self.settings.reset_to_defaults()
            elif action == '6':
                self.settings.save()
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
            elif action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
    
    def _save_edit(self):
        """Save the current edit"""
        if not self.input_buffer:
            self.editing_mode = None
            return
            
        try:
            if self.editing_mode == 'bomb_code':
                self.settings.set('bomb_code', self.input_buffer)
            elif self.editing_mode == 'countdown_time':
                value = int(self.input_buffer)
                if 10 <= value <= 300:
                    self.settings.set('countdown_time', value)
            elif self.editing_mode == 'brightness':
                value = int(self.input_buffer)
                if 10 <= value <= 100:
                    self.settings.set('brightness', value)
        except ValueError:
            pass
        
        self.editing_mode = None
        self.input_buffer = ""
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text("SETTINGS", self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.editing_mode:
            # Show editing screen
            self.draw_text(f"EDITING: {self.editing_mode.upper().replace('_', ' ')}", 
                          self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 100, center=True)
            self.draw_text(self.input_buffer or "_", self.font_header, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 150, center=True)
            self.draw_text("ENTER TO CONFIRM", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 220, center=True)
            self.draw_text("MINUS (-) TO DELETE", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
        else:
            # Show settings menu
            start_y = 70
            item_spacing = 30
            
            # Display each setting with current value
            values = [
                f": {self.settings.get('bomb_code')}",
                f": {self.settings.get('countdown_time')}s",
                f": {'ON' if self.settings.get('sound_enabled') else 'OFF'}",
                f": {self.settings.get('brightness')}%",
                "",
                ""
            ]
            
            for i, (item, value) in enumerate(zip(self.menu_items, values)):
                color = config.MILITARY_GREEN
                text = item + value
                self.draw_text(text, self.font_small, color, 
                              40, start_y + (i * item_spacing))
            
            # Footer
            self.draw_text("PRESS NUMBER TO EDIT - MINUS (-) TO GO BACK", 
                          self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20, center=True)
