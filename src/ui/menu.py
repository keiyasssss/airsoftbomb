import pygame
from src import config
from src.ui.base import BaseView

class MainMenuView(BaseView):
    def __init__(self, manager):
        super().__init__(manager)
        self.menu_items = [
            "DEMOLITION",
            "DOMINATION",
            "HOLD THE BUTTON",
            "NFC PLANT/DEFUSE",
            "HACKING",
            "SETTINGS"
        ]
        self.selected_index = 0

    def handle_input(self, action):
        if action == 'UP':
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif action == 'DOWN':
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        elif action == 'SELECT':
            print(f"Selected: {self.menu_items[self.selected_index]}")
            # TODO: Transition to specific game mode
        elif action == '1': self.selected_index = 0
        elif action == '2': self.selected_index = 1
        elif action == '3': self.selected_index = 2
        elif action == '4': self.selected_index = 3

    def draw(self):
        self.screen.fill(config.BLACK)
        
        # Draw Header
        header_text = "AIRSOFT BOMB SYSTEM"
        self.draw_text(header_text, self.font_header, config.MILITARY_GREEN, config.SCREEN_WIDTH // 2, 30, center=True)
        
        # Draw decorative line
        pygame.draw.line(self.screen, config.MILITARY_GREEN, (20, 60), (config.SCREEN_WIDTH - 20, 60), 2)

        # Draw Menu Items
        start_y = 100
        item_spacing = 35
        
        for i, item in enumerate(self.menu_items):
            color = config.MILITARY_GREEN
            prefix = "  "
            
            if i == self.selected_index:
                color = config.AMBER
                prefix = "> "
                # Draw selection box
                rect = pygame.Rect(40, start_y + (i * item_spacing) - 5, config.SCREEN_WIDTH - 80, 30)
                pygame.draw.rect(self.screen, config.DARK_GREEN, rect)
                pygame.draw.rect(self.screen, config.MILITARY_GREEN, rect, 1)

            text = f"{prefix}{item}"
            self.draw_text(text, self.font_normal, color, 50, start_y + (i * item_spacing))

        # Draw Footer
        footer_text = "USE UP/DOWN TO NAVIGATE - ENTER TO SELECT"
        self.draw_text(footer_text, self.font_small, config.GRAY, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20, center=True)
