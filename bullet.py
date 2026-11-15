"""
Program Name: bullet.py - Starbase Overdrive (Alien Invasion, Track 1: Custom Game Mechanics)
Author: Boston Deevech
Purpose: Defines the Bullet sprite. Milestone 1 changes bullets from
    straight-up-only shots into angled projectiles with their own speed and
    pre-rotated image, so the arsenal can fire spread and rapid volleys.
Starter Code Links:
    https://github.com/RedBeard41/alien_Invasion_starter
    https://github.com/LordKarnox/alien_Invasion_starter
Date Updated: 2026-11-15
"""
import math
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Bullet(Sprite):
    """A single projectile that travels in a straight line at a set angle."""

    def __init__(self, game: 'AlienInvasion', image: pygame.Surface,
                 angle_deg: float = 0.0, speed: float = 10.0) -> None:
        """Create a bullet at the ship's nose.

        Args:
            game: The running game, used for the screen and ship position.
            image: Pre-scaled, pre-rotated bullet image (built once by Arsenal
                so we never reload the file from disk for every shot).
            angle_deg: Direction of travel; 0 is straight up, positive values
                lean to the right.
            speed: Distance travelled per frame in pixels.
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = game.ship.rect.midtop

        # Split the speed into x/y velocity. Screen y grows downward, so
        # "up" is negative y.
        radians = math.radians(angle_deg)
        self.vx = speed * math.sin(radians)
        self.vy = -speed * math.cos(radians)

        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def update(self) -> None:
        """Move the bullet one frame along its velocity."""
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (round(self.x), round(self.y))

    def is_off_screen(self, boundaries: pygame.Rect) -> bool:
        """Return True once the bullet has fully left the screen on any side."""
        return not self.rect.colliderect(boundaries)

    def draw_bullet(self) -> None:
        """Draw the bullet at its current position."""
        self.screen.blit(self.image, self.rect)
