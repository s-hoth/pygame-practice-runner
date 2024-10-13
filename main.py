import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2_surf = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1_surf, player_walk_2_surf]
        self.player_index = 0
        self.player_jump_surf = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump_surf
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1_surf = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2_surf = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1_surf, fly_2_surf]
            y_pos = 210
        else:
            snail_1_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2_surf = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1_surf, snail_2_surf]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks()/ 1000) - start_time
    score_surface = test_font.render(f'Score:  {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def collison_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner') #window title
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/pixel_type.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

#player group
player = pygame.sprite.GroupSingle()
player.add(Player())

#obstacle group
obstacle_group = pygame.sprite.Group()

sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

#intro screen
stand_surf = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
stand_surf = pygame.transform.rotozoom(stand_surf, 0 , 2)
stand_rect = stand_surf.get_rect(center = (400, 200))

title_surf = test_font.render('Pixel Runner', False, (111,196,169))
title_rect = title_surf.get_rect(center = (400,80))

instructions_surf = test_font.render('press space to jump', False, (111,196,169))
instructions_rect = instructions_surf.get_rect(center = (400,340))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == obstacle_timer: obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                game_active = True 
                start_time = int(pygame.time.get_ticks() / 1000)
        
    if game_active:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collison_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(stand_surf, stand_rect)

        #display title text
        screen.blit(title_surf,title_rect)

        score_surface = test_font.render(f'Score:  {score}', False, (111,196,169))
        score_rect = score_surface.get_rect(center = (400,330))

        if score == 0: screen.blit(instructions_surf,instructions_rect)
        else: screen.blit(score_surface,score_rect)

    pygame.display.update()
    clock.tick(60) #ceiling 
