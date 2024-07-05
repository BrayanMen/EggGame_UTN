WIDTH_SCREEN = 800
HEIGHT_SCREEN = 600
SCREEN_SIZE = (WIDTH_SCREEN, HEIGHT_SCREEN)
x_width = WIDTH_SCREEN // 2
x_height = HEIGHT_SCREEN // 2

FPS = 60

# Variables Globales

speed_y = 0
speed_x = 0

bg_x = 0
speed_bg = 5

dist_caida = 0

frame_indice = 0
siguiente_frame = 0
speed_animacion = 0.2

coin_indice = 0
speed_coin_animacion = 0.04

# Variables de Interaccion

puntaje = 0
vidas = 3

# Estados del Juego

is_running = True
en_suelo = False
esta_roto = False
esta_atacando = False
atacando_en_el_aire = False
voltear = False
izq= False
der= False
up = False

# Listas del Juego

coins = []
enemigos = []
proyectiles = []
# Lista para imagenes
coins_images = []
platforms_images = []
egg_images = []

