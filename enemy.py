import pygame
from settings import SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR, WIDTH, SPRITE_SPEED, JUMP_FRAMES
from utils import get_frame
import random

class Enemy:
  def __init__(self, x, y):
    self.position = [x, y]
    self.walk_sheet = pygame.image.load("assets/Enemy/Walk.png").convert_alpha()
    self.walk_attack1_sheet = pygame.image.load("assets/Enemy/WalkAttack1.png").convert_alpha()
    self.walk_attack2_sheet = pygame.image.load("assets/Enemy/WalkAttack2.png").convert_alpha()
    self.walk_sheet_flipped = pygame.transform.flip(self.walk_sheet, True, False)
    self.walk_attack1_sheet_flipped = pygame.transform.flip(self.walk_attack1_sheet, True, False)
    self.walk_attack2_sheet_flipped = pygame.transform.flip(self.walk_attack2_sheet, True, False)
    self.walk_attacking = False
    self.moving = False
    self.moving_index = 0
    self.walk_attack_index = 0
    self.alive = True
    self.attack_colldown = 1
    self.attack = False
    self.strike = False
    self.facing_left = True


  def start_attacking(self):
    self.walk_attacking = True
    
  def update(self,player_position):
    x_delta = self.position[0] - player_position[0]
    if x_delta > 0: 
        self.facing_left = True
    else: 
        self.facing_left = False
        

    if self.facing_left and player_position[0] + (SPRITE_WIDTH / 1.5) < self.position[0] < WIDTH - SPRITE_WIDTH:
      self.moving = True
      self.position[0] -= 5
    elif not self.facing_left and player_position[0] > self.position[0] > SPRITE_WIDTH:
      self.moving = True
      self.position[0] += 5
    else:
      self.moving = False
      self.moving_index = 0
    if self.moving:
      if self.moving_index < 6:
        self.moving_index +=1
      else: 
        self.moving_index = 0

    if abs(self.position[0] - player_position[0]) < 100 and not self.walk_attacking:
        self.start_attacking()
    
    if self.walk_attacking and self.attack_colldown == 0:
      if self.walk_attack_index < 6:
        self.attack = True
        self.walk_attack_index += 1
      else:        
        if not self.strike:
          self.strike = True
        else:
          self.strike = False
        self.attack = False
        self.walk_attack_index = 0  # Reset animation
        self.attack_colldown = random.randint(10,40)  # Set cooldown
    self.get_rect() 

    if self.facing_left:
      self.walk_frames = [get_frame(self.walk_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
      self.walk_attack1_frames = [get_frame(self.walk_attack1_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
      self.walk_attack2_frames = [get_frame(self.walk_attack2_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
    else:
      self.walk_frames = [get_frame(self.walk_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
      self.walk_attack1_frames = [get_frame(self.walk_attack1_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
      self.walk_attack2_frames = [get_frame(self.walk_attack2_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]

    # Handle cooldown
    if self.attack_colldown > 0:
      self.attack_colldown -= 1

  def get_rect(self):
    return pygame.Rect(self.position[0], self.position[1], SPRITE_WIDTH, SPRITE_HEIGHT * SCALE_FACTOR)
  
  
  def draw(self, screen, player_position):
    if player_position[0] - self.position[0] < 0:
      relevant_walk_sheet = self.walk_sheet_flipped
      relevant_walk_attack1_sheet = self.walk_attack1_sheet_flipped 
      relevant_walk_attack2_sheet = self.walk_attack2_sheet_flipped
    else:
      relevant_walk_sheet = self.walk_sheet
      relevant_walk_attack1_sheet = self.walk_attack1_sheet
      relevant_walk_attack2_sheet = self.walk_attack2_sheet
    if self.moving and not self.attack:
      screen.blit(self.walk_frames[self.moving_index - 1], self.position)
    elif not self.moving and not self.attack:
      screen.blit(self.walk_frames[0], self.position)
    if self.walk_attacking and self.attack_colldown == 0:
      if not self.strike:
        screen.blit(self.walk_attack1_frames[self.walk_attack_index % 6], self.position)
      else:
        screen.blit(self.walk_attack2_frames[self.walk_attack_index % 6], self.position)

    pygame.draw.rect(screen, (0, 255, 0), self.get_rect(), 1)  # Red color, width=1
    
  

