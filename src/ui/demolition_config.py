import pygame
import random
from src import config
from src.ui.base import BaseView

class DemolitionConfigView(BaseView):
    """
    Configuration screen for Demolition mode.
    Allows selecting plant/defuse method and configuring parameters.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.menu_items = [
            "1. CODE ENTRY",
            "2. NFC CARDS",
            "3. HACKING MINIGAME",
            "4. SIMON SAYS"
        ]
        self.selected_method = None
        self.config_state = "METHOD"  # METHOD, CONFIG_CODE, CONFIG_SIMON, READY
        
        # Configuration parameters
        self.bomb_code = self._generate_code(7)
        self.countdown_time = 45
        self.simon_series = 4
        self.simon_digits = 6
        
        self.editing_field = None
        self.input_buffer = ""
        
    def _generate_code(self, length=7):
        """Generate random bomb code"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    def handle_input(self, action):
        if self.config_state == "METHOD":
            if action == '1':
                self.selected_method = "CODE"
                self.config_state = "CONFIG_CODE"
            elif action == '2':
                self.selected_method = "NFC"
                self._start_game()
            elif action == '3':
                self.selected_method = "HACKING"
                self._start_game()
            elif action == '4':
                self.selected_method = "SIMON"
                self.config_state = "CONFIG_SIMON"
            elif action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
                
        elif self.config_state == "CONFIG_CODE":
            if self.editing_field is None:
                if action == '1':
                    # Edit bomb code
                    self.editing_field = "code"
                    self.input_buffer = self.bomb_code
                elif action == '2':
                    # Edit countdown
                    self.editing_field = "countdown"
                    self.input_buffer = str(self.countdown_time)
                elif action == 'SELECT' or action == '5':
                    # Start game
                    self._start_game()
                elif action == 'BACK':
                    self.config_state = "METHOD"
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
                        
        elif self.config_state == "CONFIG_SIMON":
            if self.editing_field is None:
                if action == '1':
                    # Edit series count
                    self.editing_field = "series"
                    self.input_buffer = str(self.simon_series)
                elif action == '2':
                    # Edit digits per series
                    self.editing_field = "digits"
                    self.input_buffer = str(self.simon_digits)
                elif action == '3':
                    # Edit countdown
                    self.editing_field = "countdown"
                    self.input_buffer = str(self.countdown_time)
                elif action == 'SELECT' or action == '5':
                    # Start game
                    self._start_game()
                elif action == 'BACK':
                    self.config_state = "METHOD"
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
            if self.editing_field == "code":
                self.bomb_code = self.input_buffer
            elif self.editing_field == "countdown":
                value = int(self.input_buffer)
                if 10 <= value <= 300:
                    self.countdown_time = value
            elif self.editing_field == "series":
                value = int(self.input_buffer)
                if 1 <= value <= 10:
                    self.simon_series = value
            elif self.editing_field == "digits":
                value = int(self.input_buffer)
                if 3 <= value <= 10:
                    self.simon_digits = value
        except ValueError:
            pass
        
        self.editing_field = None
        self.input_buffer = ""
    
    def _start_game(self):
        """Start the selected game mode"""
        if self.selected_method == "CODE":
            from src.modes.demolition import DemolitionView
            view = DemolitionView(self.manager)
            view.code = self.bomb_code
            view.countdown_time = self.countdown_time
            self.manager.set_view(lambda mgr: view)
        elif self.selected_method == "NFC":
            from src.modes.nfc_mode import NFCModeView
            view = NFCModeView(self.manager)
            view.countdown_time = self.countdown_time
            self.manager.set_view(lambda mgr: view)
        elif self.selected_method == "HACKING":
            from src.modes.hacking import HackingView
            self.manager.set_view(HackingView)
        elif self.selected_method == "SIMON":
            from src.modes.simon_says import SimonSaysPlantView
            self.manager.set_view(lambda mgr: SimonSaysPlantView(
                mgr, self.simon_series, self.simon_digits, self.countdown_time
            ))
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text("DEMOLITION MODE", self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.editing_field:
            # Show editing screen
            field_names = {
                "code": "BOMB CODE",
                "countdown": "COUNTDOWN TIME (s)",
                "series": "NUMBER OF SERIES",
                "digits": "DIGITS PER SERIES"
            }
            self.draw_text(f"EDIT: {field_names.get(self.editing_field, '')}", 
                          self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 100, center=True)
            self.draw_text(self.input_buffer or "_", self.font_header, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 150, center=True)
            self.draw_text("ENTER TO CONFIRM", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 220, center=True)
            self.draw_text("MINUS (-) TO DELETE", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
        elif self.config_state == "METHOD":
            # Show method selection
            self.draw_text("SELECT PLANT/DEFUSE METHOD:", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 80, center=True)
            
            start_y = 120
            item_spacing = 35
            for i, item in enumerate(self.menu_items):
                self.draw_text(item, self.font_normal, config.MILITARY_GREEN, 
                              50, start_y + (i * item_spacing))
            
            self.draw_text("MINUS (-) TO GO BACK", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20, center=True)
                          
        elif self.config_state == "CONFIG_CODE":
            # Show code configuration
            self.draw_text("CODE ENTRY CONFIGURATION", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 80, center=True)
            
            self.draw_text(f"1. BOMB CODE: {self.bomb_code}", self.font_small, config.MILITARY_GREEN, 
                          50, 120)
            self.draw_text(f"2. COUNTDOWN: {self.countdown_time}s", self.font_small, config.MILITARY_GREEN, 
                          50, 150)
            
            # Start button
            button_y = config.SCREEN_HEIGHT - 80
            self.draw_text("PRESS ENTER (5) TO START", self.font_normal, config.AMBER, 
                          config.SCREEN_WIDTH // 2, button_y, center=True)
            button_rect = pygame.Rect(60, button_y - 20, config.SCREEN_WIDTH - 120, 50)
            pygame.draw.rect(self.screen, config.DARK_GREEN, button_rect)
            pygame.draw.rect(self.screen, config.MILITARY_GREEN, button_rect, 2)
            
            self.draw_text("PRESS NUMBER TO EDIT - MINUS (-) TO GO BACK", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20, center=True)
                          
        elif self.config_state == "CONFIG_SIMON":
            # Show Simon configuration
            self.draw_text("SIMON SAYS CONFIGURATION", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 80, center=True)
            
            self.draw_text(f"1. SERIES COUNT: {self.simon_series}", self.font_small, config.MILITARY_GREEN, 
                          50, 120)
            self.draw_text(f"2. DIGITS PER SERIES: {self.simon_digits}", self.font_small, config.MILITARY_GREEN, 
                          50, 150)
            self.draw_text(f"3. COUNTDOWN: {self.countdown_time}s", self.font_small, config.MILITARY_GREEN, 
                          50, 180)
            
            # Start button
            button_y = config.SCREEN_HEIGHT - 80
            self.draw_text("PRESS ENTER (5) TO START", self.font_normal, config.AMBER, 
                          config.SCREEN_WIDTH // 2, button_y, center=True)
            button_rect = pygame.Rect(60, button_y - 20, config.SCREEN_WIDTH - 120, 50)
            pygame.draw.rect(self.screen, config.DARK_GREEN, button_rect)
            pygame.draw.rect(self.screen, config.MILITARY_GREEN, button_rect, 2)
            
            self.draw_text("PRESS NUMBER TO EDIT - MINUS (-) TO GO BACK", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20, center=True)
