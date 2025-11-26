import pygame
import time
from src import config
from src.ui.base import BaseView

class HoldButtonView(BaseView):
    """
    Hold the Button mode: Progressive capture
    - Hold button to fill capture bar
    - First to 100% wins
    """
    def __init__(self, manager):
        super().__init__(manager)
        from src.utils.settings import get_settings
        settings = get_settings()
        
        self.state = "PLAYING"  # PLAYING, FINISHED
        self.team_a_progress = 0.0  # 0.0 to 1.0
        self.team_b_progress = 0.0
        self.last_update = time.time()
        self.capture_speed = settings.get('hold_button_capture_speed', 0.2)
        self.decay_speed = settings.get('hold_button_decay_speed', 0.05)
        self.current_holder = None
        
    def handle_input(self, action):
        if self.state == "PLAYING":
            if action == '1':
                self.current_holder = 'A'
            elif action == '2':
                self.current_holder = 'B'
            elif action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
        elif self.state == "FINISHED":
            if action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
    
    def update(self):
        if self.state == "PLAYING":
            current_time = time.time()
            delta = current_time - self.last_update
            self.last_update = current_time
            
            if self.current_holder == 'A':
                self.team_a_progress += self.capture_speed * delta
                self.team_b_progress -= self.decay_speed * delta
            elif self.current_holder == 'B':
                self.team_b_progress += self.capture_speed * delta
                self.team_a_progress -= self.decay_speed * delta
            else:
                # Decay both when no one is holding
                self.team_a_progress -= self.decay_speed * delta
                self.team_b_progress -= self.decay_speed * delta
            
            # Clamp values
            self.team_a_progress = max(0.0, min(1.0, self.team_a_progress))
            self.team_b_progress = max(0.0, min(1.0, self.team_b_progress))
            
            # Check win condition
            if self.team_a_progress >= 1.0:
                self.state = "FINISHED"
                self.winner = 'A'
            elif self.team_b_progress >= 1.0:
                self.state = "FINISHED"
                self.winner = 'B'
            
            # Reset holder (must hold continuously)
            self.current_holder = None
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text("HOLD THE BUTTON", self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.state == "PLAYING":
            # Team A
            self.draw_text("TEAM A (Hold 1)", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 80, center=True)
            bar_width = int((config.SCREEN_WIDTH - 80) * self.team_a_progress)
            pygame.draw.rect(self.screen, config.MILITARY_GREEN, 
                           (40, 110, bar_width, 25))
            pygame.draw.rect(self.screen, config.GRAY, 
                           (40, 110, config.SCREEN_WIDTH - 80, 25), 2)
            self.draw_text(f"{int(self.team_a_progress * 100)}%", 
                          self.font_small, config.WHITE, config.SCREEN_WIDTH // 2, 150, center=True)
            
            # Team B
            self.draw_text("TEAM B (Hold 2)", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 190, center=True)
            bar_width = int((config.SCREEN_WIDTH - 80) * self.team_b_progress)
            pygame.draw.rect(self.screen, config.AMBER, 
                           (40, 220, bar_width, 25))
            pygame.draw.rect(self.screen, config.GRAY, 
                           (40, 220, config.SCREEN_WIDTH - 80, 25), 2)
            self.draw_text(f"{int(self.team_b_progress * 100)}%", 
                          self.font_small, config.WHITE, config.SCREEN_WIDTH // 2, 260, center=True)
                          
        elif self.state == "FINISHED":
            self.draw_text(f"TEAM {self.winner} WINS!", self.font_header, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
