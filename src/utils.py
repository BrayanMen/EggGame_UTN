from game_functions import *
import os

base_path = os.path.dirname(__file__)
font_path = os.path.join(base_path, "./assets/fonts/Merathus.ttf")
sound_click_path = os.path.join(base_path, "./assets/sounds/click1.mp3")
sound_coin_path = os.path.join(base_path, "./assets/sounds/coin.mp3")
sound_over_path = os.path.join(base_path, "./assets/sounds/game_over.mp3")
sound_jump_path = os.path.join(base_path, "./assets/sounds//jump.mp3")

# Frame Image
egg_frames = image_frames_list_game(egg_images, "assets/egg/eggMAsked",14, 70,70)
EGG_RESPIRACION = [egg_frames[0],egg_frames[1]]
EGG_CAMINAR = [egg_frames[2],egg_frames[1],egg_frames[3]]
EGG_SALTAR = [egg_frames[4]]
EGG_CAER = [egg_frames[5],egg_frames[1]]
EGG_ATAQUE = [egg_frames[6],egg_frames[7],egg_frames[8],egg_frames[1]]
EGG_ATAQUE_AIRE = [egg_frames[9],egg_frames[10],egg_frames[11],egg_frames[4]]
EGG_ROTO = [egg_frames[12],egg_frames[13],egg_frames[14]]

# Frame Power
egg_power_frame = image_frames_list_game(power_image, "assets/attacks/atackframe",2,70,70)
# Plataformas Frames
platforms_frames = image_frames_list_game(platforms_images,"./assets/plataforms/plataforms",20,random.randint(200, 400),100)

# Background
bg_game = image_scale_game("assets/background/night_autumn", WIDTH_SCREEN, HEIGHT_SCREEN)

# Items
coins_frames = image_frames_list_game(coins_images,"assets/coin/goldCoin",8, 64,64)
knife_image = image_scale_game("assets/items/knife",60,50)
heart_image = image_scale_game("assets/items/Heart",60,60)


canciones = ["music0.mp3", "music1.mp3", "music2.mp3", "music3.mp3", "music4.mp3"]
canciones_nombres = ["Cancion 1", "Cancion 2", "Cancion 3", "Cancion 4", "Cancion 5"]

musica_json = []
for i in range(len(canciones)):
    canc_json = {"musica": canciones[i], "nombre": canciones_nombres[i]}
    musica_json.append(canc_json)
    
guardar_archivo_json(musica_json, "musica")