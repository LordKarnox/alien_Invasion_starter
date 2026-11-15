"""
Program Name: ship.py - Starbase Overdrive (Alien Invasion, Track 1: Custom Game Mechanics)
Author: Boston Deevech
Purpose: The player's ship. Milestone 1 adds free movement inside a lower
    "flight zone" (WASD or arrow keys), hold-to-fire, and a stacking energy
    shield that will absorb enemy hits once return fire arrives in Milestone 2.
Starter Code Links:
    https://github.com/RedBeard41/alien_Invasion_starter
    https://github.com/LordKarnox/alien_Invasion_starter
Date Updated: 2026-11-15
"""
import pygame
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


class Ship:
    """The player-controlled ship, its movement, weapon trigger and shield."""

    def __init__(self, game: 'AlienInvasion',
                 arsenal: Optional['Arsenal'] = None) -> None:
        """Load the ship image and place the ship at the bottom center.

        Args:
            game: The running game, used for the screen and settings.
            arsenal: The weapon system this ship fires with.
        """
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.settings.ship_width, self.settings.ship_height))
        self.rect = self.image.get_rect()

        # The ship may roam only the bottom part of the screen.
        self.top_limit = int(self.screen_rect.height
                             * (1 - self.settings.ship_move_zone))

        self.arsenal = arsenal
        self.firing = False
        self.shield = 0
        self.center_ship()

    def update(self) -> None:
        """Move the ship, auto-fire while the trigger is held, update bullets."""
        self._update_ship_movement()
        if self.firing:
            self.fire()
        if self.arsenal:
            self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        """Move in all four directions while staying inside the flight zone."""
        speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= speed
        if self.moving_up and self.rect.top > self.top_limit:
            self.y -= speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += speed

        # Clamp so float drift can never push the ship out of bounds.
        self.x = max(0.0, min(self.x, self.screen_rect.width - self.rect.width))
        self.y = max(float(self.top_limit),
                     min(self.y, self.screen_rect.height - self.rect.height))
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def draw(self) -> None:
        """Draw bullets, the ship, its shield ring, and its weapon gauges."""
        if self.arsenal:
            self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
        self._draw_shield()
        if self.arsenal:
            self.arsenal.draw_gauges(self.rect)

    def _draw_shield(self) -> None:
        """Draw one ring around the ship for each shield charge."""
        base_radius = max(self.rect.width, self.rect.height) // 2 + 6
        for layer in range(self.shield):
            pygame.draw.circle(self.screen, self.settings.shield_color,
                               self.rect.center, base_radius + layer * 4, 2)

    def fire(self) -> bool:
        """Ask the arsenal to fire; return True if a volley went out."""
        if self.arsenal:
            return self.arsenal.fire_bullet()
        return False

    def add_shield(self, amount: int = 1) -> None:
        """Add shield charges, up to settings.shield_max."""
        self.shield = min(self.settings.shield_max, self.shield + amount)

    def absorb_hit(self) -> bool:
        """Spend a shield charge to block a hit.

        Hook for Milestone 2 enemy return fire.

        Returns:
            True if the shield blocked the hit, False if the ship is exposed.
        """
        if self.shield > 0:
            self.shield -= 1
            return True
        return False

    def center_ship(self) -> None:
        """Put the ship back at the bottom center and stop all movement."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.firing = False

    # --- MILESTONE 2 (ship vs. alien fleet) - isolated, not used in M1 ---
    # def check_collisions(self, other_group):
    #     """Return True if any sprite in other_group touches the ship."""
    #     return pygame.sprite.spritecollideany(self, other_group) is not None
