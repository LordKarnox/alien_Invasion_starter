import pygame
from typing import TYPE_CHECKING
from Bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
   

class Arsenal:
    # Weapons and ammo for the ship
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()
    def update_arsenal(self):
        self.arsenal.update()

        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self):
        for bullet in self.arsenal.sprites():
            bullet.draw_bullet()

    def fire_bullet(self):
        if len(self.arsenal) < self.settings.bullets_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False

      