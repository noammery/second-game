import pygame
from player import Player  
import random
from sys import exit

pygame.init()
#Arguments:
HEIGHT = 480 #Resolution
WIDTH = 1250 #Resolution
FLOOR = HEIGHT - 130 # minimum height of the floor
SPRITE_WIDTH = 42  # Width of each sprite
SPRITE_HEIGHT =50  # Height of each sprite
SPRITE_SPEED = 5
SCALE_FACTOR = 2
JUMP_HEIGHT = 10  # Maximum height the player will jump
JUMP_FRAMES = 6  # Number of frames in the jump animation

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
main_surface = pygame.transform.scale(pygame.image.load("assets/Backgrounds/Sky.jpg"),(WIDTH, HEIGHT-130)).convert()
main_ground = pygame.transform.scale(pygame.image.load("assets/Backgrounds/Ground.jpg"),(WIDTH, 130)).convert()
enemy_walk_sheet = pygame.image.load("assets/Enemy/Walk.png").convert_alpha()
enemy_attack1_sheet = pygame.image.load("assets/Enemy/Attack1.png").convert_alpha()
enemy_attack2_sheet = pygame.image.load("assets/Enemy/Attack2.png").convert_alpha()
enemy_walk_sheet_flipped = pygame.transform.flip(enemy_walk_sheet, True, False)
enemy_attack1_sheet_flipped = pygame.transform.flip(enemy_attack1_sheet, True, False)
enemy_attack2_sheet_flipped = pygame.transform.flip(enemy_attack2_sheet, True, False)
next_enemy_attack = 3

player = Player(x=100, y=FLOOR - 50)

def get_frame(sheet, frame, width, height, SCALE_FACTOR):
    rect = pygame.Rect(frame * width, 0, width, height)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    scaled_image = pygame.transform.scale(image, (width * SCALE_FACTOR, height * SCALE_FACTOR))
    return scaled_image

enemy_walk_frames = [get_frame(enemy_walk_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
enemy_position = [WIDTH - 2 * SPRITE_WIDTH, HEIGHT - 130 - SPRITE_HEIGHT]
enemy_moving_index = 0
enemy_attck_index = 0
enemy_alive = True

while True: # Main loop
  #Defining movements:
  keys = pygame.key.get_pressed()
  player_moving = False


  if enemy_alive:
     enemy_position[0] -= 5
     if enemy_moving_index < 6:
         enemy_moving_index +=1
     else: 
        enemy_moving_index = 0

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit() 
      exit()
  #Blits:
  player.update()
  screen.blit(main_surface, (0, 0))
  screen.blit(main_ground, (0, HEIGHT - 130))
  screen.blit(enemy_walk_frames[enemy_moving_index - 1], enemy_position)
  player.draw(screen)

  # Update the frame index
  pygame.display.update()
  clock.tick(20)