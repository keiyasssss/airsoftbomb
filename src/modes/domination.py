import pygame
import time
from src import config
from src.ui.base import BaseView

class DominationView(BaseView):
    """
    Domination mode: Time accumulation
    - Two teams accumulate time by holding their button
    - First to reach target time wins
    """
    def __init__(self, manager):
        super().__init__(manager)
        from src.utils.settings import get_settings
        settings = get_settings()
        
        self.state = "PLAYING"  # PLAYING, FINISHED
        self.team_a_time = 0.0
        self.team_b_time = 0.0
        self.target_time = settings.get('domination_target_time', 60.0)
        self.last_update = time.time()
        self.current_holder = None  # None, 'A', or 'B'
        
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
                self.team_a_time += delta
            elif self.current_holder == 'B':
                self.team_b_time += delta
                
            # Check win condition
            if self.team_a_time >= self.target_time:
                self.state = "FINISHED"
                self.winner = 'A'
            elif self.team_b_time >= self.target_time:
                self.state = "FINISHED"
                self.winner = 'B'
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text("DOMINATION MODE", self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.state == "PLAYING":
            # Team A
            self.draw_text("TEAM A (Press 1)", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 80, center=True)
            progress_a = min(1.0, self.team_a_time / self.target_time)
            bar_width = int((config.SCREEN_WIDTH - 80) * progress_a)
            pygame.draw.rect(self.screen, config.MILITARY_GREEN, 
                           (40, 110, bar_width, 20))
            pygame.draw.rect(self.screen, config.GRAY, 
                           (40, 110, config.SCREEN_WIDTH - 80, 20), 1)
            self.draw_text(f"{int(self.team_a_time)}s / {int(self.target_time)}s", 
                          self.font_small, config.WHITE, config.SCREEN_WIDTH // 2, 145, center=True)
            
            # Team B
            self.draw_text("TEAM B (Press 2)", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 180, center=True)
            progress_b = min(1.0, self.team_b_time / self.target_time)
            bar_width = int((config.SCREEN_WIDTH - 80) * progress_b)
            pygame.draw.rect(self.screen, config.AMBER, 
                           (40, 210, bar_width, 20))
            pygame.draw.rect(self.screen, config.GRAY, 
                           (40, 210, config.SCREEN_WIDTH - 80, 20), 1)
            self.draw_text(f"{int(self.team_b_time)}s / {int(self.target_time)}s", 
                          self.font_small, config.WHITE, config.SCREEN_WIDTH // 2, 245, center=True)
            
            # Current holder indicator
            if self.current_holder:
                self.draw_text(f"TEAM {self.current_holder} HOLDING", self.font_normal, 
                              config.ALERT_RED, config.SCREEN_WIDTH // 2, 280, center=True)
                              
        elif self.state == "FINISHED":
            self.draw_text(f"TEAM {self.winner} WINS!", self.font_header, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
