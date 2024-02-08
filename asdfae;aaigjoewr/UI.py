import os
import pygame as py
import sys
import math
from urllib.request import urlopen
import re
import requests
from bs4 import BeautifulSoup

start2button = False
right2button = False
left2button = False

titleNum = 0
descNum = 0
ownerNum = 0

py.init()
screenResolution = py.display.Info()
py.display.set_mode((screenResolution.current_w, screenResolution.current_h))
clock = py.time.Clock()
running = True
textGood = False

SCREEN_WIDTH = 1536
SCREEN_HIGHT = 864

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))

bg = py.image.load("images\Background2.png").convert()
loading = py.image.load("images\loading.png").convert()
loading = py.transform.scale(loading, (100, 500))
Start1 = py.image.load("images\Start1.png")
start1 = py.transform.scale(Start1, (310, 140))
Start2 = py.image.load("images\Start2.png")
start2 = py.transform.scale(Start2, (310, 140))

leftUp = py.image.load("images\leftUp.png")
leftUp = py.transform.scale(leftUp, (55, 75))
leftDown = py.image.load("images\leftDown.png")
leftDown = py.transform.scale(leftDown, (55, 75))
rightUp = py.image.load("images\RightUp.png")
rightUp = py.transform.scale(rightUp, (55, 75))
rightDown = py.image.load("images\RightDown.png")
rightDown = py.transform.scale(rightDown, (55, 75))

# worlds smallest web scraper starts here     v v v
url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

titleList = []
ownerList = []
descList = []

for x in soup.find_all("h2"):
    result = x.get_text()
    titleList.append(result)
for x in soup.find_all("p", class_="location"):
    result = x.get_text()
    descList.append(result)
for x in soup.find_all("h3"):
    result = x.get_text()
    ownerList.append(result)

#background width
bg = py.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HIGHT))
bg_width = bg.get_width()

#moving background
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

def buttons(x, y, xLen, yLen):
    button = py.Rect(x, y, xLen, yLen)
    return button

def menu(button1, button2, width, height, buttonReady):
    if buttonReady == True:
        startbutton = screen.blit(button2, (SCREEN_WIDTH/2 + width, SCREEN_HIGHT/2 + height))
    else:
        startbutton = screen.blit(button1, (SCREEN_WIDTH/2 + width, SCREEN_HIGHT/2 + height))

    return(startbutton)


while running == True:
    mouse = py.mouse.get_pos()
    clock.tick(60)
#blit moving screen
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
    scroll -= 0.5

    #reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

            # ----- blit only after this point -----
    menu(start1, start2, int(-155), int(-250), start2button)
    menu(leftUp, leftDown, int(-400 - 27.5), int(+0), left2button)
    menu(rightUp, rightDown, int(+400 - 27.5), int(+0), right2button)


    for event in py.event.get():
        if event.type == py.QUIT: #quit game via X button
            py.quit()
            sys.exit()
        elif event.type == py.KEYDOWN: #quit via esc key
            if event.key == py.K_ESCAPE:
                py.quit()
                sys.exit()
        elif event.type == py.MOUSEBUTTONDOWN: #mouse pressed
            if menu(start1, start2, int(-155), int(-250), start2button).collidepoint(event.pos):
                if textGood == False:
                    textGood = True
                else:
                    textGood = False
                start2button = True
                totalNum = -1
            if menu(leftUp, leftDown, int(-400 - 27.5), int(+0), left2button).collidepoint(event.pos):
                titleNum -= 1
                descNum -= 1
                ownerNum -= 1
                left2button = True
            if menu(rightUp, rightDown, int(+400 - 27.5), int(+0), right2button).collidepoint(event.pos):
                titleNum += 1
                descNum += 1
                ownerNum += 1
                right2button = True

            if titleNum >= len(titleList):#making sure it loops instead of crashing
                titleNum = 0
            if descNum >= len(descList):
                descNum = 0
            if ownerNum >= len(ownerList):
                ownerNum = 0

        elif event.type == py.MOUSEBUTTONUP: #mouse released
            start2button = False
            left2button = False
            right2button = False

        font = py.font.Font("slkscr.ttf", 32)
        textTitle = font.render(titleList[titleNum], True, (255, 255, 255))
        textTitleLocation = textTitle.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HIGHT/2 + 0))

        textOwner = font.render(ownerList[ownerNum], True, (255, 255, 255))
        textOwnerLocation = textOwner.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HIGHT/2 + 40))

        textDesc = font.render(descList[descNum], True, (255, 255, 255))
        textDescLocation = textDesc.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HIGHT/2 + 80))

    if textGood == True:
        screen.blit(textTitle, textTitleLocation)
        screen.blit(textOwner, textOwnerLocation)
        screen.blit(textDesc, textDescLocation)

    py.display.update()