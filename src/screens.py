import pygame
from game_functions import *
from utils import *
from file_functions import *
import settings
import sys
from main import *

def ranking_screen(screen):
    is_running_rank = True
    clock = pygame.time.Clock()
    
    logo_image = image_scale_game("assets/logo/logo", 250, 250)
    logo_rect = logo_image.get_rect(center=(settings.WIDTH_SCREEN // 2, 100))
    
    back_image = image_scale_game("assets/items/boton_back", 300, 100)
    back_rect = back_image.get_rect(center=(settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN // 3 + 300))

    tabla_rect = pygame.Rect(settings.WIDTH_SCREEN // 4, 180, settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN - 330)
    tabla_border_color = pygame.Color("gold")
    tabla_fill_color = pygame.Color("gray80")
    tabla_border = 5
    
    while is_running_rank:
        mouse_pos = pygame.mouse.get_pos()
        if back_rect.collidepoint(mouse_pos):
            back_image_scaled = pygame.transform.scale(back_image, (360, 120))
            back_rect_scaled = back_image_scaled.get_rect(center=back_rect.center)
        else:
            back_image_scaled = back_image
            back_rect_scaled = back_rect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_RETURN or event.type == pygame.K_ESCAPE:
                click_sound.play()
                is_running_rank = False
                    

        screen.blit(bg_game, (0, 0))
        pygame.draw.rect(screen, tabla_fill_color, tabla_rect,0 ,99)
        pygame.draw.rect(screen, tabla_border_color, tabla_rect, tabla_border,99)

        mostrar_puntajes(screen, font, WIDTH_SCREEN, HEIGHT_SCREEN)  
        screen.blit(logo_image, logo_rect.topleft)
        screen.blit(back_image_scaled, back_rect_scaled.topleft)
        
        pygame.display.flip()
        clock.tick(30)

def game_over_screen(screen, puntaje):
    global is_running, screen_menu
    clock = pygame.time.Clock()
    input_box = pygame.Rect(settings.WIDTH_SCREEN // 2 - 100, settings.HEIGHT_SCREEN // 2, 250, 80)
    color_inactive = pygame.Color('goldenrod1')
    color_active = pygame.Color('orangered4')
    color = color_inactive
    active = False
    text = ''
    lista_scores = cargar_archivo_csv("top_rank")

    game_over_image = image_scale_game("./assets/items/GameOver", settings.WIDTH_SCREEN // 2 + 100, 200)
    score_text = font.render(f'Puntaje Total: {puntaje}', True, (0, 0, 0))
   
    retry_button_rect = pygame.Rect(settings.WIDTH_SCREEN // 2 - 100, settings.HEIGHT_SCREEN // 2 + 100, 200, 50)
    exit_button_image = image_scale_game("./assets/items/boton_exit", 300,100)
    exit_button_rect = exit_button_image.get_rect(center = (settings.WIDTH_SCREEN // 2, 500))
    
    def reset(screen):
        nonlocal text
        lista_score = {"nombre": text if text else "Anónimo", "puntaje": puntaje}
        lista_scores.append(lista_score)
        guardar_archivo_csv("top_rank", lista_scores)
        text = ''
        main(screen)
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                    color = color_active if active else color_inactive
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        reset(screen)
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
           
        screen.blit(game_over_image, (settings.WIDTH_SCREEN // 2 - game_over_image.get_width() // 2, 100))
        screen.blit(score_text, (settings.WIDTH_SCREEN // 2 - score_text.get_width() // 2, 80))
        txt_surface = font.render(text, True, color_active)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        pygame.draw.rect(screen, color, input_box,0,99)
        screen.blit(txt_surface, (input_box.x, input_box.y))

        draw_button("Retry", retry_button_rect, (0, 255, 0), (0, 200, 0), 3, font, screen, action=reset)
        screen.blit(exit_button_image, exit_button_rect)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
              
def reset_game(screen):
    global is_running, FPS, frame_indice, speed_animacion, image_egg, egg_rect, voltear, speed_y, speed_x, en_suelo, esta_roto
    global dist_caida, esta_atacando, atacando_en_el_aire, der, izq, up, proyectiles, knife_image, coins, coins_frames
    global coins_puntos, coin_indice, speed_coin_animacion, vidas, puntaje, puntaje_acc, suelos, plataforms_list, bg_x, speed_bg
    
    is_running = True
    speed_y = 0
    speed_x = 3
    bg_x = 0
    speed_bg = 5
    dist_caida = 0
    frame_indice = 0
    speed_animacion = 0.2
    coin_indice = 0
    speed_coin_animacion = 0.04
    puntaje_acc = 0
    puntaje = 0
    vidas = 3
    en_suelo = False
    esta_roto = False
    esta_atacando = False
    atacando_en_el_aire = False
    voltear = False
    izq = False
    der = False
    up = False
    coins = []
    enemigos = []
    proyectiles = []
    plataforms_list = [{"image": platforms_frames[3], "rect": pygame.Rect(0, 500, 200, 200)},
                       {"image": platforms_frames[6], "rect": pygame.Rect(300, 300, 200, 200)}]
    
    image_egg = EGG_RESPIRACION[1]
    egg_rect = image_egg.get_rect(center=(100, 100))

    crear_plataforma(platforms_frames, settings.WIDTH_SCREEN, settings.HEIGHT_SCREEN, plataforms_list, coins)
    coins_puntos(random.randint(1, 5), coins, plataforms_list)    

def main(screen):
    global is_running, FPS, frame_indice, speed_animacion, image_egg, egg_rect, voltear, speed_y, speed_x, en_suelo, esta_roto
    global dist_caida, esta_atacando, atacando_en_el_aire, der, izq, up, proyectiles, knife_image, coins, coins_frames
    global coins_puntos, coin_indice, speed_coin_animacion, vidas, puntaje, puntaje_acc, suelos, plataforms_list, bg_x, speed_bg,hearts
    
    reset_game(screen)
    music_paused = False
    pause_image = image_scale_game("assets/items/botones-pause", 150,50)
    pause_rect = pause_image.get_rect(center=(settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN - 100))
    
    while is_running:
        mouse_pos = pygame.mouse.get_pos()
 
        if pause_rect.collidepoint(mouse_pos):
            pause_scaled = pygame.transform.scale(pause_image, (160, 60))
            pause_rect_scaled = pause_scaled.get_rect(center=pause_rect.center)
        else:
            pause_scaled = pause_image
            pause_rect_scaled = pause_rect
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not esta_roto:
                        if en_suelo:
                            esta_atacando = True
                            lanzar_efecto_espada(egg_rect, poderes, voltear)
                        elif not en_suelo:
                            atacando_en_el_aire = True
                            lanzar_efecto_espada(egg_rect, poderes, voltear)
                if event.key == pygame.K_LEFT:
                    izq =True  
                if event.key == pygame.K_RIGHT:
                    der = True
                if event.key == pygame.K_UP:
                    up=True
                if event.key == pygame.K_p:
                    if not music_paused:
                        pygame.mixer.music.pause()
                        continue
                    else:
                        pygame.mixer.music.unpause()
                    music_paused = not music_paused                      
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    izq = False
                if event.key == pygame.K_RIGHT:
                    der = False
                if event.key == pygame.K_UP:
                    up = False
        # wait_user(pygame.K_p)                
        if up:
            if en_suelo and not esta_roto:
                jump_sound.play()
                speed_y = -20
                en_suelo = False
        if izq:
            egg_rect.x -= speed_x
            x = egg_rect.x
            if not voltear:
                voltear = True
            image_egg,frame_indice = animacion_frames(EGG_CAMINAR,frame_indice,speed_animacion)
        if der:
            egg_rect.x += 0.7
            x= egg_rect.x  
            if voltear:
                voltear = False
            image_egg,frame_indice = animacion_frames(EGG_CAMINAR,frame_indice,speed_animacion)
                
            
            if bg_x <= -SCREEN_SIZE[0]:
                bg_x = 0
            bg_x = speed_bg
                
            for platform in plataforms_list:
                platform["rect"].x -= speed_bg
                if platform["rect"].right < 0:
                    plataforms_list.remove(platform)
            plataforms_list = actualizar_plataformas(plataforms_list, platforms_frames, egg_rect.x, WIDTH_SCREEN, HEIGHT_SCREEN, coins)
                        
            for coin in coins:
                coin.x -= speed_bg
                if coin.right < 0:
                    coins.remove(coin)
                    
            for heart in hearts:
                heart.x -= speed_bg
                if heart.right < 0:
                    hearts.remove(heart)
                        
            for cuchillo in proyectiles:
                cuchillo["rect"].x -= speed_bg
                if cuchillo["rect"].right < 0:
                    proyectiles.remove(cuchillo)
          
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
                    
            if egg_rect.bottom >= HEIGHT_SCREEN:
                if dist_caida == 0:
                    image_egg, frame_indice = animacion_frames(EGG_ROTO, frame_indice, speed_animacion)
                    vidas -= 1
                egg_rect.bottom = HEIGHT_SCREEN
                speed_y = 0
                en_suelo = True
            else:
                en_suelo= False
                        
                for plataforma in plataforms_list:
                    plataforma_rect = plataforma["rect"]
                    if egg_rect.colliderect(plataforma_rect):
                        if egg_rect.bottom >= plataforma_rect.top and speed_y > 0:
                            speed_y = 0
                            egg_rect.y = plataforma_rect.top - egg_rect.height
                            en_suelo = True
                        elif egg_rect.right >= plataforma_rect.left and speed_x < plataforma_rect.left:
                            egg_rect.right = plataforma_rect.left
                        elif egg_rect.left <= plataforma_rect.right and speed_x > plataforma_rect.right:
                            egg_rect.left = plataforma_rect.right
        
        for coin in coins[:]:
            if egg_rect.colliderect(coin):
                coin_sound.play()
                coins.remove(coin)
                puntaje += 1
                puntaje_acc += 1 
                if puntaje >= 100:
                    vidas += 1
                    puntaje -=100
                    
        for heart in hearts[:]:
            if egg_rect.colliderect(heart):
                coin_sound.play()
                hearts.remove(heart)
                vidas += 1
                puntaje_acc += 10 
        
        for cuchillo in proyectiles[:]:
            cuchillo["rect"].x -= cuchillo["velocidad"]
            if egg_rect.colliderect(cuchillo["rect"]):
                vidas -= 1
                proyectiles.remove(cuchillo)
                
        for poder in poderes[:]:
            poder["rect"].x += poder["velocidad"]
            if poder["rect"].right < 0 or poder["rect"].left > WIDTH_SCREEN:
                poderes.remove(poder)
            else:
                for cuchillo in proyectiles[:]:
                    if poder["rect"].colliderect(cuchillo["rect"]):
                        poderes.remove(poder)
                        proyectiles.remove(cuchillo)
                        puntaje_acc += 1
                        break
                    
        if random.randint(0, 300) < 2:
            lanzar_cuchillos(proyectiles)
                              
        screen.blit(bg_game,(0,0))
        
        for coin in coins:
            coins_anim = animacion_frames_coin(coins_frames,coin_indice,speed_coin_animacion)
            screen.blit(coins_anim, coin.topleft)
        for heart in hearts:
            screen.blit(heart_image, heart.topleft)
        for plataforma in plataforms_list:
            screen.blit(plataforma["image"], plataforma["rect"].topleft)
        for cuchillo in proyectiles:
            screen.blit(knife_image, cuchillo["rect"].topleft)
        for ataque in poderes:
            image_power = animacion_frames_coin(egg_power_frame, frame_indice,speed_animacion)
            if voltear:
                screen.blit(pygame.transform.flip(image_power, True, False), ataque["rect"].topleft)
            else:
                screen.blit(image_power, ataque["rect"].topleft)
        
        if voltear:
            screen.blit(pygame.transform.flip(image_egg, True, False), egg_rect)
        else:
            screen.blit(image_egg, egg_rect)
            
        puntaje_text = font.render(f"Puntaje: {puntaje}", True, (0,0,0))
        screen.blit(puntaje_text, (15, 10))
        for i in range(vidas):
            screen.blit(heart_image, (20 + i * 50, 80))
        
        if music_paused:
            screen.blit(pause_scaled, pause_rect_scaled)

        if vidas <= 0:
            g_over_sound.play()
            game_over_screen(screen, puntaje_acc)
    
        pygame.display.flip()
        clock.tick(FPS)
   
def options_screen(screen):
    global font
    is_running_options = True
    clock = pygame.time.Clock()

    back_image = image_scale_game("assets/items/boton_back", 300, 100)
    back_rect = back_image.get_rect(center=(settings.WIDTH_SCREEN // 2, settings.HEIGHT_SCREEN - 100))

    canciones_json = cargar_archivo_json("musica")
    
    base_path = os.path.dirname(__file__)
         
    # Inicializar la música
    current_song = None
    pygame.mixer.music.load(os.path.join(base_path, "./assets/music/" + canciones_json[0]["musica"]))
    pygame.mixer.music.play(-1)  

    while is_running_options:
        mouse_pos = pygame.mouse.get_pos()
        if back_rect.collidepoint(mouse_pos):
            back_image_scaled = pygame.transform.scale(back_image, (360, 120))
            back_rect_scaled = back_image_scaled.get_rect(center=back_rect.center)
        else:
            back_image_scaled = back_image
            back_rect_scaled = back_rect
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect_scaled.collidepoint(event.pos):
                    click_sound.play()
                    is_running_options = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    click_sound.play()
                    is_running_options = False

        screen.blit(bg_game, (0, 0))

        y = 150

        for i in range(len(canciones_json)):
            nombre = canciones_json[i]["nombre"]
            song_rect = pygame.Rect(settings.WIDTH_SCREEN // 4, y, settings.WIDTH_SCREEN // 2, 50)
            if song_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (200, 200, 255), song_rect)
            else:
                pygame.draw.rect(screen, (150, 150, 150), song_rect)
            
            song_text = font.render(nombre, True, (0, 0, 0))
            screen.blit(song_text, (song_rect.x + 10, song_rect.y + 10))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if song_rect.collidepoint(event.pos):
                    selected_song = canciones_json[i]["musica"]
                    pygame.mixer.music.load(os.path.join(base_path,"assets/music/" + selected_song))
                    pygame.mixer.music.play(-1)
            
            y += 60

        screen.blit(back_image_scaled, back_rect_scaled.topleft)

        pygame.display.flip()
        clock.tick(30)
        