#!/usr/bin/env python3
import pygame
import sys
from src import config
from src.hardware.interface import HardwareInterface
from src.ui.manager import UIManager
from src.ui.menu import MainMenuView

def main():
    """
    Main entry point for the Airsoft Bomb application.
    """
    print("Airsoft Bomb System Starting...")
    
    # Initialize Pygame
    pygame.init()
    
    # Setup Screen
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Airsoft Bomb")
    
    # Initialize Subsystems
    hardware = HardwareInterface()
    ui_manager = UIManager(screen)
    
    # Set Initial View
    ui_manager.set_view(MainMenuView)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # 1. Event Handling (Pygame + Hardware)
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False
        
        # Get abstract hardware actions
        actions = hardware.get_events(pygame_events)
        
        # Pass actions to UI
        ui_manager.handle_input(actions)
        
        # 2. Update
        hardware.update()
        ui_manager.update()
        
        # 3. Draw
        ui_manager.draw()
        
        pygame.display.flip()
        clock.tick(config.FPS)

    hardware.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
