import pygame
import settings
from game_functions import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(settings.SCREEN_SIZE)
pygame.display.set_caption("El Huevo Enmascarado")
pygame.display.set_icon(pygame.image.load("./src/assets/egg/eggMAsked1.png"))


# Frame Image
egg_frames = image_frames_list_game(egg_images, "assets/egg/eggMAsked",14, 70,70)
EGG_RESPIRACION = [egg_frames[0],egg_frames[1]]
EGG_CAMINAR = [egg_frames[2],egg_frames[1],egg_frames[3]]
EGG_SALTAR = [egg_frames[4]]
EGG_CAER = [egg_frames[5],egg_frames[1]]
EGG_ATAQUE = [egg_frames[6],egg_frames[7],egg_frames[8],egg_frames[1]]
EGG_ATAQUE_AIRE = [egg_frames[9],egg_frames[10],egg_frames[11],egg_frames[4]]
EGG_ROTO = [egg_frames[12],egg_frames[13],egg_frames[14]]

image_egg = EGG_RESPIRACION[1]
egg_rect = image_egg.get_rect(center = (100,500))

# platforms_frames = image_frames_list_game(platforms_images,"./assets/plataforms/plataforms")

# Background
bg_game = image_scale_game("assets/background/night_autumn", WIDTH_SCREEN, HEIGHT_SCREEN)

# Items
coins_frames = image_frames_list_game(coins_images,"assets/coin/goldCoin",8, 64,64)
knife_image = image_scale_game("assets/items/knife",60,50)

suelo = pygame.Surface((settings.WIDTH_SCREEN, 50))
suelo.fill((100, 100, 100))
suelo_rect = suelo.get_rect(midtop=(settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN - 50))



def main():
    global is_running,FPS,frame_indice,speed_animacion,image_egg,egg_rect,voltear, speed_y, speed_x,en_suelo,esta_roto
    global dist_caida, esta_atacando, atacando_en_el_aire, der, izq, up,proyectiles,knife_image
    speed_x=3
    x= 0
    y=0
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not esta_roto:
                        if en_suelo:
                            esta_atacando = True
                        elif not suelo:
                            atacando_en_el_aire = True
                if event.key == pygame.K_LEFT:
                    izq =True  
                if event.key == pygame.K_RIGHT:
                    der = True
                if event.key == pygame.K_UP:
                    up=True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    izq = False
                if event.key == pygame.K_RIGHT:
                    der = False
                if event.key == pygame.K_UP:
                    up = False
            
        if izq:
            egg_rect.x -= speed_x
            x= egg_rect.x
            if not voltear:
                voltear = True
            image_egg,frame_indice = animacion_frames(EGG_CAMINAR,frame_indice,speed_animacion)
        if der:
            egg_rect.x += speed_x
            x= egg_rect.x  
            if voltear:
                voltear = False
            image_egg,frame_indice = animacion_frames(EGG_CAMINAR,frame_indice,speed_animacion)
        if up:
            if en_suelo and not esta_roto:
                speed_y = -15
                en_suelo = False
                
        if not esta_roto:
            speed_y += 1
            egg_rect.y += speed_y
            if not en_suelo:
                if speed_y > 0:
                    image_egg,frame_indice = animacion_frames(EGG_CAER,frame_indice,speed_animacion)
                else:
                    image_egg,frame_indice = animacion_frames(EGG_SALTAR,frame_indice,speed_animacion)
            else:
                if esta_atacando:
                    image_egg,frame_indice = animacion_frames(EGG_ATAQUE,frame_indice,speed_animacion)
                    esta_atacando = False
                elif atacando_en_el_aire:
                    image_egg,frame_indice = animacion_frames(EGG_ATAQUE_AIRE,frame_indice,0.009)
                    atacando_en_el_aire = False
                
                elif not izq and not der:
                    image_egg,frame_indice = animacion_frames(EGG_RESPIRACION,frame_indice,0.03)
                        
                                                
        if egg_rect.colliderect(suelo_rect):
            if dist_caida >= 10:
                egg_rect.bottom = suelo_rect.top
                speed_y = 0
                en_suelo = True
                esta_roto = True
                image_egg = animacion_frames(EGG_ROTO, frame_indice, speed_animacion)
            else:
                egg_rect.bottom = suelo_rect.top
                speed_y = 0
                en_suelo = True
                dist_caida = 0
        
        for cuchillo in proyectiles[:]:
                cuchillo.x -= 2
                # if egg_rect.colliderect(cuchillo):
                #     vidas -= 1
                #     proyectiles.remove(cuchillo)
        if random.randint(0, 500) < 2:
                lanzar_cuchillos(proyectiles)
                        
                
        screen.blit(bg_game,(0,0))
        for cuchillo in proyectiles:
            screen.blit(knife_image, cuchillo.topleft)
        screen.blit(suelo, suelo_rect.topleft)
        
        if voltear:
            screen.blit(pygame.transform.flip(image_egg, True, False), egg_rect)
        else:
            screen.blit(image_egg, egg_rect)
    
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()