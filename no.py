# Pyxel Studio

import pyxel
import random
import json

pyxel.init(128, 128, fps=30)
pyxel.load("no.pyxres")

vaisseau_x = 60
vaisseau_y = 60

TOUCHE_TIR = pyxel.KEY_SPACE
GAMEPAD_TIR = pyxel.GAMEPAD1_BUTTON_B

vies = 4

munition = 10

tirs_liste = []

ennemis_liste = []

explosions_liste = []

points = 0

vitesse_ennemi = 1

etoiles = [[random.randint(0, 127), random.randint(0, 127), random.choice([7, 13, 9, 10, 5, 6])] for _ in range(80)]


def play_music():
    with open(f"music.json", "rt") as fin:
        music = json.loads(fin.read())

    for ch, sound in enumerate(music):
        s = pyxel.Sound()
        s.set(*sound)
        pyxel.sounds[ch] = s
        pyxel.play(ch, ch, loop=True)

play_music()

def deplacement_etoiles():
    global etoiles
    for i in range(len(etoiles)):
        if etoiles[i][2] == 7 or etoiles[i][2] == 6 or etoiles[i][2] == 10:
            etoiles[i][1] = etoiles[i][1] + 2
        elif etoiles[i][2] == 13 or etoiles[i][2] == 9 or etoiles[i][2] == 5:
            etoiles[i][1] = etoiles[i][1] + 1
    n = 0
    for e in etoiles:
        if e[1] > 128:
            etoiles.remove(e)
            n += 1
    for i in range (n):
        etoiles.append([random.randint(0, 127), 0, random.choice([7, 13, 9, 10, 5, 6])])

def vaisseau_deplacement(x, y):
    global munition
    if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
        if x < 120:
            x = x + 1
    if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
        if x > 0:
            x = x - 1
    if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
        if y < 120:
            y = y + 1
    if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
        if y > 0:
            y = y - 1
    if pyxel.btn(pyxel.KEY_R) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
        munition = 10

    return x, y

def vaisseau_suppression(vies):

    for ennemi in ennemis_liste:
        if ennemi[0] <= vaisseau_x+8 and ennemi[1] <= vaisseau_y+8 and ennemi[0]+8 >= vaisseau_x and ennemi[1]+8 >= vaisseau_y:
           ennemis_liste.remove(ennemi)
           vies -= 1
    return vies
            
def ennemis_suppression():
    global points
    for ennemi in ennemis_liste:
        for tir in tirs_liste:
            x_tir = tir[0]
            y_tir = tir[1]
            x_ennemi = ennemi[0]
            y_ennemi = ennemi[1]
            if x_ennemi - 8 < x_tir < x_ennemi+8 and y_tir < y_ennemi+8:
                ennemis_liste.remove(ennemi)
                tirs_liste.remove(tir)
                explosions_creation(x_ennemi, y_ennemi)
                points += 1


def tirs_creation(x, y, tirs_liste):
    global munition
    if munition > 0:
        if pyxel.btnp(TOUCHE_TIR, repeat=15) or pyxel.btnp(GAMEPAD_TIR, repeat=15):
            tirs_liste.append([x, y-4])
            munition -= 1
    return tirs_liste

def tirs_deplacement(tirs_liste):
    for tir in tirs_liste:
        tir[1] -= 1
        if tir[1]<-8:
            tirs_liste.remove(tir)
    return tirs_liste

def ennemis_creation(ennemis_liste):
    if pyxel.frame_count % 30 == 0:
        ennemis_liste.append([random.randint(0, 120), 0])
    return ennemis_liste

def ennemis_deplacement(ennemis_liste):
    for ennemi in ennemis_liste:
        ennemi[1] += vitesse_ennemi
        if ennemi[1]>128:
           ennemis_liste.remove(ennemi)
    return ennemis_liste

def explosions_creation(x, y):
    explosions_liste.append([x, y, 0])

def explosions_animation():
    for explosion in explosions_liste:
        explosion[2] += 1
        if explosion[2] == 12:
            explosions_liste.remove(explosion)

def update():
    global vaisseau_x, vaisseau_y, tirs_liste, ennemis_liste ,vies, explosions_liste, points, vitesse_ennemi



    if pyxel.frame_count % 900 == 0:
        points =points+10
        vitesse_ennemi = vitesse_ennemi+0.5

    deplacement_etoiles()

    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)

    tirs_liste = tirs_creation(vaisseau_x, vaisseau_y, tirs_liste)

    tirs_liste = tirs_deplacement(tirs_liste)

    ennemis_liste = ennemis_creation(ennemis_liste)

    ennemis_deplacement(ennemis_liste)

    ennemis_suppression()

    vies = vaisseau_suppression(vies)

    explosions_animation()


def draw():
    pyxel.cls(0)

    if vies > 0:

        for e in etoiles:
            x_etoile = e[0]
            y_etoile = e[1]
            col = e[2]
            pyxel.rect(x_etoile, y_etoile, 1, 1, col)

        pyxel.text(5, 5, 'VIES:'+ str(vies), 7)

        pyxel.text(128-40, 5, 'POINTS:' + str(points), 7)

        pyxel.blt(40,2.5, 0, 8, 0, 8, 8, 0)
        pyxel.text(50, 5, str(munition), 7)

        if munition == 0:
            pyxel.text(vaisseau_x-10,vaisseau_y+10, 'RELOAD', pyxel.COLOR_RED)

        pyxel.blt(vaisseau_x, vaisseau_y, 0, 0,0 , 8, 8, 0)

        for tir in tirs_liste:
            pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8, 0)

        for ennemi in ennemis_liste:
            pyxel.blt(ennemi[0], ennemi[1], 0, 0, 8, 8, 8, 0)

        for explosion in explosions_liste:
            pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)
    else:
        pyxel.text(50, 64, 'GAME OVER', 7)
        pyxel.text(50, 74, 'SCORE :' +str(points) , 7)

pyxel.run(update, draw)


