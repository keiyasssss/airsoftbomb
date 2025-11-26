import pygame
from src import config
from src.ui.base import BaseView

class MainMenuView(BaseView):
    def __init__(self, manager):
        super().__init__(manager)
        self.menu_items = [
            "1. DEMOLITION",
            "2. DOMINATION",
            "3. HOLD THE BUTTON",
            "4. NFC PLANT/DEFUSE",
            "5. HACKING",
            "6. SETTINGS"
        ]

    def handle_input(self, action):
        if action == '1':
            from src.ui.demolition_config import DemolitionConfigView
            self.manager.set_view(DemolitionConfigView)
        elif action == '2':
            from src.ui.mode_config import ModeConfigView
            from src.modes.domination import DominationView
            self.manager.set_view(lambda mgr: ModeConfigView(
                mgr, "DOMINATION MODE", DominationView,
                [
                    ("TARGET TIME (s)", "target_time", 60, 30, 300),
                ]
            ))
        elif action == '3':
            from src.ui.mode_config import ModeConfigView
            from src.modes.hold_button import HoldButtonView
            
            # Create custom view for decimal values
            view = ModeConfigView(
                mgr, "HOLD THE BUTTON", HoldButtonView,
                [
                    ("CAPTURE SPEED (x10)", "capture_speed_x10", 20, 5, 50),
                    ("DECAY SPEED (x10)", "decay_speed_x10", 5, 1, 20),
                ]
            )
            # Override start game to convert values
            original_start = view._start_game
            def custom_start():
                game_view = HoldButtonView(view.manager)
                game_view.capture_speed = view.values['capture_speed_x10'] / 100.0
                game_view.decay_speed = view.values['decay_speed_x10'] / 100.0
                view.manager.set_view(lambda mgr: game_view)
            view._start_game = custom_start
            self.manager.set_view(lambda mgr: view)
        elif action == '4':
            from src.ui.mode_config import ModeConfigView
            from src.modes.nfc_mode import NFCModeView
            self.manager.set_view(lambda mgr: ModeConfigView(
                mgr, "NFC PLANT/DEFUSE", NFCModeView,
                [
                    ("COUNTDOWN TIME (s)", "countdown_time", 45, 10, 300),
                ]
            ))
        elif action == '5':
            from src.ui.mode_config import ModeConfigView
            from src.modes.hacking import HackingView
            self.manager.set_view(lambda mgr: ModeConfigView(
                mgr, "HACKING MODE", HackingView,
                [
                    ("ROUNDS TO WIN", "rounds_needed", 3, 1, 10),
                    ("MAX ATTEMPTS", "max_attempts", 5, 3, 10),
                ]
            ))
        elif action == '6':
            from src.ui.settings import SettingsView
            self.manager.set_view(SettingsView)
        elif action == 'BACK':
            # Exit application
            self.manager.running = False

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
            
            # Draw item with number prefix
            self.draw_text(item, self.font_normal, color, 50, start_y + (i * item_spacing))

        # Draw Footer
        footer_text = "PRESS NUMBER TO SELECT - MINUS (-) TO EXIT"
        self.draw_text(footer_text, self.font_small, config.GRAY, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20, center=True)
