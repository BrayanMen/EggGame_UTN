import pygame
import settings
from game_functions import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(settings.SCREEN_SIZE)
pygame.display.set_caption("El Huevo Enmascarado")

# Frame Image
egg_frames = image_frames_list_game(egg_images, "assets/egg/eggMAsked",14, 64,64)
EGG_RESPIRACION = [egg_frames[0],egg_frames[1]]
EGG_CAMINAR = [egg_frames[2],egg_frames[1],egg_frames[3]]
EGG_SALTAR = [egg_frames[4]]
EGG_CAER = [egg_frames[5]]
EGG_ATAQUE = [egg_frames[6],egg_frames[7],egg_frames[8]]
EGG_ATAQUE_AIRE = [egg_frames[9],egg_frames[10],egg_frames[11]]
EGG_ROTO = [egg_frames[12],egg_frames[13],egg_frames[14]]

coins_frames = image_frames_list_game(coins_images,"assets/coin/goldCoin",8, 64,64)
# platforms_frames = image_frames_list_game(platforms_images,"./assets/plataforms/plataforms")

# Background
bg_game = image_scale_game("assets/background/night_autumn", WIDTH_SCREEN, HEIGHT_SCREEN)


def main():
    global is_running
    #
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
    
        screen.blit(bg_game,(0,0))
        pygame.display.update()

if __name__ == "__main__":
    main()