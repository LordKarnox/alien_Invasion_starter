import pygame



class Ship:
    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_width, self.settings.ship_height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

    def draw(self):
        self.screen.blit(self.image, self.rect)

def __init__(self, ai_game):
    self.screen = ai_game.screen
    self.settings = ai_game.settings