import pygame
from player import Player  
from enemy import Enemy
from sys import exit
from settings import WIDTH, HEIGHT, FLOOR, SPRITE_WIDTH, SPRITE_HEIGHT
pygame.font.init()
from powerups import PowerUp
import random


clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
main_surface = pygame.transform.scale(pygame.image.load("assets/Backgrounds/Sky.jpg"),(WIDTH, HEIGHT-130)).convert()
main_ground = pygame.transform.scale(pygame.image.load("assets/Backgrounds/Ground.jpg"),(WIDTH, 130)).convert()



FONT = pygame.font.SysFont("comicsans", 20)

player = Player(x=100, y=FLOOR - SPRITE_HEIGHT)
enemy = Enemy(x=WIDTH - 2 * SPRITE_WIDTH, y=FLOOR - SPRITE_HEIGHT)
powerups = []

terrain = [
    pygame.Rect(200, FLOOR - 50, 100, 20),  # Platform 1
    pygame.Rect(400, FLOOR - 100, 100, 20),  # Platform 2
    pygame.Rect(500, FLOOR - 150, 100, 20),  # Platform 3
]

while True: # Main loop
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit() 
      exit()
    if event.type == pygame.USEREVENT + 1:
      player.hit = False 
      enemy.hit = False
  

  if player.get_rect().colliderect(enemy.get_rect()) and enemy.attack and not player.hit:
    player.got_hit()
  if player.get_rect().colliderect(enemy.get_rect()) and (player.attacking or player.walk_attack_R or player.walk_attack_L) and not enemy.hit:
    enemy.got_hit()
  if random.randint(1,150) == 1 and powerups.__len__() <= 2:  # Adjust frequency as needed and the max amount of powerups at once
    powerups.append(PowerUp(random.randint(50, WIDTH - 50), FLOOR - 15))
  for powerup in powerups:
      if player.get_rect().colliderect(powerup.get_rect()):
          player.life = min(player.life + 1, 10)  # Restore health, max at 10
          powerups.remove(powerup)
  
  player.update()
  enemy.update(player.position)
  player.on_terrain = False  # Reset at start of check
  for rect in terrain:
      if (rect.left <= player.get_rect().right <= rect.right or 
          rect.left <= player.get_rect().left <= rect.right) and player.get_rect().bottom <= (rect.bottom + 10):
                player.on_terrain = True
                player.current_floor = rect.top - SPRITE_HEIGHT//2  # Just use the platform's top
                break
  screen.blit(main_surface, (0, 0))
  screen.blit(main_ground, (0, HEIGHT - 130))
  player.draw(screen,FONT)
  enemy.draw(screen,FONT)
  for powerup in powerups:
    powerup.draw(screen)
  for rect in terrain:
    pygame.draw.rect(screen, (139, 69, 19), rect)  # Brown platforms

  # Update the frame index
  pygame.display.update()
  clock.tick(20)