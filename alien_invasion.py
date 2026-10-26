import sys
import pygame
from ship import Ship
from settings import Settings
from arsenal import Arsenal
from alien_fleet import AlienFleet
from game_stats import GameStats
from time import sleep

class AlienInvasion:

    def __init__(self):
        self.settings = Settings()
        self.game_stats = GameStats(self.settings.ship_limit)
        self.game_active = True
        pygame.init()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_width, self.settings.screen_height))
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(str(self.settings.laser_sound))
        self.laser_sound.set_volume(0.5)
        self.impact_sound = pygame.mixer.Sound(str(self.settings.impact_sound))
        self.impact_sound.set_volume(0.5)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)

    def run_game(self):
        while self.running:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()

            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _update_screen(self):
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)



    def _check_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.game_active:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)



        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

    def _check_collisions(self):
        if (
            self.ship.check_collisions(self.alien_fleet.fleet)
            or self.alien_fleet.check_fleet_bottom()
        ):
            self._check_game_status()
            return

        collisions = self.alien_fleet.check_collisions(
            self.ship.arsenal.arsenal
        )

        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()

    def _check_game_status(self):
        self.game_stats.ships_left -= 1
        print(f"Ships left: {self.game_stats.ships_left}")

        if self.game_stats.ships_left > 0:
            self._reset_level()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            print("Game over!")

    def _reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.fleet_direction = self.settings.fleet_direction
        self.alien_fleet.create_fleet()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game() 
    