import os
import pygame
from settings import *

def image_frames_list_game(lista:list, path:str,num_image: int,width_image:int, height_image: int):
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
    return lista_frame[int(indice_frame)]
    