import pygame
import settings
from game_functions import *
import random
from screens import *
from utils import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(settings.SCREEN_SIZE)
pygame.display.set_caption("El Huevo Enmascarado")
pygame.display.set_icon(pygame.image.load("./src/assets/egg/eggMAsked1.png"))

font = pygame.font.Font(font_path,48)

image_egg = EGG_RESPIRACION[1]
egg_rect = image_egg.get_rect(center = (100,100))

plataforms_list = [{"image": platforms_frames[3],"rect":pygame.Rect(0, 500, 200, 200)},
                   {"image": platforms_frames[6],"rect":pygame.Rect(300, 300, 200, 200)}]

# Sounds
click_sound = pygame.mixer.Sound(sound_click_path)
coin_sound = pygame.mixer.Sound(sound_coin_path)
g_over_sound = pygame.mixer.Sound(sound_over_path)
jump_sound = pygame.mixer.Sound(sound_jump_path)

def screen_menu():
    global is_running,screen
    start_image = image_scale_game("assets/items/boton_start", 300, 100)
    exit_image = image_scale_game("assets/items/boton_exit", 300, 100)
    rank_image = image_scale_game("assets/items/boton_ranking", 300, 100)
    options_image = image_scale_game("assets/items/boton_option", 300, 100)
    logo_image = image_scale_game("assets/logo/logo", 250, 250)
    
    logo_rect = logo_image.get_rect(center=(settings.WIDTH_SCREEN // 2, 100))
    start_rect = start_image.get_rect(center=(settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN // 3+10))
    options_rect = options_image.get_rect(center=(settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN // 3 + 100))
    rank_rect = rank_image.get_rect(center=(settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN // 3 + 190))
    exit_rect = exit_image.get_rect(center=(settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN // 3 + 280))
    
    delay_time = 500

    while is_running:
        mouse_pos = pygame.mouse.get_pos()

        if start_rect.collidepoint(mouse_pos):
            start_image_scaled = pygame.transform.scale(start_image, (360, 120))
            start_rect_scaled = start_image_scaled.get_rect(center=start_rect.center)
        else:
            start_image_scaled = start_image
            start_rect_scaled = start_rect

        if options_rect.collidepoint(mouse_pos):
            options_image_scaled = pygame.transform.scale(options_image, (360, 120))
            options_rect_scaled = options_image_scaled.get_rect(center=options_rect.center)
        else:
            options_image_scaled = options_image
            options_rect_scaled = options_rect
            
        if rank_rect.collidepoint(mouse_pos):
            rank_image_scaled = pygame.transform.scale(rank_image, (360, 120))
            rank_rect_scaled = rank_image_scaled.get_rect(center=rank_rect.center)
        else:
            rank_image_scaled = rank_image
            rank_rect_scaled = rank_rect

        if exit_rect.collidepoint(mouse_pos):
            exit_image_scaled = pygame.transform.scale(exit_image, (360, 120))
            exit_rect_scaled = exit_image_scaled.get_rect(center=exit_rect.center)
        else:
            exit_image_scaled = exit_image
            exit_rect_scaled = exit_rect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect_scaled.collidepoint(mouse_pos):
                    pygame.time.delay(delay_time)
                    click_sound.play()
                    main(screen)
                elif options_rect_scaled.collidepoint(mouse_pos):
                    click_sound.play()
                    pygame.time.delay(delay_time)
                    options_screen(screen)
                elif rank_rect_scaled.collidepoint(mouse_pos):
                    click_sound.play()
                    pygame.time.delay(delay_time)
                    ranking_screen(screen)
                elif exit_rect_scaled.collidepoint(mouse_pos):
                    click_sound.play()                    
                    pygame.time.delay(delay_time)
                    is_running = False

            if event.type == pygame.MOUSEMOTION:
                if start_rect_scaled.collidepoint(mouse_pos) or options_rect_scaled.collidepoint(mouse_pos) or exit_rect_scaled.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        screen.blit(bg_game, (0, 0))
        screen.blit(logo_image, logo_rect.topleft)
        screen.blit(start_image_scaled, start_rect_scaled.topleft)
        screen.blit(rank_image_scaled, rank_rect_scaled.topleft)
        screen.blit(options_image_scaled, options_rect_scaled.topleft)
        screen.blit(exit_image_scaled, exit_rect_scaled.topleft)
        
        pygame.display.update()
    
if __name__ == "__main__":
    screen_menu()