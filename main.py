import pygame
from player import Player  
from enemy import Enemy
from sys import exit
from settings import WIDTH, HEIGHT, FLOOR, SPRITE_WIDTH, SPRITE_HEIGHT

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
main_surface = pygame.transform.scale(pygame.image.load("assets/Backgrounds/Sky.jpg"),(WIDTH, HEIGHT-130)).convert()
main_ground = pygame.transform.scale(pygame.image.load("assets/Backgrounds/Ground.jpg"),(WIDTH, 130)).convert()


player = Player(x=100, y=FLOOR - 50)
enemy = Enemy(x=WIDTH - 2 * SPRITE_WIDTH, y=HEIGHT - 130 - SPRITE_HEIGHT)


while True: # Main loop

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit() 
      exit()

  #Blits:
  player.update()
  enemy.update(player.position)
  screen.blit(main_surface, (0, 0))
  screen.blit(main_ground, (0, HEIGHT - 130))
  player.draw(screen)
  enemy.draw(screen)

  # Update the frame index
  pygame.display.update()
  clock.tick(20)