import pygame
from settings import SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR, WIDTH, SPRITE_SPEED, JUMP_FRAMES
from utils import get_frame

class Player():
    def __init__(self, x, y):
        self.position = [x, y]
        self.walk_sheet = pygame.image.load("assets/Player/Walk.png").convert_alpha()
        self.walk_attack1_sheet = pygame.image.load("assets/Player/WalkAttack1.png").convert_alpha()
        self.walk_attack2_sheet = pygame.image.load("assets/Player/WalkAttack2.png").convert_alpha()
        self.walk_sheet = pygame.image.load("assets/Player/Walk.png").convert_alpha()
        self.jump_sheet = pygame.image.load("assets/Player/Jump.png").convert_alpha()
        self.attack1_sheet = pygame.image.load("assets/Player/Attack1.png").convert_alpha()
        self.attack2_sheet = pygame.image.load("assets/Player/Attack2.png").convert_alpha()
        self.death_sheet = pygame.image.load("assets/Player/Death.png").convert_alpha()
        self.block_sheet = pygame.image.load("assets/Player/Squat.png").convert_alpha()
        self.walk_sheet_flipped = pygame.transform.flip(self.walk_sheet, True, False)
        self.attack1_sheet_flipped = pygame.transform.flip(self.attack1_sheet, True, False)
        self.attack2_sheet_flipped = pygame.transform.flip(self.attack2_sheet, True, False)
        self.walk_attack1_sheet_flipped = pygame.transform.flip(self.walk_attack1_sheet, True, False)
        self.walk_attack2_sheet_flipped = pygame.transform.flip(self.walk_attack2_sheet, True, False)
        self.jump_sheet_flipped = pygame.transform.flip(self.jump_sheet, True, False)
        self.block_sheet_flipped = pygame.transform.flip(self.block_sheet, True, False)
        self.walk_frames = [get_frame(self.walk_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.jump_frames = [get_frame(self.jump_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.attack1_frames = [get_frame(self.attack1_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.attack2_frames = [get_frame(self.attack2_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.walk_attack1_frames = [get_frame(self.walk_attack1_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.walk_attack2_frames = [get_frame(self.walk_attack2_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.death_frames = [get_frame(self.death_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.block_frames = [get_frame(self.block_sheet, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(4)]
        self.walk_frames_flipped = [get_frame(self.walk_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.attack1_frames_flipped = [get_frame(self.attack1_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.attack2_frames_flipped = [get_frame(self.attack2_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.walk_attack1_frames_flipped = [get_frame(self.walk_attack1_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.walk_attack2_frames_flipped = [get_frame(self.walk_attack2_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.jump_frames_flipped = [get_frame(self.jump_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(6)]
        self.block_frames_flipped = [get_frame(self.block_sheet_flipped, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE_FACTOR) for i in range(4)]
        
        self.moving_index = 0
        self.attacking_index = 0
        self.jumping_index = 0
        self.death_index = 0
        self.block_index = 0
        self.walk_attack_index = 0
        self.frame_index = 0
        self.moving = False 
        self.attacking = False
        self.jumping = False
        self.death = False
        self.strike = False
        self.walk_attack_R = False
        self.walk_attack_L = False
        self.space_clicked = False
        self.life = 2
        self.hit = False
        self.direction = True #True - right, False - left 
        self.block = False  


    def start_jumping(self):
        self.jumping = True
        self.jumping_index = 0
    def start_attacking(self):
        self.attacking = True
        self.attacking_index = 0

    def start_walk_attacking_R(self):
        self.walk_attack_R = True
        self.walk_attack_index = 0
    
    def start_walk_attacking_L(self):  
        self.walk_attack_L = True
        self.walk_attack_index = 0

    def update(self):
        self.moving = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.position[0] >= 0:
            self.position[0] -= SPRITE_SPEED
            self.moving = True
            self.direction = False
        if keys[pygame.K_RIGHT] and self.position[0] <= WIDTH - SPRITE_WIDTH:
            self.position[0] += SPRITE_SPEED
            self.moving = True
            self.direction = True
        if keys[pygame.K_1] and not self.attacking and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.start_attacking()
        if keys[pygame.K_1] and keys[pygame.K_RIGHT] and not self.attacking and self.position[0] <= WIDTH - SPRITE_WIDTH and not self.walk_attack_R:
            self.start_walk_attacking_R()
        if keys[pygame.K_1] and keys[pygame.K_LEFT] and not self.attacking and self.position[0] >= 0 + SPRITE_WIDTH and not self.walk_attack_L:
            self.start_walk_attacking_L()
        if keys[pygame.K_SPACE] and not self.space_clicked:
            self.space_clicked = True
            self.start_jumping()
        if keys[pygame.K_2] and not self.attacking and not self.moving:
            self.block = True
        else:
            self.block = False
        if self.life == 0:
            self.death = True
        
        self.get_rect() 

        if self.jumping:
            if self.jumping_index < JUMP_FRAMES // 2:
                self.position[1] -= 10
                self.jumping_index += 1
            elif JUMP_FRAMES // 2 <= self.jumping_index < JUMP_FRAMES:
                self.position[1] += 10
                self.jumping_index += 1
            elif self.jumping_index == JUMP_FRAMES:
                self.jumping_index = 0
                self.jumping = False
                self.space_clicked = False

        if self.attacking and not self.moving and not self.block:
            if self.attacking_index < 6:
                self.attacking_index += 1
            else:
                if not self.strike:
                    self.strike = True
                else:
                    self.strike = False
                self.attacking_index = 0
                self.attacking = False

        if self.walk_attack_R and not self.block:
            if self.walk_attack_index < 6:
                self.position[0] += 1
                self.walk_attack_index += 1
            else:
                if not self.strike:
                    self.strike = True
                else:
                    self.strike = False               
                self.walk_attack_index = 0
                self.walk_attack_R = False

        if self.walk_attack_L and not self.block:
            if self.walk_attack_index < 6:
                self.position[0] -= 1
                self.walk_attack_index += 1
            else:
                if not self.strike:
                    self.strike = True
                else:
                    self.strike = False                      
                self.walk_attack_index = 0
                self.walk_attack_L = False

        if self.block:
            if self.block_index < 4:
                self.block_index += 1
        else:
            if self.block_index > 0:
                self.block_index -= 1

        
        if self.death:
            self.death_index += 1
        

        if self.moving and not self.attacking:
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
        else:
            self.frame_index = 0
        
        


    def get_rect(self):
        return pygame.Rect(self.position[0] + SPRITE_WIDTH / 2, self.position[1], SPRITE_WIDTH, SPRITE_HEIGHT * SCALE_FACTOR)
    
    def got_hit(self):
        if not self.hit and not self.block:  
             self.hit = True
             self.life -= 1
             pygame.time.set_timer(pygame.USEREVENT + 1, 500)  

    def draw(self, screen, FONT):
        if self.attacking and not self.moving and not self.death:
            if not self.strike:
                if self.direction:
                  screen.blit(self.attack1_frames[self.attacking_index % 6], self.position)
                else:  
                  screen.blit(self.attack1_frames_flipped[self.attacking_index % 6], self.position) 
            else:
                if self.direction:
                    screen.blit(self.attack2_frames[self.attacking_index % 6], self.position)
                else:
                    screen.blit(self.attack2_frames_flipped[self.attacking_index % 6], self.position)
        elif self.jumping and not self.death:
            if self.direction:
                screen.blit(self.jump_frames[self.jumping_index % JUMP_FRAMES], self.position)
            else:
                screen.blit(self.jump_frames_flipped[self.jumping_index % JUMP_FRAMES], self.position)
        elif self.walk_attack_R and not self.death:
            if not self.strike:
                screen.blit(self.walk_attack1_frames[self.walk_attack_index % 6], self.position)
            else:
                screen.blit(self.walk_attack2_frames[self.walk_attack_index % 6], self.position)
        elif self.walk_attack_L and not self.death:
            if not self.strike:
                screen.blit(self.walk_attack1_frames_flipped[self.walk_attack_index % 6], self.position)
            else:
                screen.blit(self.walk_attack2_frames_flipped[self.walk_attack_index % 6], self.position)
        elif self.block_index > 0 and not self.death:
            if self.direction:
                screen.blit(self.block_frames[self.block_index - 1], self.position)
            else:
                screen.blit(self.block_frames_flipped[abs(4-self.block_index)], self.position)
        elif not self.death:
            if self.direction:
                screen.blit(self.walk_frames[self.frame_index], self.position)
            else:
                screen.blit(self.walk_frames_flipped[self.frame_index], self.position)
        elif self.death:
            if self.death_index < 6:
                screen.blit(self.death_frames[self.death_index], self.position)
            else:
                pygame.quit()
                exit()

        self.moving_index = (self.moving_index + 1) % len(self.walk_frames)
        player_life = FONT.render(f"Life: {self.life}", 1, "red")
        screen.blit(player_life, (10, 10))



