import cv2 as cv

import mss
import pyautogui
import numpy as np
import webcolors

import time

from collections import Counter 

### Funções auxiliares ###

green_colors = [color for color in webcolors.names(webcolors.CSS3) if "green" in color or color == "olivedrab"]

#Determina qual a cor mais frequente da imagem
def most_frequent_color(screenshot):
    width, height = screenshot.size
    
    rgb_total = []

    for x in range(0, width):
        for y in range(0, height):

            r,g,b = screenshot.pixel(x,y)

            rgb_total.append(str(r)+" "+str(g)+" "+str(b))
    
    rgb_dict = Counter(rgb_total)

    return rgb_dict.most_common(1)

#Define cor mais próxima de uma dada cor
def closest_color(rgb):
    differences = {}
    for color_name in webcolors.names(spec=webcolors.CSS3):
        color_hex = webcolors.name_to_hex(color_name)
        r, g, b = webcolors.hex_to_rgb(color_hex)
        differences[sum([(r - rgb[0]) ** 2,
                        (g - rgb[1]) ** 2,
                        (b - rgb[2]) ** 2])] = color_name

    return differences[min(differences.keys())]

#Retorna se a cor "color_name" é predominante
def is_color_commmon(color_name, screenshot):

    colors_to_compare = None
    match(color_name):
        case "green":
            colors_to_compare = green_colors
        case None:
            colors_to_compare = None

    #Cor predominante da imagem
    frequent_colors = most_frequent_color(screenshot)

    #Converte para tuplas depois de remover espaços
    color_rgb = tuple(int(num_str) for num_str in frequent_colors[0][0].split())

    if(closest_color(color_rgb) in colors_to_compare):
        print("É verde")
    else:
        print("Não é verde")

### Fim das funções auxiliares ###



#Obter o tamanho da tela
width, height = pyautogui.size()

#Medidas da tela divididas em 4 - a ideia não é capturar a tela toda, apenas a região do centro
smallwidth = int(width/16) #120 px
smallheight = int(height/9) #120 px

#Tamanho da captura
screenshot = {"top": smallheight*4, "left": smallwidth*7, "width": smallwidth*3, "height": smallheight}

with mss.mss() as sct:

    while "Captura de tela":
        #last_time = time.time()

        #Captura a imagem e salva num array Numpy
        pure_img = sct.grab(screenshot)
        sct_img = np.asarray(pure_img)

        time.sleep(0.5)

        is_color_commmon('green', pure_img)

        #Exibe a imagem
        cv.imshow("OpenCV/Numpy normal", sct_img)

        #print(f"FPS: {1 / (time.time() - last_time)}")


        #Q para sair
        if cv.waitKey(25) & 0xFF == ord("q"):
            cv.destroyAllWindows()
            break


    