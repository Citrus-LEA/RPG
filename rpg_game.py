import pygame
import sys
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

bg_menu = pygame.transform.scale(pygame.image.load('bg_rpg.jpg'), (screen_width, screen_height))
menu_music = pygame.mixer.Sound('lobby_music.mp3')
menu_music.play(-1)

bg_game = pygame.transform.scale(pygame.image.load('bg_rpg_game.jpg'), (screen_width, screen_height))
game_music = pygame.mixer.Sound('rpg_music.mp3')

main_menu = True
running = True
finish = False
game_start = False

class GameSprite:
    def __init__(self, picture, x, y):
        self.image = pygame.transform.scale(pygame.image.load(picture), (100, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, speed):
        self.speed = speed
        self.rotation = 0
        self.frame = 0
        self.animation_timer = 0
        
        self.run_images = []
        for i in range(11, 19):
            img = pygame.transform.scale(pygame.image.load(f'Warrior/Warrior/{i}.png'), (100, 120))
            self.run_images.append(img)
            
        self.idle_image = pygame.transform.scale(pygame.image.load('Warrior/Warrior/1.png'), (100, 120))
        
        self.death_images = []
        for i in range(61, 68):
            img = pygame.transform.scale(pygame.image.load(f'Warrior/Warrior/{i}.png'), (100, 120))
            self.death_images.append(img)
            
        self.attack_images = []
        for i in range(41, 48):
            img = pygame.transform.scale(pygame.image.load(f'Warrior/Warrior/{i}.png'), (100, 120))
            self.attack_images.append(img)

        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def animate(self):
        if self.rotation == 2:
            self.rect.x += self.speed
        elif self.rotation == 3:
            self.rect.x -= self.speed
        
        if self.rect.x > screen_width - 100:
            self.rotation = 0
        if self.rect.x < 0:
            self.rotation = 1

        if self.rotation == 2 or self.rotation == 3:
            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.frame += 1
                if self.frame >= len(self.run_images):
                    self.frame = 0
                
                current_img = self.run_images[self.frame]
                if self.rotation == 3:
                    current_img = pygame.transform.flip(current_img, True, False)
                self.image = current_img
        else:
            self.frame = 0
            self.image = self.idle_image
            if self.rotation == 1:
                self.image = pygame.transform.flip(self.image, True, False)

def start_screen():
    start = pygame.transform.scale(pygame.image.load('start.jpg'), (200, 70))
    start_rect = start.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(start, start_rect)
    
    stop = pygame.transform.scale(pygame.image.load('exit.jpg'), (200, 70))
    stop_rect = stop.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(stop, stop_rect)
    
    return start_rect, stop_rect

hero = Player(300, 450, 3)

start_rect, stop_rect = start_screen()

while running:
    if not finish:
        if main_menu:
            screen.blit(bg_menu, (0, 0))
            start_rect, stop_rect = start_screen() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if main_menu:
                    if start_rect.collidepoint(x, y):
                        game_start = True
                        main_menu = False
                        menu_music.stop()
                        game_music.play(-1)
                    elif stop_rect.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    hero.rotation = 2
                elif event.key == pygame.K_LEFT:
                    hero.rotation = 3
                elif event.key == pygame.K_SPACE:
                    pass
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and hero.rotation == 2:
                    hero.rotation = 0
                elif event.key == pygame.K_LEFT and hero.rotation == 3:
                    hero.rotation = 1

        if game_start:
            screen.blit(bg_game, (0, 0))
            hero.animate()
            hero.draw() 

    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
sys.exit()