"""
Program Name: arsenal.py - Starbase Overdrive (Alien Invasion, Track 1: Custom Game Mechanics)
Author: Boston Deevech
Purpose: The ship's weapon system. Milestone 1 replaces the base "5 bullets on
    screen" limit with three firing modes (single, spread, rapid), per-mode
    cooldowns, a heat/overheat mechanic, timed weapon power-ups, a coolant
    effect, and an on-ship heat gauge.
Starter Code Links:
    https://github.com/RedBeard41/alien_Invasion_starter
    https://github.com/LordKarnox/alien_Invasion_starter
Date Updated: 2026-11-15
"""
import pygame
from typing import TYPE_CHECKING
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Arsenal:
    """Manage the ship's bullets, firing modes, cooldowns and weapon heat."""

    def __init__(self, game: 'AlienInvasion') -> None:
        """Set up an empty bullet group, the starting mode, and a cool weapon."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.arsenal = pygame.sprite.Group()

        self.modes = self.settings.weapon_modes
        self.mode = self.settings.base_weapon_mode
        self.mode_started_at = 0
        self.mode_expires_at = 0          # 0 means the mode never expires

        self.heat = 0.0
        self.overheated = False
        self.coolant_until = 0            # time (ms) the no-heat effect ends
        self.last_shot_at = -10_000       # long ago, so the first shot is ready

        self.laser_sound = pygame.mixer.Sound(str(self.settings.laser_sound))
        self.laser_sound.set_volume(self.settings.laser_volume)
        self._images = self._build_images()

    def _build_images(self) -> dict:
        """Pre-scale and pre-rotate one bullet image per mode and angle.

        Returns:
            A dict mapping each mode name to a list of (angle, image) pairs.
        """
        base = pygame.image.load(self.settings.bullet_file).convert_alpha()
        images = {}
        for name, stats in self.modes.items():
            scaled = pygame.transform.scale(base, stats['size'])
            # pygame rotates counter-clockwise, so negate to lean right.
            images[name] = [(angle, pygame.transform.rotate(scaled, -angle))
                            for angle in stats['angles']]
        return images

    # ------------------------------------------------------------------ update
    def update_arsenal(self) -> None:
        """Advance timers, cool the weapon, move bullets and drop stray ones."""
        now = pygame.time.get_ticks()
        self._update_mode_timer(now)
        self._update_heat()

        self.arsenal.update()
        for bullet in self.arsenal.copy():
            if bullet.is_off_screen(self.boundaries):
                self.arsenal.remove(bullet)

    def _update_mode_timer(self, now: int) -> None:
        """Return to the base firing mode once a timed power-up runs out."""
        if self.mode_expires_at and now >= self.mode_expires_at:
            self.mode = self.settings.base_weapon_mode
            self.mode_expires_at = 0

    def _update_heat(self) -> None:
        """Bleed off heat each frame and unlock the weapon once it has cooled."""
        rate = (self.settings.overheat_cool_rate if self.overheated
                else self.settings.heat_cool_rate)
        self.heat = max(0.0, self.heat - rate)
        if self.overheated and self.heat <= self.settings.overheat_recover_level:
            self.overheated = False

    # ------------------------------------------------------------------ firing
    def fire_bullet(self) -> bool:
        """Fire one volley in the current mode if the weapon is ready.

        Returns:
            True if a volley was fired, False if blocked by cooldown,
            overheat, or the bullet cap.
        """
        now = pygame.time.get_ticks()
        stats = self.modes[self.mode]
        if self.overheated:
            return False
        if now - self.last_shot_at < stats['cooldown']:
            return False
        if len(self.arsenal) >= self.settings.max_bullets:
            return False

        for angle, image in self._images[self.mode]:
            self.arsenal.add(Bullet(self.game, image, angle, stats['speed']))
        self.last_shot_at = now
        self._add_heat(stats['heat'], now)
        self.laser_sound.play()
        self.laser_sound.fadeout(150)
        return True

    def _add_heat(self, amount: float, now: int) -> None:
        """Add heat from a shot; lock the weapon if it reaches the maximum."""
        if now < self.coolant_until:
            return
        self.heat = min(self.settings.heat_max, self.heat + amount)
        if self.heat >= self.settings.heat_max:
            self.overheated = True

    # --------------------------------------------------------------- power-ups
    def set_mode(self, mode: str, duration_ms: int = 0) -> None:
        """Switch firing mode, optionally only for a limited time.

        Args:
            mode: A key of settings.weapon_modes.
            duration_ms: How long the mode lasts; 0 makes it permanent.
        """
        now = pygame.time.get_ticks()
        self.mode = mode
        self.mode_started_at = now
        self.mode_expires_at = now + duration_ms if duration_ms else 0

    def apply_coolant(self, duration_ms: int) -> None:
        """Vent all heat and stop shots from adding heat for a while."""
        self.heat = 0.0
        self.overheated = False
        self.coolant_until = pygame.time.get_ticks() + duration_ms

    def coolant_active(self) -> bool:
        """Return True while the coolant effect is running."""
        return pygame.time.get_ticks() < self.coolant_until

    # ----------------------------------------------------------------- drawing
    def draw(self) -> None:
        """Draw every live bullet."""
        for bullet in self.arsenal.sprites():
            bullet.draw_bullet()

    def draw_gauges(self, ship_rect: pygame.Rect) -> None:
        """Draw the heat gauge (right of ship) and mode timer (left of ship).

        These are part of the weapon mechanic itself, not the base-game HUD.
        """
        width = self.settings.gauge_width
        gap = self.settings.gauge_gap
        height = ship_rect.height

        # Heat gauge: green -> yellow -> red; flashes while overheated.
        heat_frame = pygame.Rect(ship_rect.right + gap, ship_rect.top, width, height)
        pygame.draw.rect(self.screen, (40, 40, 40), heat_frame)
        fill_h = int(height * self.heat / self.settings.heat_max)
        fill = pygame.Rect(heat_frame.left, heat_frame.bottom - fill_h, width, fill_h)
        pygame.draw.rect(self.screen, self._heat_color(), fill)
        if self.coolant_active():
            pygame.draw.rect(self.screen, self.settings.powerup_types['coolant']['color'],
                             heat_frame, 1)

        # Mode timer: drains while a timed weapon power-up is active.
        if self.mode_expires_at:
            now = pygame.time.get_ticks()
            total = max(1, self.mode_expires_at - self.mode_started_at)
            left = max(0, self.mode_expires_at - now)
            timer_h = int(height * left / total)
            color = self.settings.powerup_types[self.mode]['color']
            timer = pygame.Rect(ship_rect.left - gap - width,
                                ship_rect.bottom - timer_h, width, timer_h)
            pygame.draw.rect(self.screen, color, timer)

    def _heat_color(self) -> tuple:
        """Pick the heat gauge color for the current heat level."""
        if self.overheated:
            flash_on = (pygame.time.get_ticks() // 150) % 2 == 0
            return (255, 30, 30) if flash_on else (120, 0, 0)
        ratio = self.heat / self.settings.heat_max
        if ratio < 0.5:
            return (60, 220, 60)
        if ratio < 0.8:
            return (240, 210, 40)
        return (255, 90, 30)
