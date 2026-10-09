import pygame
import sys
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

bg_menu = pygame.transform.scale(pygame.image.load('bg_rpg.jpg'), (screen_width, screen_height))
menu_music = pygame.mixer.Sound('lobby_music.mp3')
menu_music.play(-1)

main_menu = True
running = True
finish = False
game_start = False

def start_screen():
    start = pygame.transform.scale(pygame.image.load('start.jpg'), (200, 70))
    start_rect = start.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(start, start_rect)
    
    stop = pygame.transform.scale(pygame.image.load('exit.jpg'), (200, 70))
    stop_rect = stop.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(stop, stop_rect)
    
    return start_rect, stop_rect

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
                if start_rect.collidepoint(x, y):
                    game_start = True
                    main_menu = False
                    menu_music.stop()
                elif stop_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        if game_start:
            screen.fill((255, 255, 255))

    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
sys.exit()