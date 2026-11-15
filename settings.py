"""
Program Name: settings.py - Starbase Overdrive (Alien Invasion, Track 1: Custom Game Mechanics)
Author: Boston Deevech
Purpose: Central home for every tunable value in the game. Static values are
    set once in __init__; values that may change during play live in
    initialize_dynamic_settings(). Milestone 1 adds weapon-mode, heat and
    power-up tuning tables used by arsenal.py, bullet.py and powerup.py.
Starter Code Links:
    https://github.com/RedBeard41/alien_Invasion_starter
    https://github.com/LordKarnox/alien_Invasion_starter
Date Updated: 2026-11-15
"""
from pathlib import Path

# Resolve assets relative to this file (not the current working directory) so
# the game launches correctly from any folder on Windows or macOS.
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'Assets'
IMAGES_DIR = ASSETS_DIR / 'images'
SOUND_DIR = ASSETS_DIR / 'sound'
FONTS_DIR = ASSETS_DIR / 'Fonts'


class Settings:
    """Store all static and dynamic settings for Starbase Overdrive."""

    def __init__(self) -> None:
        """Initialize the static settings that never change during a run."""
        # --- Window ---
        self.name: str = 'Starbase Overdrive - Track 1'
        self.screen_width: int = 1200
        self.screen_height: int = 800
        self.FPS: int = 60
        self.bg_file: Path = IMAGES_DIR / 'Starbasesnow.png'

        # --- Ship ---
        self.ship_file: Path = IMAGES_DIR / 'ship2(no bg).png'
        self.ship_width: int = 40
        self.ship_height: int = 60
        # Fraction of the screen (measured up from the bottom) the ship may roam.
        self.ship_move_zone: float = 0.40
        self.shield_max: int = 3
        self.shield_color = (0, 200, 255)

        # --- Bullets / weapons ---
        self.bullet_file: Path = IMAGES_DIR / 'laserBlast.png'
        self.laser_sound: Path = SOUND_DIR / 'laser.mp3'
        self.impact_sound: Path = SOUND_DIR / 'impactSound.mp3'
        self.laser_volume: float = 0.35
        # Hard safety cap on bullets alive at once (replaces the base 5-bullet limit;
        # rate of fire is now limited by per-mode cooldowns and heat instead).
        self.max_bullets: int = 60
        # Each firing mode: cooldown (ms between shots), heat added per shot,
        # bullet speed (px/frame), bullet size (w, h), and the angles (degrees,
        # 0 = straight up, positive = to the right) of the bullets in one volley.
        self.base_weapon_mode: str = 'single'
        self.weapon_modes: dict = {
            'single': {'cooldown': 250, 'heat': 8, 'speed': 12,
                       'size': (25, 80), 'angles': (0,)},
            'spread': {'cooldown': 400, 'heat': 18, 'speed': 10,
                       'size': (20, 60), 'angles': (-15, 0, 15)},
            'rapid':  {'cooldown': 80, 'heat': 5, 'speed': 16,
                       'size': (12, 45), 'angles': (0,)},
        }

        # --- Heat / overheat ---
        self.heat_max: float = 100.0
        self.heat_cool_rate: float = 0.6        # heat lost per frame normally
        self.overheat_cool_rate: float = 0.8    # heat lost per frame while locked
        self.overheat_recover_level: float = 25.0  # weapons unlock at/below this
        self.gauge_width: int = 6
        self.gauge_gap: int = 6

        # --- Power-ups ---
        self.font_file: Path = FONTS_DIR / 'Silkscreen' / 'Silkscreen-Bold.ttf'
        self.text_color = (255, 255, 255)
        self.powerup_size: int = 34
        self.powerup_font_size: int = 14
        self.powerup_speed: float = 2.5
        self.powerup_spawn_ms: int = 4000
        self.weapon_powerup_ms: int = 10000
        self.coolant_ms: int = 5000
        self.powerup_types: dict = {
            'spread':  {'label': 'S', 'color': (255, 140, 0)},
            'rapid':   {'label': 'R', 'color': (220, 40, 220)},
            'coolant': {'label': 'C', 'color': (40, 220, 120)},
            'shield':  {'label': 'SH', 'color': (0, 200, 255)},
        }
        # Number keys 1-4 drop a specific power-up above the ship (demo/testing).
        self.debug_keys: bool = True

        # --- MILESTONE 2 (fleet / scoring) - isolated, not used in M1 ---
        # self.difficulty_scale = 1.1
        # self.scores_file = ASSETS_DIR / 'file' / 'scores.json'
        # self.alien_file = IMAGES_DIR / 'enemy_4.png'
        # self.alien_w = 40
        # self.alien_h = 40
        # self.fleet_direction = 1  # 1 for right, -1 for left

        # --- FINAL SUBMISSION (Play button / HUD) - isolated, not used in M1 ---
        # self.button_w = 200
        # self.button_h = 50
        # self.button_color = (0, 135, 50)
        # self.button_font_size = 48
        # self.HUD_font_size = 20

    def initialize_dynamic_settings(self) -> None:
        """Initialize the settings that can change while the game is played."""
        self.ship_speed: float = 5

        # --- MILESTONE 2 (lives / fleet / scoring) - isolated, not used in M1 ---
        # self.ship_limit = 3
        # self.fleet_speed = 2
        # self.fleet_dropspeed = 40
        # self.alien_points = 50

    # --- MILESTONE 2 (levels) - isolated, not used in M1 ---
    # def increase_difficulty(self):
    #     """Speed the game up after each cleared fleet."""
    #     self.ship_speed *= self.difficulty_scale
    #     self.fleet_speed *= self.difficulty_scale
