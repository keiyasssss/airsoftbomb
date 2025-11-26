import pygame
import time
import random
from src import config
from src.ui.base import BaseView

class SimonSaysPlantView(BaseView):
    """
    Simon Says minigame for planting/defusing bomb.
    Shows sequences of numbers that must be repeated.
    """
    def __init__(self, manager, num_series=4, digits_per_series=6, countdown_time=45):
        super().__init__(manager)
        self.num_series = num_series
        self.digits_per_series = digits_per_series
        self.countdown_time = countdown_time
        
        self.state = "PLANT_SHOW"  # PLANT_SHOW, PLANT_INPUT, ARMED, DEFUSE_SHOW, DEFUSE_INPUT, EXPLODED, DEFUSED
        self.current_series = 0
        self.sequences = []
        self.current_sequence = ""
        self.input_buffer = ""
        self.show_start_time = None
        self.show_duration = 5.0  # seconds to show sequence
        self.plant_time = None
        self.last_beep = 0
        self.beep_interval = 1.0
        
        # Generate sequences for planting
        self._generate_sequences()
        
    def _generate_sequences(self):
        """Generate random number sequences"""
        self.sequences = []
        for _ in range(self.num_series):
            sequence = ''.join([str(random.randint(0, 9)) for _ in range(self.digits_per_series)])
            self.sequences.append(sequence)
    
    def handle_input(self, action):
        if self.state == "PLANT_SHOW":
            # Just wait for sequence to finish showing
            pass
            
        elif self.state == "PLANT_INPUT":
            if action in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.input_buffer += action
                if len(self.input_buffer) >= self.digits_per_series:
                    self._check_plant_sequence()
            elif action == 'BACK':
                if self.input_buffer:
                    self.input_buffer = self.input_buffer[:-1]
                else:
                    from src.ui.menu import MainMenuView
                    self.manager.set_view(MainMenuView)
                    
        elif self.state == "ARMED":
            # Can't go back when armed
            pass
            
        elif self.state == "DEFUSE_SHOW":
            # Just wait
            pass
            
        elif self.state == "DEFUSE_INPUT":
            if action in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.input_buffer += action
                if len(self.input_buffer) >= self.digits_per_series:
                    self._check_defuse_sequence()
            elif action == 'BACK':
                if self.input_buffer:
                    self.input_buffer = self.input_buffer[:-1]
                    
        elif self.state in ["EXPLODED", "DEFUSED"]:
            if action == 'BACK':
                from src.ui.menu import MainMenuView
                self.manager.set_view(MainMenuView)
    
    def _check_plant_sequence(self):
        """Check if input matches current sequence"""
        if self.input_buffer == self.current_sequence:
            self.current_series += 1
            self.input_buffer = ""
            if self.current_series >= self.num_series:
                # All sequences completed - bomb planted!
                self.state = "ARMED"
                self.plant_time = time.time()
                print("BOMB PLANTED!")
            else:
                # Next sequence
                self.state = "PLANT_SHOW"
                self.show_start_time = time.time()
        else:
            # Wrong sequence - reset
            print("WRONG SEQUENCE!")
            self.input_buffer = ""
    
    def _check_defuse_sequence(self):
        """Check if defuse input matches sequence"""
        if self.input_buffer == self.current_sequence:
            self.current_series += 1
            self.input_buffer = ""
            if self.current_series >= self.num_series:
                # All sequences completed - bomb defused!
                self.state = "DEFUSED"
                print("BOMB DEFUSED!")
            else:
                # Next sequence
                self.state = "DEFUSE_SHOW"
                self.show_start_time = time.time()
        else:
            # Wrong sequence - reset current series
            print("WRONG SEQUENCE!")
            self.input_buffer = ""
    
    def update(self):
        if self.state == "PLANT_SHOW":
            if self.show_start_time is None:
                self.show_start_time = time.time()
                self.current_sequence = self.sequences[self.current_series]
            elif time.time() - self.show_start_time >= self.show_duration:
                self.state = "PLANT_INPUT"
                self.show_start_time = None
                
        elif self.state == "DEFUSE_SHOW":
            if self.show_start_time is None:
                self.show_start_time = time.time()
                self.current_sequence = self.sequences[self.current_series]
            elif time.time() - self.show_start_time >= self.show_duration:
                self.state = "DEFUSE_INPUT"
                self.show_start_time = None
                
        elif self.state == "ARMED":
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
        self.draw_text("SIMON SAYS MODE", self.font_header, config.MILITARY_GREEN, 
                      config.SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 50), 
                        (config.SCREEN_WIDTH - 20, 50), 2)
        
        if self.state == "PLANT_SHOW":
            self.draw_text(f"MEMORIZE SEQUENCE {self.current_series + 1}/{self.num_series}", 
                          self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 90, center=True)
            self.draw_text(self.current_sequence, self.font_header, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 150, center=True)
            remaining = self.show_duration - (time.time() - self.show_start_time)
            self.draw_text(f"{int(remaining)}s", self.font_normal, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 210, center=True)
                          
        elif self.state == "PLANT_INPUT":
            self.draw_text(f"ENTER SEQUENCE {self.current_series + 1}/{self.num_series}", 
                          self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 90, center=True)
            display = self.input_buffer + "_" * (self.digits_per_series - len(self.input_buffer))
            self.draw_text(display, self.font_header, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 150, center=True)
            self.draw_text("MINUS (-) TO DELETE", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 220, center=True)
                          
        elif self.state == "ARMED":
            elapsed = time.time() - self.plant_time
            remaining = max(0, self.countdown_time - elapsed)
            
            color = config.MILITARY_GREEN if remaining > 10 else config.ALERT_RED
            self.draw_text(f"{int(remaining):02d}", self.font_header, color, 
                          config.SCREEN_WIDTH // 2, 80, center=True)
            
            self.draw_text("BOMB ARMED!", self.font_normal, config.ALERT_RED, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("PRESS 1 TO START DEFUSE", self.font_small, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 180, center=True)
            
            # Start defuse if user presses 1
            if self.state == "ARMED":  # Check again in case it changed
                pass  # Will be handled in handle_input
                
        elif self.state == "DEFUSE_SHOW":
            self.draw_text(f"MEMORIZE SEQUENCE {self.current_series + 1}/{self.num_series}", 
                          self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 90, center=True)
            self.draw_text(self.current_sequence, self.font_header, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 150, center=True)
            remaining = self.show_duration - (time.time() - self.show_start_time)
            self.draw_text(f"{int(remaining)}s", self.font_normal, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 210, center=True)
                          
        elif self.state == "DEFUSE_INPUT":
            self.draw_text(f"ENTER SEQUENCE {self.current_series + 1}/{self.num_series}", 
                          self.font_normal, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 90, center=True)
            display = self.input_buffer + "_" * (self.digits_per_series - len(self.input_buffer))
            self.draw_text(display, self.font_header, config.AMBER, 
                          config.SCREEN_WIDTH // 2, 150, center=True)
                          
        elif self.state == "EXPLODED":
            self.draw_text("BOMB EXPLODED!", self.font_header, config.ALERT_RED, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
                          
        elif self.state == "DEFUSED":
            self.draw_text("BOMB DEFUSED!", self.font_header, config.MILITARY_GREEN, 
                          config.SCREEN_WIDTH // 2, 140, center=True)
            self.draw_text("PRESS MINUS (-) TO EXIT", self.font_small, config.GRAY, 
                          config.SCREEN_WIDTH // 2, 250, center=True)
    
    # Override handle_input to add defuse start
    def handle_input(self, action):
        if self.state == "ARMED" and action == '1':
            # Start defuse sequence
            self.current_series = 0
            self.state = "DEFUSE_SHOW"
            self.show_start_time = None
            return
            
        # Call parent implementation for other cases
        super().handle_input(action)
