import pygame
from settings import SPRITE_WIDTH, SPRITE_HEIGHT

class PowerUp:
    def __init__(self, x, y):
        self.position = [x, y]
        self.image = pygame.image.load("assets/PowerUps/HealthPickup.png").convert_alpha()
        # Resize the image to match SPRITE_WIDTH and SPRITE_HEIGHT
        self.image = pygame.transform.scale(self.image, (SPRITE_WIDTH + 10, SPRITE_HEIGHT + 10))
        self.rect = pygame.Rect(x, y, SPRITE_WIDTH, SPRITE_HEIGHT)

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def get_rect(self):
        return self.rect
