import pygame
from settings import SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR, WIDTH, SPRITE_SPEED, JUMP_FRAMES
from utils import get_frame

class Enemy:
  def __init__(self, x, y):
    self.position = [x, y]
    self.walk_sheet = pygame.image.load("assets/Enemy/Walk.png").convert_alpha()
    self.attack1_sheet = pygame.image.load("assets/Enemy/Attack1.png").convert_alpha()
    self.attack2_sheet = pygame.image.load("assets/Enemy/Attack2.png").convert_alpha()
    self.walk_sheet_flipped = pygame.transform.flip(self.walk_sheet, True, False)
    self.attack1_sheet_flipped = pygame.transform.flip(self.attack1_sheet, True, False)
    self.attack2_sheet_flipped = pygame.transform.flip(self.attack2_sheet, True, False)
    self.walk_frames = [get_frame(self.walk_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
    self.attack1_frames = [get_frame(self.attack1_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
    self.attack2_frames = [get_frame(self.attack2_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]

    self.moving_index = 0
    self.attck_index = 0
    self.alive = True

  def update(self):
      if self.alive:
        self.position[0] -= 5
        if self.moving_index < 6:
          self.moving_index +=1
        else: 
          self.moving_index = 0

  def draw(self, screen):
    screen.blit(self.walk_frames[self.moving_index - 1], self.position)