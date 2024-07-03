import os
import pygame
from settings import *

def image_frames_list_game(lista, path:str,num_image: int,width_image:int, height_image: int)->list[pygame.Surface]:
    base_path = os.path.dirname(__file__)
    
    for i in range(num_image + 1):
        image_path = os.path.join(base_path, f"{path}{i}.png")
        image_frame = pygame.image.load(image_path).convert_alpha()
        image_frame_scale = pygame.transform.scale(image_frame, (width_image, height_image))
        lista.append(image_frame_scale)
    return lista


def image_scale_game(path:str,width_image:int, height_image: int):
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, f"{path}.png")
    image_frame = pygame.image.load(image_path).convert_alpha()
    image_frame_scale = pygame.transform.scale(image_frame, (width_image, height_image))
    return image_frame_scale

def animacion_frames(lista_frame:list, indice_frame:int, animacion_speed:float):
    indice_frame += animacion_speed
    if indice_frame >= len(lista_frame):
        indice_frame = 0
    frame = lista_frame[int(indice_frame)]
    return frame, indice_frame
    
    
def mostrar_texto(superficie,texto,fuente:pygame.font.Font ,coordenada,color=(255,255,255), bg=(0,0,0)):
    sticker = fuente.render(texto,True, color,bg)
    rect = sticker.get_rect()
    rect.center = coordenada
    superficie.blit(sticker,rect)
    
def wait_user(tecla):
    continuar = True
    while continuar:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == tecla:
                    continuar = False
                    
def wait_user_imagen(imagen_rect: pygame.Rect) :
    continuar = True
    while continuar :
        for evento in pygame.event.get() :
            if evento.type == pygame.MOUSEBUTTONDOWN :
                if evento.key == 1:
                    if punta_en_rectangulo(event.pos,imagen_rect):
                        continuar = False   