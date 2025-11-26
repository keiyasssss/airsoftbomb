import pygame
import time
import random
from src import config
from src.ui.base import BaseView

class HackingView(BaseView):
    """
    Hacking mode: Minigame with moving bar
    - Stop the bar in the green zone to hack
    - Multiple rounds to complete
    """
    def __init__(self, manager):
        super().__init__(manager)
        from src.utils.settings import get_settings
        settings = get_settings()
        
        self.state = "PLAYING"  # PLAYING, SUCCESS, FAILED
        self.bar_position = 0.0  # 0.0 to 1.0
        self.bar_speed = 0.5  # units per second
        self.bar_direction = 1  # 1 or -1
        self.target_zone_start = 0.4
        self.target_zone_end = 0.6
        self.rounds_completed = 0
        self.rounds_needed = settings.get('hacking_rounds', 3)
        self.last_update = time.time()
        self.attempts = 0
        self.max_attempts = settings.get('hacking_max_attempts', 5)
        
    def handle_input(self, action):
        if self.state == "PLAYING":
            if action == 'SELECT' or action == '5':
                # Check if in target zone
                if self.target_zone_start <= self.bar_position <= self.target_zone_end:
                    self.rounds_completed += 1
                    if self.rounds_completed >= self.rounds_needed:
                        self.state = "SUCCESS"
                    else:
                        # Reset for next round, make it harder
                        self.bar_speed += 0.1
                        self.target_zone_start = random.uniform(0.2, 0.6)
                        self.target_zone_end = self.target_zone_start + random.uniform(0.15, 0.25)
                else:
                    self.attempts += 1
                    if self.attempts >= self.max_attempts:
                        self.state = "FAILED"
                        
            elif action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
                
        elif self.state in ["SUCCESS", "FAILED"]:
            if action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
    
    def update(self):
        if self.state == "PLAYING":
            current_time = time.time()
            delta = current_time - self.last_update
            self.last_update = current_time
            
            self.bar_position += self.bar_speed * self.bar_direction * delta
            
            # Bounce at edges
            if self.bar_position >= 1.0:
                self.bar_position = 1.0
                self.bar_direction = -1
            elif self.bar_position <= 0.0:
                self.bar_position = 0.0
                self.bar_direction = 1
    
    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Header
        self.draw_text("HACKING MINIGAME", self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.state == "PLAYING":
            # Round info
            self.draw_text(f"ROUND {self.rounds_completed + 1}/{self.rounds_needed}", 
                          self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 80, center=True)
            self.draw_text(f"ATTEMPTS: {self.attempts}/{self.max_attempts}", 
                          self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 110, center=True)
            
            # Draw track
            track_y = 160
            track_width = config.SCREEN_WIDTH - 80
            track_x = 40
            
            # Background track
            pygame.draw.rect(self.screen, config.GRAY, 
                           (track_x, track_y, track_width, 30), 2)
            
            # Target zone (green)
            zone_start_x = track_x + int(track_width * self.target_zone_start)
            zone_width = int(track_width * (self.target_zone_end - self.target_zone_start))
            pygame.draw.rect(self.screen, config.DARK_GREEN, 
                           (zone_start_x, track_y, zone_width, 30))
            pygame.draw.rect(self.screen, config.MILITARY_GREEN, 
                           (zone_start_x, track_y, zone_width, 30), 2)
            
            # Moving bar
            bar_x = track_x + int(track_width * self.bar_position)
            pygame.draw.rect(self.screen, config.AMBER, 
                           (bar_x - 3, track_y - 5, 6, 40))
            
            # Instructions
            self.draw_text("PRESS ENTER WHEN IN GREEN ZONE", self.font_small, config.WHITE, 
                          config.SCREEN_WIDTH // 2, 220, center=True)
            self.draw_text("MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
                          
        elif self.state == "SUCCESS":
            self.draw_text("HACK SUCCESSFUL!", self.font_header, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("SYSTEM COMPROMISED", self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 190, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
                          
        elif self.state == "FAILED":
            self.draw_text("HACK FAILED!", self.font_header, config.ALERT_RED, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("TOO MANY FAILED ATTEMPTS", self.font_normal, config.ALERT_RED, 
                          config.SCREEN_WIDTH // 2, 190, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
