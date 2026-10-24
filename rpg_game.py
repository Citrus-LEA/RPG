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

bg_width, bg_height = bg_game.get_size()
camera = pygame.Rect(0, 0, screen_width, screen_height)

main_menu = True
running = True
finish = False
game_start = False

bullets = pygame.sprite.Group()

class GameSprite:
    def init(self, picture, x, y):
        self.image = pygame.transform.scale(pygame.image.load(picture), (100, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))

class Player(GameSprite):
    def __init__(self, x, y, speed):
        self.speed = speed
        self.rotation = 0
        self.pick_ind = 0
        
        path = 'Warrior/Warrior/'
        
        self.move_right = [pygame.transform.scale(pygame.image.load(f'{path}{i}.png'), (100, 120)).convert_alpha() for i in range(11, 19)]
        self.move_left = [pygame.transform.flip(pic, True, False) for pic in self.move_right]
        
        self.stay_right = [pygame.transform.scale(pygame.image.load(f'{path}{i}.png'), (100, 120)).convert_alpha() for i in range(1, 11)]
        self.stay_left = [pygame.transform.flip(pic, True, False) for pic in self.stay_right]

        self.image = self.stay_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.atk = [pygame.transform.scale(pygame.image.load(f'{path}{i}.png'), (100,120)).convert_alpha() for i in range(41,48)]


    def animate(self):
        if self.rotation == 2:
            self.image = self.move_right[self.pick_ind // 7]
            self.rect.x += self.speed
        elif self.rotation == 3:
            self.image = self.move_left[self.pick_ind // 7]
            self.rect.x -= self.speed
        elif self.rotation == 0:
            self.image = self.stay_right[self.pick_ind // 6]
        elif self.rotation == 1:
            self.image = self.stay_left[self.pick_ind // 6]
        elif self.rotation == 4:
                self.image = self.atk[self.pick_ind // 4]


        
        if self.rotation == 4:
                self.pick_ind = (self.pick_ind + 1) % 25
        else:
                self.pick_ind = (self.pick_ind + 1) % 55


        if self.rect.x > bg_width - 100:
            self.rect.x = bg_width - 100
        if self.rect.x < 0:
            self.rect.x = 0




    def update_rotation(self, new_rotation):
                if new_rotation != self.rotation:
                        self.rotation = new_rotation
                        self.pick_ind = 0


class Enemy(GameSprite):
        def update(self):
                if self.rect.x < 7500:
                        self.rect.x += 5

class Bullet(GameSprite):
        def __init__(self, picture, x, y, speed, width, height):
                super().__init__(picture, x, y)
                self.speed = speed
                self.image = pygame.transform.scale(pygame.image.load(picture), (width, height))

        def update(self):
            if hero.rotation == 2:
                    self.rect.x -= self.speed + hero.speed
            else:
            	       self.rect.x -= self.speed

class GameSprite(pygame.sprite.Sprite):
        def __init__(self, picture, x, y):
                super().__init__()
        from random import randint  # скорость движения пули сделаем случайной

def start_screen():
    start = pygame.transform.scale(pygame.image.load('start.jpg'), (200, 70))
    start_rect = start.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(start, start_rect)
    
    stop = pygame.transform.scale(pygame.image.load('exit.jpg'), (200, 70))
    stop_rect = stop.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(stop, stop_rect)
    
    return start_rect, stop_rect

hero = Player(300, 450, 3)

enemy Enemy(600, 450)

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
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and hero.rotation == 2:
                    hero.rotation = 0
                elif event.key == pygame.K_LEFT and hero.rotation == 3:
                    hero.rotation = 1

            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                        hero.update_rotation(0)
                elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                        hero.update_rotation(1)  
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        hero.update_rotation(2)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        hero.update_rotation(3)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        hero.update_rotation(4)

        if game_start:
            camera.x = hero.rect.x - screen_width // 2
            camera.y = hero.rect.y - screen_height // 2
            
            camera.x = max(0, min(camera.x, bg_width - screen_width))
            camera.y = max(0, min(camera.y, bg_height - screen_height))
            
            screen.blit(bg_game, (-camera.x, -camera.y))
            
            hero.animate()
            hero.draw() 

            enemy.draw()
            enemy.update()


    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
sys.exit()
