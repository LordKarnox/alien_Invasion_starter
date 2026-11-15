"""
Program Name: powerup.py - Starbase Overdrive (Alien Invasion, Track 1: Custom Game Mechanics)
Author: Boston Deevech
Purpose: New Milestone 1 module. Defines falling power-up capsules and the
    manager that spawns, moves, draws and collects them. Power-ups grant
    Spread or Rapid fire for a limited time, vent weapon heat (Coolant), or
    add a shield charge. In Milestone 2 destroyed aliens will drop these too.
Starter Code Links:
    https://github.com/RedBeard41/alien_Invasion_starter
    https://github.com/LordKarnox/alien_Invasion_starter
Date Updated: 2026-11-15
"""
import random
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from ship import Ship


class PowerUp(Sprite):
    """A capsule that drifts down the screen until collected or missed."""

    def __init__(self, image: pygame.Surface, kind: str, x: int,
                 speed: float) -> None:
        """Create a power-up just above the top edge of the screen.

        Args:
            image: The capsule image for this kind of power-up.
            kind: A key of settings.powerup_types.
            x: Horizontal center of the capsule in pixels.
            speed: Fall speed in pixels per frame.
        """
        super().__init__()
        self.kind = kind
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, 0))
        self.y = float(self.rect.y)
        self.speed = speed

    def update(self) -> None:
        """Fall one frame."""
        self.y += self.speed
        self.rect.y = round(self.y)


class PowerUpManager:
    """Spawn power-ups on a timer and apply their effect when the ship grabs one."""

    def __init__(self, game: 'AlienInvasion') -> None:
        """Create the power-up group and pre-draw one capsule image per kind."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.powerups = pygame.sprite.Group()
        self.font = pygame.font.Font(self.settings.font_file,
                                     self.settings.powerup_font_size)
        self.images = {kind: self._build_image(info['label'], info['color'])
                       for kind, info in self.settings.powerup_types.items()}
        self.next_spawn_at = pygame.time.get_ticks() + self.settings.powerup_spawn_ms

    def _build_image(self, label: str, color: tuple) -> pygame.Surface:
        """Draw a round, labelled capsule with a transparent background."""
        size = self.settings.powerup_size
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        pygame.draw.circle(image, color, center, size // 2)
        pygame.draw.circle(image, (255, 255, 255), center, size // 2, 2)
        text = self.font.render(label, True, self.settings.text_color)
        image.blit(text, text.get_rect(center=center))
        return image

    def update(self) -> None:
        """Spawn on schedule, move capsules, and drop any that fell off-screen."""
        now = pygame.time.get_ticks()
        if now >= self.next_spawn_at:
            self.spawn()
            self.next_spawn_at = now + self.settings.powerup_spawn_ms

        self.powerups.update()
        for powerup in self.powerups.copy():
            if powerup.rect.top > self.screen_rect.bottom:
                self.powerups.remove(powerup)

    def spawn(self, kind: Optional[str] = None, x: Optional[int] = None) -> None:
        """Drop a power-up from the top of the screen.

        Args:
            kind: Which power-up to drop; random if None.
            x: Horizontal position; random if None.
        """
        if kind is None:
            kind = random.choice(list(self.settings.powerup_types))
        if x is None:
            margin = self.settings.powerup_size
            x = random.randint(margin, self.screen_rect.width - margin)
        self.powerups.add(PowerUp(self.images[kind], kind, x,
                                  self.settings.powerup_speed))

    def check_pickups(self, ship: 'Ship') -> list:
        """Collect every power-up touching the ship and apply its effect.

        Returns:
            The list of PowerUp sprites that were collected this frame.
        """
        collected = pygame.sprite.spritecollide(ship, self.powerups, True)
        for powerup in collected:
            self._apply(powerup.kind, ship)
        return collected

    def _apply(self, kind: str, ship: 'Ship') -> None:
        """Give the ship the effect for one kind of power-up."""
        if kind in ('spread', 'rapid'):
            ship.arsenal.set_mode(kind, self.settings.weapon_powerup_ms)
        elif kind == 'coolant':
            ship.arsenal.apply_coolant(self.settings.coolant_ms)
        elif kind == 'shield':
            ship.add_shield()

    def clear(self) -> None:
        """Remove every power-up from the screen."""
        self.powerups.empty()

    def draw(self) -> None:
        """Draw every falling power-up."""
        self.powerups.draw(self.screen)
