import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


class Ship:
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal' = None):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_width, self.settings.ship_height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.arsenal = arsenal 
    def update(self):
        # where the ship is
        self._update_ship_movement()
        if self.arsenal:
            self.arsenal.update_arsenal()

        self.rect.x = self.x

    def _update_ship_movement(self):
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= temp_speed

    def draw(self):
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        if self.arsenal:
            return self.arsenal.fire_bullet()
        return False

    def check_collisions(self, other_group):
        return pygame.sprite.spritecollideany(self, other_group) is not None

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False

