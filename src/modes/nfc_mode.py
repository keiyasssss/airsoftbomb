import pygame
import time
from src import config
from src.ui.base import BaseView

class NFCModeView(BaseView):
    """
    NFC Plant/Defuse mode
    - Simulates NFC card reading (mocked for now)
    - Press specific keys to simulate card tap
    """
    def __init__(self, manager):
        super().__init__(manager)
        from src.utils.settings import get_settings
        settings = get_settings()
        
        self.state = "WAITING"  # WAITING, ARMED, DEFUSED, EXPLODED
        self.valid_cards = ['1234', '5678']  # Simulated NFC card IDs
        self.countdown_time = settings.get('countdown_time', 45)
        self.plant_time = None
        self.last_beep = 0
        self.beep_interval = 1.0
        
    def handle_input(self, action):
        if self.state == "WAITING":
            # Simulate NFC tap with number sequences
            if action == '1':
                print("Card 1234 detected - PLANTING BOMB")
                self.state = "ARMED"
                self.plant_time = time.time()
            elif action == '2':
                print("Card 5678 detected - PLANTING BOMB")
                self.state = "ARMED"
                self.plant_time = time.time()
            elif action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
                
        elif self.state == "ARMED":
            if action == '1' or action == '2':
                print("Valid card detected - DEFUSING")
                self.state = "DEFUSED"
            elif action == 'BACK':
                pass  # Can't go back when armed
                
        elif self.state in ["DEFUSED", "EXPLODED"]:
            if action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
    
    def update(self):
        if self.state == "ARMED":
            elapsed = time.time() - self.plant_time
            remaining = self.countdown_time - elapsed
            
            if remaining <= 0:
                self.state = "EXPLODED"
            else:
                if remaining < 10:
                    self.beep_interval = 0.2
                elif remaining < 20:
                    self.beep_interval = 0.5
                    
                if time.time() - self.last_beep > self.beep_interval:
                    self.last_beep = time.time()
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text("NFC PLANT/DEFUSE", self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.state == "WAITING":
            self.draw_text("TAP CARD TO PLANT", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 120, center=True)
            self.draw_text("(Press 1 or 2 to simulate)", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 160, center=True)
            
            # Draw NFC icon simulation
            pygame.draw.circle(self.screen, config.MILITARY_GREEN, 
                             (config.SCREEN_WIDTH // 2, 220), 30, 3)
            pygame.draw.circle(self.screen, config.MILITARY_GREEN, 
                             (config.SCREEN_WIDTH // 2, 220), 20, 2)
            pygame.draw.circle(self.screen, config.MILITARY_GREEN, 
                             (config.SCREEN_WIDTH // 2, 220), 10, 2)
                             
        elif self.state == "ARMED":
            elapsed = time.time() - self.plant_time
            remaining = max(0, self.countdown_time - elapsed)
            
            color = config.MILITARY_GREEN if remaining > 10 else config.ALERT_RED
            self.draw_text(f"{int(remaining):02d}", self.font_header, color, 
                          config.SCREEN_WIDTH // 2, 100, center=True)
            
            self.draw_text("BOMB ARMED!", self.font_normal, config.ALERT_RED, 
                          config.SCREEN_WIDTH // 2, 160, center=True)
            self.draw_text("TAP CARD TO DEFUSE", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 200, center=True)
            self.draw_text("(Press 1 or 2)", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 230, center=True)
                          
        elif self.state == "DEFUSED":
            self.draw_text("BOMB DEFUSED!", self.font_header, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
                          
        elif self.state == "EXPLODED":
            self.draw_text("BOMB EXPLODED!", self.font_header, config.ALERT_RED, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
