import pygame
from src import config

class BaseView:
    def __init__(self, manager):
        self.manager = manager
        self.screen = manager.screen
        self.font_header = pygame.font.Font(config.FONT_MAIN, config.FONT_SIZE_HEADER)
        self.font_normal = pygame.font.Font(config.FONT_MAIN, config.FONT_SIZE_NORMAL)
        self.font_small = pygame.font.Font(config.FONT_MAIN, config.FONT_SIZE_SMALL)

    def handle_input(self, action):
        """
        Handle hardware input actions (UP, DOWN, SELECT, BACK).
        Override this in subclasses.
        """
        pass

    def update(self):
        """
        Update logic for the view.
        Override this in subclasses.
        """
        pass

    def draw(self):
        """
        Draw the view to the screen.
        Override this in subclasses.
        """
        self.screen.fill(config.BLACK)

    def draw_text(self, text, font, color, x, y, center=False):
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)
