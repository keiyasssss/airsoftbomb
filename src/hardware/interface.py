import pygame
try:
    from gpiozero import Button
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("GPIO not available, running in MOCK mode.")

from src import config

class HardwareInterface:
    def __init__(self):
        self.buttons = {}
        if GPIO_AVAILABLE:
            # Initialize real buttons here if needed, or keep it simple for now
            pass
            
    def update(self):
        """
        Call this once per frame to update hardware state if necessary.
        """
        pass

    def get_events(self, pygame_events):
        """
        Process pygame events and return abstract hardware events.
        Returns a list of strings: 'UP', 'DOWN', 'SELECT', 'BACK', etc.
        """
        actions = []
        
        for event in pygame_events:
            if event.type == pygame.KEYDOWN:
                # Navigation (Numpad 8/2/4/6)
                if event.key == pygame.K_KP8 or event.key == pygame.K_UP:
                    actions.append('UP')
                elif event.key == pygame.K_KP2 or event.key == pygame.K_DOWN:
                    actions.append('DOWN')
                
                # Select (Numpad 5, Enter)
                elif event.key == pygame.K_KP5 or event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    actions.append('SELECT')
                
                # Back (Numpad . or *)
                elif event.key == pygame.K_KP_PERIOD or event.key == pygame.K_KP_MULTIPLY or event.key == pygame.K_BACKSPACE:
                    actions.append('BACK')
                
                # Numeric Input (Numpad 0-9)
                elif event.key == pygame.K_KP0: actions.append('0')
                elif event.key == pygame.K_KP1: actions.append('1')
                elif event.key == pygame.K_KP2: actions.append('2') # Note: 2 is also DOWN, context matters in UI
                elif event.key == pygame.K_KP3: actions.append('3')
                elif event.key == pygame.K_KP4: actions.append('4')
                elif event.key == pygame.K_KP5: actions.append('5') # Note: 5 is also SELECT
                elif event.key == pygame.K_KP6: actions.append('6')
                elif event.key == pygame.K_KP7: actions.append('7')
                elif event.key == pygame.K_KP8: actions.append('8') # Note: 8 is also UP
                elif event.key == pygame.K_KP9: actions.append('9')
                
                # Standard Number keys (Fallback/Debug)
                elif event.key == pygame.K_1: actions.append('1')
                elif event.key == pygame.K_2: actions.append('2')
                elif event.key == pygame.K_3: actions.append('3')
                elif event.key == pygame.K_4: actions.append('4')

        return actions

    def cleanup(self):
        if GPIO_AVAILABLE:
            pass
