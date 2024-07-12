import os
import sys
import pygame
from settings import *
import random
from file_functions import *

def image_frames_list_game(lista, path:str,num_image: int,width_image:int, height_image: int)->list[pygame.Surface]:
    base_path = os.path.dirname(__file__)
    
    for i in range(num_image + 1):
        image_path = os.path.join(base_path, f"{path}{i}.png")
        image_frame = pygame.image.load(image_path)
        image_frame_scale = pygame.transform.scale(image_frame, (width_image, height_image))
        lista.append(image_frame_scale)
    return lista

def image_scale_game(path:str,width_image:int, height_image: int):
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, f"{path}.png")
    image_frame = pygame.image.load(image_path)
    image_frame_scale = pygame.transform.scale(image_frame, (width_image, height_image))
    return image_frame_scale

def animacion_frames(lista_frame:list, indice_frame:int, animacion_speed:float):
    indice_frame += animacion_speed
    if indice_frame >= len(lista_frame):
        indice_frame = 0
    frame = lista_frame[int(indice_frame)]
    return frame, indice_frame

def animacion_frames_coin(lista_frame:list, indice_frame:int, animacion_speed:float):
    indice_frame += animacion_speed
    if indice_frame >= len(lista_frame):
        indice_frame = 0
    frame = lista_frame[int(indice_frame)]
    return frame

def lanzar_cuchillos(lista:list):
    proj_x = random.randint(799,WIDTH_SCREEN)
    cuchillo_rect = pygame.Rect(proj_x, random.randint(120, HEIGHT_SCREEN-50), 32, 32)
    velocidad = random.uniform(1, 5)
    cuchillo = {"rect": cuchillo_rect, "velocidad": velocidad}
    lista.append(cuchillo)
    
def coins_puntos(num_coins:int, lista:list, lista_plataforma:list):
    for platform in lista_plataforma:
        for _ in range(num_coins):
            item_x = random.randint(platform["rect"].left, platform["rect"].right)
            item_y = platform["rect"].top - random.randint(40, 100)
            lista.append(pygame.Rect(item_x, item_y, 32, 32))
            
def crear_plataforma(plataform_images: list[pygame.Surface], width_screen: int, height_screen: int, plataformas: list, coins:list):
    """ 
    Crea una nueva plataforma en una ubicación que permita saltos realistas sin superposición.
    """
    min_y = 300
    max_y = height_screen - 100

    min_gap_x = 80  
    max_gap_x = 150  
    min_gap_y = 50   
    max_gap_y = 400  

    if plataformas:
        last_plataforma = plataformas[-1]["rect"]
    else:
        last_plataforma = pygame.Rect(0, height_screen - 100, 200, 50)

    intentos = 0
    max_intentos = 1000

    while intentos < max_intentos:
        plataform_image = random.choice(plataform_images)
        width_p, height_p = plataform_image.get_size()

        x = random.randint(last_plataforma.right + min_gap_x, last_plataforma.right + max_gap_x)
        y = random.randint(min_y, max_y)

        if abs(y - last_plataforma.y) < min_gap_y or abs(y - last_plataforma.y) > max_gap_y:
            y = max(last_plataforma.bottom - max_gap_y, min_y)

        nueva_plataforma = pygame.Rect(x, y, width_p, height_p)

        sobrepuesto = any(nueva_plataforma.colliderect(p["rect"]) for p in plataformas)

        if not sobrepuesto:
            plataformas.append({"image": plataform_image, "rect": nueva_plataforma})
            
            num_coins = random.randint(1,5)
            coins_puntos(num_coins, coins,[plataformas[-1]])
            if random.random() < 0.05:
                hearts.append(pygame.Rect(nueva_plataforma.centerx - 15, nueva_plataforma.top - 30, 30, 30))
            return

        intentos += 1

    print("Se han alcanzado el máximo de intentos para crear una plataforma no superpuesta.")    
    
def actualizar_plataformas(plataformas: list[dict], plataform_images: list[pygame.Surface], jugador_pos:int, width_screen:int, height_screen:int, coins:list):
    while len(plataformas) < 5:
        crear_plataforma( plataform_images, width_screen, height_screen, plataformas, coins)
        
    plataformas_validas = []
    for plataforma in plataformas:
        if plataforma["rect"].right > jugador_pos - width_screen:
            plataformas_validas.append(plataforma)

    return plataformas_validas
    
def create_button(text, font:pygame.font.Font, color, rect):
    button_surface = font.render(text, True, color)
    button_rect = button_surface.get_rect(center=rect.center)
    button_image = pygame.Surface(rect.size, pygame.SRCALPHA)
    button_image.fill((0, 0, 0, 0))
    button_image.blit(button_surface, button_rect.topleft)
    return button_image

def draw_button(text, rect, color,hover_color, hover_scale,font, screen, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = rect.collidepoint(mouse_pos)
    
    if hovered:
        pygame.draw.rect(screen, hover_color, rect,hover_scale)
        if click[0] == 1 and action:
            pygame.time.delay(200)
            action(screen)
    else:
        pygame.draw.rect(screen, color, rect)
    
    text_surf = font.render(text, True, (0,0,0))
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))
    
    return hovered

def swap_lista(lista:list, i:int, j: int)->None:
    lista[i], lista[j] = lista[j], lista[i]

def ordenar_por_criterio(lista:list, campo:str, asc: bool=True):
    TAM = len(lista)
    for i in range(TAM - 1):
        for j in range(i+1, TAM):
                if lista[i][campo] < lista[j][campo] if asc else lista[i][campo] > lista[j][campo]:
                    swap_lista(lista,i,j)
                    
def mostrar_puntajes(screen, font,screen_w, screen_h):
    puntajes = cargar_archivo_csv("top_rank")
    ordenar_por_criterio(puntajes,"puntaje")
    top_5 = puntajes[:5]
    y = 180
    for puntaje in top_5:
        texto = f"{puntaje['nombre']}: {puntaje['puntaje']}"
        puntaje_text = font.render(texto, True, (0,0,0))
        screen.blit(puntaje_text, (screen_w // 2 - 100, y))
        y += 50

def wait_user(tecla):
    continuar = True
    while continuar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == tecla:
                    continuar = False
                    

def lanzar_efecto_espada(rect, poderes, voltear):
    velocidad = 10
    if voltear:
        velocidad = -10
    efecto_rect = pygame.Rect(rect.centerx, rect.centery - 20, 40, 40)
    poderes.append({"rect": efecto_rect, "velocidad": velocidad})