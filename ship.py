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
        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):

        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= temp_speed

        self.rect.x = self.x

    def draw(self):
        self.screen.blit(self.image, self.rect)

def __init__(self, ai_game):
    self.screen = ai_game.screen
    self.settings = ai_game.settings