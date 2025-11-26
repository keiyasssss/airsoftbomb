import pygame
import time
from src import config
from src.ui.base import BaseView

class DemolitionView(BaseView):
    """
    Demolition mode: Plant & Defuse (CS-Style)
    - Attackers plant bomb with code
    - Countdown starts
    - Defenders must defuse with code
    """
    def __init__(self, manager):
        super().__init__(manager)
        from src.utils.settings import get_settings
        settings = get_settings()
        
        self.state = "MENU"  # MENU, PLANT, ARMED, DEFUSE, EXPLODED, DEFUSED
        self.code = settings.get('bomb_code', '7355608')
        self.input_code = ""
        self.countdown_time = settings.get('countdown_time', 45)
        self.plant_time = None
        self.beep_interval = 1.0  # seconds between beeps
        self.last_beep = 0
        
    def handle_input(self, action):
        if self.state == "MENU":
            if action in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.input_code += action
                if len(self.input_code) > 10:
                    self.input_code = self.input_code[-10:]
            elif action == 'SELECT':
                if self.input_code == self.code:
                    self.state = "ARMED"
                    self.plant_time = time.time()
                    self.input_code = ""
                    print("BOMB PLANTED!")
                else:
                    print("WRONG CODE!")
                    self.input_code = ""
            elif action == 'BACK':
                if self.input_code:
                    self.input_code = self.input_code[:-1]
                else:
                    from src.ui.menu import MainMenuView
                    self.manager.set_view(MainMenuView)
                    
        elif self.state == "ARMED":
            if action in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.input_code += action
                if len(self.input_code) > 10:
                    self.input_code = self.input_code[-10:]
            elif action == 'SELECT':
                if self.input_code == self.code:
                    self.state = "DEFUSED"
                    print("BOMB DEFUSED!")
                else:
                    print("WRONG CODE!")
                    self.input_code = ""
            elif action == 'BACK':
                if self.input_code:
                    self.input_code = self.input_code[:-1]
                    
        elif self.state in ["EXPLODED", "DEFUSED"]:
            if action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
    
    def update(self):
        if self.state == "ARMED":
            elapsed = time.time() - self.plant_time
            remaining = self.countdown_time - elapsed
            
            if remaining <= 0:
                self.state = "EXPLODED"
                print("BOMB EXPLODED!")
            else:
                # Beep faster as time runs out
                if remaining < 10:
                    self.beep_interval = 0.2
                elif remaining < 20:
                    self.beep_interval = 0.5
                    
                if time.time() - self.last_beep > self.beep_interval:
                    self.last_beep = time.time()
                    # TODO: Play beep sound
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text("DEMOLITION MODE", self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.state == "MENU":
            self.draw_text("ENTER CODE TO PLANT:", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 100, center=True)
            self.draw_text("*" * len(self.input_code), self.font_header, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 150, center=True)
            self.draw_text("PRESS ENTER TO CONFIRM", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 220, center=True)
            self.draw_text("MINUS (-) TO GO BACK", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
                          
        elif self.state == "ARMED":
            elapsed = time.time() - self.plant_time
            remaining = max(0, self.countdown_time - elapsed)
            
            # Big countdown
            color = config.MILITARY_GREEN if remaining > 10 else config.ALERT_RED
            self.draw_text(f"{int(remaining):02d}", self.font_header, color, 
                          config.SCREEN_WIDTH // 2, 100, center=True)
            
            self.draw_text("ENTER CODE TO DEFUSE:", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 170, center=True)
            self.draw_text("*" * len(self.input_code), self.font_normal, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 210, center=True)
                          
        elif self.state == "EXPLODED":
            self.draw_text("BOMB EXPLODED!", self.font_header, config.ALERT_RED, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("ATTACKERS WIN", self.font_normal, config.ALERT_RED, 
                          config.SCREEN_WIDTH // 2, 190, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
                          
        elif self.state == "DEFUSED":
            self.draw_text("BOMB DEFUSED!", self.font_header, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("DEFENDERS WIN", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 190, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
