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

        self.pick_ind += 1
        
        if self.pick_ind >= 56:
            self.pick_ind = 0

        if self.rect.x > bg_width - 100:
            self.rect.x = bg_width - 100
        if self.rect.x < 0:
            self.rect.x = 0

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
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and hero.rotation == 2:
                    hero.rotation = 0
                elif event.key == pygame.K_LEFT and hero.rotation == 3:
                    hero.rotation = 1

        if game_start:
            camera.x = hero.rect.x - screen_width // 2
            camera.y = hero.rect.y - screen_height // 2
            
            camera.x = max(0, min(camera.x, bg_width - screen_width))
            camera.y = max(0, min(camera.y, bg_height - screen_height))
            
            screen.blit(bg_game, (-camera.x, -camera.y))
            
            hero.animate()
            hero.draw() 

    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
sys.exit()
