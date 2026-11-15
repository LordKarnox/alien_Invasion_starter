"""
Program Name: alien_invasion.py - Starbase Overdrive (Alien Invasion, Track 1: Custom Game Mechanics)
Author: Boston Deevech
Purpose: Main game loop. Milestone 1 is a rapid prototype of the custom
    mechanics: four-way ship movement, hold-to-fire with three firing modes,
    weapon heat/overheat, and falling power-ups (Spread, Rapid, Coolant,
    Shield). The base tutorial's alien fleet, scoring, HUD and Play button are
    isolated (commented out) until Milestone 2 and the Final Submission.

    Controls: WASD / arrow keys move, hold SPACE to fire, Q or ESC quits.
    Debug (settings.debug_keys): 1 = Spread, 2 = Rapid, 3 = Coolant,
    4 = Shield power-up dropped above the ship.
Starter Code Links:
    https://github.com/RedBeard41/alien_Invasion_starter
    https://github.com/LordKarnox/alien_Invasion_starter
Date Updated: 2026-11-15
"""
import sys
import pygame
from ship import Ship
from settings import Settings
from arsenal import Arsenal
from powerup import PowerUpManager

# --- MILESTONE 2 (fleet / lives / scoring) - isolated, not used in M1 ---
# from time import sleep
# from alien_fleet import AlienFleet
# from game_stats import GameStats

# --- FINAL SUBMISSION (Play button / HUD) - isolated, not used in M1 ---
# from button import Button
# from hud import HUD


class AlienInvasion:
    """Overall class that owns the window, the game objects and the main loop."""

    # Maps number keys to the power-up they drop when debug keys are on.
    DEBUG_DROPS = {pygame.K_1: 'spread', pygame.K_2: 'rapid',
                   pygame.K_3: 'coolant', pygame.K_4: 'shield'}

    def __init__(self) -> None:
        """Initialize pygame, the window, sounds and all M1 game objects."""
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file).convert()
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_width, self.settings.screen_height))
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        # Reused in M1 as the power-up pickup sound.
        self.impact_sound = pygame.mixer.Sound(str(self.settings.impact_sound))
        self.impact_sound.set_volume(0.5)

        self.ship = Ship(self, Arsenal(self))
        self.powerups = PowerUpManager(self)

        # M1 has no Play button, so the prototype starts active immediately.
        self.game_active = True

        # --- MILESTONE 2 - isolated ---
        # self.game_stats = GameStats(self)
        # self.alien_fleet = AlienFleet(self)
        # --- FINAL SUBMISSION - isolated ---
        # self.game_active = False
        # self.play_button = Button(self, 'Play')
        # self.HUD = HUD(self)

    def run_game(self) -> None:
        """Run the main loop: input, update, collisions, draw, tick."""
        while self.running:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.powerups.update()
                self._check_powerup_pickups()
                # self.alien_fleet.update_fleet()   # MILESTONE 2
                # self._check_collisions()          # MILESTONE 2

            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _update_screen(self) -> None:
        """Redraw the background, power-ups and ship, then flip the display."""
        self.screen.blit(self.bg, (0, 0))
        self.powerups.draw()
        self.ship.draw()
        # self.alien_fleet.draw()                   # MILESTONE 2
        # self.HUD.draw()                           # FINAL SUBMISSION
        # if not self.game_active:                  # FINAL SUBMISSION
        #     self.play_button.draw()
        #     pygame.mouse.set_visible(True)
        pygame.display.flip()

    def _check_events(self) -> None:
        """Respond to window, keyboard (and later mouse) events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN and self.game_active:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # elif event.type == pygame.MOUSEBUTTONDOWN:   # FINAL SUBMISSION
            #     self._check_button_clicked()

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Start moving/firing, drop debug power-ups, or quit on key press."""
        if event.key in (pygame.K_d, pygame.K_RIGHT):
            self.ship.moving_right = True
        elif event.key in (pygame.K_a, pygame.K_LEFT):
            self.ship.moving_left = True
        elif event.key in (pygame.K_w, pygame.K_UP):
            self.ship.moving_up = True
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self.ship.firing = True
        elif self.settings.debug_keys and event.key in self.DEBUG_DROPS:
            self.powerups.spawn(self.DEBUG_DROPS[event.key], self.ship.rect.centerx)
        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
            self._quit()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """Stop moving/firing when the matching key is released."""
        if event.key in (pygame.K_d, pygame.K_RIGHT):
            self.ship.moving_right = False
        elif event.key in (pygame.K_a, pygame.K_LEFT):
            self.ship.moving_left = False
        elif event.key in (pygame.K_w, pygame.K_UP):
            self.ship.moving_up = False
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.ship.moving_down = False
        elif event.key == pygame.K_SPACE:
            self.ship.firing = False

    def _check_powerup_pickups(self) -> None:
        """Apply any power-ups the ship touched and play the pickup sound."""
        if self.powerups.check_pickups(self.ship):
            self.impact_sound.play()
            self.impact_sound.fadeout(400)

    def _quit(self) -> None:
        """Shut pygame down and exit the program."""
        self.running = False
        # self.game_stats.save_scores()             # MILESTONE 2
        pygame.quit()
        sys.exit()

    # ==================================================================
    # MILESTONE 2 - fleet collisions, lives and levels (isolated in M1)
    # ==================================================================
    # def _check_collisions(self):
    #     """Handle ship/fleet, fleet/bottom and bullet/alien collisions."""
    #     if (self.ship.check_collisions(self.alien_fleet.fleet)
    #             or self.alien_fleet.check_fleet_bottom()):
    #         self._check_game_status()
    #         return
    #     collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
    #     if collisions:
    #         self.impact_sound.play()
    #         self.impact_sound.fadeout(500)
    #         self.game_stats.update(collisions)
    #         self.HUD.update_scores()
    #     if self.alien_fleet.check_destroyed_status():
    #         self._reset_level()
    #         self.settings.increase_difficulty()
    #         self.game_stats.update_level()
    #         self.HUD.update_level()
    #
    # def _check_game_status(self):
    #     """Lose a life, then reset the level or end the game."""
    #     self.game_stats.ships_left -= 1
    #     if self.game_stats.ships_left > 0:
    #         self._reset_level()
    #         self.ship.center_ship()
    #         sleep(0.5)
    #     else:
    #         self.game_active = False
    #
    # def _reset_level(self):
    #     """Clear bullets and rebuild the alien fleet."""
    #     self.ship.arsenal.arsenal.empty()
    #     self.alien_fleet.fleet.empty()
    #     self.alien_fleet.fleet_direction = self.settings.fleet_direction
    #     self.alien_fleet.create_fleet()

    # ==================================================================
    # FINAL SUBMISSION - Play button and restart (isolated in M1)
    # ==================================================================
    # def _check_button_clicked(self):
    #     """Start a new game when the Play button is clicked."""
    #     mouse_pos = pygame.mouse.get_pos()
    #     if self.play_button.check_clicked(mouse_pos):
    #         self.restart_game()
    #
    # def restart_game(self):
    #     """Reset settings, stats, HUD and level, then go active."""
    #     self.settings.initialize_dynamic_settings()
    #     self.game_stats.reset_stats()
    #     self.HUD.update_scores()
    #     self.HUD.update_level()
    #     self._reset_level()
    #     self.ship.center_ship()
    #     self.game_active = True
    #     pygame.mouse.set_visible(False)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
