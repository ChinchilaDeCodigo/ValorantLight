import cv2 as cv

import mss
import pyautogui
import numpy as np

#Obter o tamanho da tela
width, height = pyautogui.size()

#Medidas da tela divididas em 4 - a ideia não é capturar a tela toda, apenas a região do centro
smallwidth = int(width/4)
smallheight = int(height/4)

#Imagem
img = None

#Tamanho da captura
screenshot = {"top": smallheight, "left": smallwidth, "width": smallwidth * 2, "height": smallheight}

with mss.mss() as sct:
    #Nome da imagem
    output = "sct-{top}x{left}_{width}x{height}.png".format(**screenshot)

    #Captura a imagem
    sct_img = sct.grab(screenshot)

    #Salva a imagem
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)
    