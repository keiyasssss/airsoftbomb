import pygame
from src import config

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_view = None
        self.running = True

    def set_view(self, view_class):
        """
        Switch to a new view.
        """
        self.current_view = view_class(self)

    def handle_input(self, actions):
        if self.current_view:
            for action in actions:
                self.current_view.handle_input(action)

    def update(self):
        if self.current_view:
            self.current_view.update()

    def draw(self):
        if self.current_view:
            self.current_view.draw()
        else:
            self.screen.fill(config.BLACK)
