import pygame
from settings import SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR, WIDTH, SPRITE_SPEED, JUMP_FRAMES
from utils import get_frame
import random
import time

class Enemy:
  def __init__(self, x, y):
    self.position = [x, y]
    self.walk_sheet = pygame.image.load("assets/Enemy/Walk.png").convert_alpha()
    self.walk_attack1_sheet = pygame.image.load("assets/Enemy/WalkAttack1.png").convert_alpha()
    self.walk_attack2_sheet = pygame.image.load("assets/Enemy/WalkAttack2.png").convert_alpha()
    self.death_sheet = pygame.image.load("assets/Enemy/Death.png").convert_alpha()
    self.death_sheet_flipped = pygame.transform.flip(self.death_sheet, True, False)
    self.walk_sheet_flipped = pygame.transform.flip(self.walk_sheet, True, False)
    self.walk_attack1_sheet_flipped = pygame.transform.flip(self.walk_attack1_sheet, True, False)
    self.walk_attack2_sheet_flipped = pygame.transform.flip(self.walk_attack2_sheet, True, False)
    self.death_index = 0  
    self.walk_attacking = False
    self.moving = False
    self.moving_index = 0
    self.speed = 5
    self.walk_attack_index = 0
    self.alive = True
    self.attack_colldown = 1
    self.attack = False
    self.strike = False
    self.facing_left = True
    self.change_direction_coll = random.randint(5,10)
    self.surprise_attack_coll = 10 
    self.attack_direction = True
    self.surprise_attacking = False
    self.life = 3 
    self.hit = False



  def start_attacking(self):
    self.walk_attacking = True
  
  def got_hit(self):
    if not self.hit:  
      self.hit = True
      self.life -= 1
      pygame.time.set_timer(pygame.USEREVENT + 1, 500)      
  def update(self,player_position):
    x_delta = self.position[0] - player_position[0]
    if x_delta > 0: 
        self.attack_direction = True
    else: 
        self.attack_direction = False
        

    if self.facing_left and SPRITE_WIDTH  < self.position[0] < WIDTH - SPRITE_WIDTH and self.alive:
      self.moving = True
      self.position[0] -= self.speed
    elif not self.facing_left and WIDTH - SPRITE_WIDTH > self.position[0] > SPRITE_WIDTH and self.alive:
      self.moving = True
      self.position[0] += self.speed
    elif self.alive:
      self.moving = False
      self.moving_index = 0
    if self.moving and self.alive:
      if self.moving_index < 6:
        self.moving_index +=1
      else: 
        self.moving_index = 0

    if abs(self.position[0] - player_position[0]) < 100 and not self.walk_attacking and self.alive:
        self.start_attacking()
    elif not self.alive:
        self.attack = False
    
    if self.walk_attacking and self.attack_colldown == 0 and self.alive:
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
      self.death_frames = [get_frame(self.death_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
    else:
      self.walk_frames = [get_frame(self.walk_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
      self.walk_attack1_frames = [get_frame(self.walk_attack1_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
      self.walk_attack2_frames = [get_frame(self.walk_attack2_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
      self.death_frames = [get_frame(self.death_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]

    # Handle cooldown
    if self.attack_colldown > 0:
      self.attack_colldown -= 1
    
    if self.change_direction_coll <= 0 and not self.surprise_attacking and self.alive:
      if self.facing_left:
        self.facing_left = False
      else:
        self.facing_left = True
      self.change_direction_coll = random.randint(2,10)

    if self.surprise_attack_coll <= 0 and self.alive:
      self.surprise_attacking = True
      self.facing_left = self.attack_direction
      self.speed = 10
      if abs(self.position[0] - player_position[0]) < 10:
        self.surprise_attacking = False
        self.speed = 5
        self.surprise_attack_coll = random.randint(5,10)

    
    if self.change_direction_coll > 0:
      self.change_direction_coll -=0.1

    if self.surprise_attack_coll > 0:
      self.surprise_attack_coll -=0.1

    if self.life <= 0:
      self.alive = False
      if self.death_index < 6:
        self.death_index += 1
      
  def get_rect(self):
    return pygame.Rect(self.position[0], self.position[1], SPRITE_WIDTH, SPRITE_HEIGHT * SCALE_FACTOR)
  
  
  def draw(self, screen,FONT):
    if self.moving and not self.attack and self.alive:
      screen.blit(self.walk_frames[self.moving_index - 1], self.position)
    elif not self.moving and not self.attack and self.alive:
      screen.blit(self.walk_frames[0], self.position)
    if self.walk_attacking and self.attack_colldown == 0 and self.alive:
      if not self.strike:
        screen.blit(self.walk_attack1_frames[self.walk_attack_index % 6], self.position)
      else:
        screen.blit(self.walk_attack2_frames[self.walk_attack_index % 6], self.position)
    if not self.alive:
      if self.death_index < 6:
        screen.blit(self.death_frames[self.death_index % 6], self.position)
    if self.alive:
      enemy_life = FONT.render(f"Enemy Life: {self.life}", 1, "red")
      screen.blit(enemy_life, (WIDTH - enemy_life.get_width() - 2, 10))

    
  

