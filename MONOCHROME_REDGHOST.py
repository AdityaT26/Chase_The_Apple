from time import sleep as slp
import sys
import keyboard as keypress
import random
from threading import Thread
import os
import winsound
import tkinter

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Vars():

    started = False

    '''rows = 32
    columns = 64'''
    rows = 32
    columns = 79

    player = "ᗣ"
    fruit = "@"
    bomb = "█"
    explosion = "▓"

    playarea  = []

    numbombs = 30
    posbombs = []

    posR = 0 
    posC = 0

    posRF = 0 
    posCF = 0

    score = 0

    delay = 0.03

    fixedtime = 5
    timer = fixedtime

    borders = True

    health = 3
    healthrem = 3

    gameover=False

def applecollect():
    winsound.Beep(round(1046.5022612023945), 100)

def bombhit():
    winsound.Beep(round(110), 70)
    winsound.Beep(round(220), 70)
    winsound.Beep(round(440), 70)
    winsound.Beep(round(880), 70)

def starmenusound():
    while not Vars.started:
        winsound.Beep(round(293.6647679174076), 300)
        winsound.Beep(round(659.2551138257398), 300)
        winsound.Beep(round(329.6275569128699), 300)
        winsound.Beep(round(587.3295358348151), 300)

def intro():
    print(color.PURPLE+"*********************************************************************************"+color.END)
    print(color.PURPLE+"*"+color.END+" ***************************************************************************** "+color.PURPLE+"*"+color.END)
    print(color.PURPLE+"#"+color.END+" *                                                                           * "+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+" *                                                                           * "+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+color.CYAN+    " *     =============         =============         =============             * "+color.END+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+color.RED+     " *     [|]       [|]         [|]       [|]         [|]                       * "+color.END+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+color.YELLOW+  " *     [|]       [|]         [|]       [|]         [|]                       * "+color.END+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+color.GREEN+   " *     [|]       [|]         [===========]         [|]                       * "+color.END+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+color.BLUE+    " *     [|]       [|]         []                    [|]    [|][|]             * "+color.END+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+color.CYAN+    " *     [|]       [|]         []                    [|]       [|]             * "+color.END+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+color.RED+     " *     [|]       [|]         []                    [|]       [|]             * "+color.END+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+color.YELLOW+  " *     =============   [o]   []               [o]  =============    [o]      * "+color.END+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+" *                                                                           * "+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"#"+color.END+" *                                                                           * "+color.PURPLE+"#"+color.END)
    print(color.PURPLE+"*"+color.END+" ***************************************************************************** "+color.PURPLE+"*"+color.END)
    print(color.PURPLE+"*********************************************************************************"+color.END)
    print()
    print('*********************************************************************************')
    print("     "+color.DARKCYAN+'©2021-2022'+color.END+'--        '+color.PURPLE+'For Personal Use Only'+color.END+'      --Author:'+color.BOLD+color.YELLOW+'Aditya Thakur'+color.END)
    print('*********************************************************************************')
    print()
    print()

def timer():
    while True:
        if Vars.timer>0:
            slp(1)
            Vars.timer-=1
        else:
            spawnFruit()
            Vars.timer=Vars.fixedtime

def exitCheck():
    while True:
        slp(Vars.delay)
        if keypress.is_pressed('ctrl'):
            if keypress.is_pressed('alt'):
                exit()

def gameoversound():
    slp(0.5)
    winsound.Beep(round(3322.437580639561), 400)
    winsound.Beep(round(3135.9634878539946), 405)
    winsound.Beep(round(2959.9553816930757), 408)
    winsound.Beep(round(2793.825851464031), 412)
    winsound.Beep(round(2637.0204553029594), 416)
    winsound.Beep(round(2489.015869776647), 1000)
    #winsound.Beep(round(2349.31814333926), 400)


def gameover():

    Thread(target = lambda:gameoversound()).start()

    for i in range(Vars.posR+Vars.posC):
        try:
            Vars.playarea[Vars.posR-i][Vars.posC-i] = Vars.explosion
        except:
            pass
        try:
            Vars.playarea[Vars.posR-i][Vars.posC+i] = Vars.explosion
        except:
            pass
        try:
            Vars.playarea[Vars.posR+i][Vars.posC-i] = Vars.explosion
        except:
            pass
        try:
            Vars.playarea[Vars.posR+i][Vars.posC+i] = Vars.explosion
        except:
            pass
        slp(0.1)

    slp(1)

    for i in range(Vars.rows):
        for j in range(Vars.columns):
            Vars.playarea[i][j]=" "

    for i in range(Vars.rows):
        for j in range(Vars.columns):
            Vars.playarea[i][j]=Vars.explosion
        slp(0.01)

    print(color.RED+color.BOLD+"GAME OVER!"+color.END+color.END)
    exit()

def move():
    while True:
        slp(Vars.delay)
        if Vars.posRF == Vars.posR and Vars.posCF == Vars.posC:
            Vars.score +=1
            Vars.timer=Vars.fixedtime
            Thread(target = lambda:applecollect()).start()
            spawnFruit("garbage")
        if (Vars.posR, Vars.posC) in Vars.posbombs:
            Thread(target = lambda:bombhit()).start()
            Vars.posbombs.pop(Vars.posbombs.index((Vars.posR, Vars.posC)))
            Vars.score -=1
            Vars.timer = 0
            Vars.healthrem -= 1
            if Vars.healthrem == 0:
                Vars.gameover=True
                gameover()
        if keypress.is_pressed('left'):
            if Vars.posC>0:
                Vars.playarea[Vars.posR][Vars.posC] = " "
                Vars.posC-=1
                Vars.playarea[Vars.posR][Vars.posC] = Vars.player
        if keypress.is_pressed('right'):
            if Vars.posC<Vars.columns-1:
                Vars.playarea[Vars.posR][Vars.posC] = " "
                Vars.posC+=1
                Vars.playarea[Vars.posR][Vars.posC] = Vars.player
        if keypress.is_pressed('up'):
            if Vars.posR>0:
                Vars.playarea[Vars.posR][Vars.posC] = " "
                Vars.posR-=1
                Vars.playarea[Vars.posR][Vars.posC] = Vars.player
        if keypress.is_pressed('down'):
            if Vars.posR<Vars.rows-1:
                Vars.playarea[Vars.posR][Vars.posC] = " "
                Vars.posR+=1
                Vars.playarea[Vars.posR][Vars.posC] = Vars.player
        if keypress.is_pressed('ctrl'):
            if keypress.is_pressed('d') or keypress.is_pressed('z'):
                if Vars.delay<0.1:
                    Vars.delay += 0.01
                    Vars.delay = round(Vars.delay, 2)
                    slp(0.1)
            if keypress.is_pressed('i') or keypress.is_pressed('x'):
                if Vars.delay>=0.01:
                    Vars.delay -= 0.01
                    Vars.delay = round(Vars.delay, 2)
                    slp(0.1)
            if keypress.is_pressed('b'):
                slp(0.1)
                if Vars.borders:
                    Vars.borders=False
                else:
                    Vars.borders=True

def display(outputWindow):
    i=0
    while True:

        healthstr = " "
        for i in range(Vars.healthrem):
            healthstr+="❤ "

        for i in range(Vars.health-Vars.healthrem):
            healthstr+" "

        s=""
        s+="Score: "+\
        str(Vars.score*100)+\
        " Acceleration: "+str(int(10-Vars.delay*100))+\
        " Time Left for fruit to rot : "+str(Vars.timer)+healthstr+"\n"
        if Vars.borders:
            for i in range(Vars.columns+2):
                s+="*"
            s+="\n"
        else:
            for i in range(Vars.columns+2):
                s+=" "
            s+="\n"
        for i in range(Vars.rows):
            if Vars.borders:
                s+="*"
            else:
                s+=" "
            for j in range(Vars.columns):
                s+=Vars.playarea[i][j]
            if Vars.borders:
                s+="*\n"
            else:
                s+=" \n"
        if Vars.borders:
            for i in range(Vars.columns+2):
                s+="*"
            s+="\n"
        else:
            for i in range(Vars.columns+2):
                s+=" "
            s+="\n"
        #outputWindow.config(text=s)
        outputWindow.insert("1.0", s)
        outputWindow.tag_add("player", str(Vars.posR+3)+"."+str(Vars.posC+1), str(Vars.posR+3)+"."+str(Vars.posC+2))
        outputWindow.tag_config("player", background="beige", foreground="red")
        
        if i>=2:
            outputWindow.delete(str(Vars.rows+4)+".0", tkinter.END)
        else:
            i+=1

def debugScore():
    try:
        h=open("debugscore.txt", "r")
        Vars.score = int(h.readline())
        h.close()
    except:
        pass

def generatePos():

    posR = random.randint(0, Vars.rows-1)
    posC = random.randint(0, Vars.columns-1)

    return posR, posC


def initialisePlayGround(rows, columns):

    for i in range(rows):
        Vars.playarea.append([])
        for j in range(columns):
            Vars.playarea[i].append(" ")

def spawnPlayer():

    Vars.posR, Vars.posC = generatePos()

    Vars.playarea[Vars.posR][Vars.posC] = Vars.player

def spawnBombs():

    for i in range(Vars.numbombs):
        posBR, posBC = generatePos()
        Vars.playarea[posBR][posBC] = Vars.bomb
        Vars.posbombs.append((posBR, posBC))

def spawnFruit(*args):

    if(Vars.gameover==False):
        if len(args)>0:
            Vars.playarea[Vars.posRF][Vars.posCF] = Vars.player
        else:
            Vars.playarea[Vars.posRF][Vars.posCF] = " "

        while True:
            Vars.posRF, Vars.posCF = generatePos()
            if (Vars.posRF, Vars.posCF) not in Vars.posbombs:
                break

        Vars.playarea[Vars.posRF][Vars.posCF] = Vars.fruit
        

def gameStart(outputWindow):
    sys.stdout.write('\rLoading 01.')
    slp(0.5)
    sys.stdout.write('\rLoading 02..')
    slp(0.5)
    sys.stdout.write('\rLoading 03...')
    print()
    spawnPlayer()
    spawnBombs()
    spawnFruit()

    Thread(target= lambda:move()).start()
    Thread(target= lambda:timer()).start()
    Thread(target= lambda:display(outputWindow)).start()

def exit():
    os._exit(0)

def main():

    root = tkinter.Tk()

    Thread(target= lambda:exitCheck()).start()

    initialisePlayGround(Vars.rows, Vars.columns)

    intro()

    Thread(target= lambda:starmenusound()).start()

    input("Press enter to start : ")

    Vars.started=True

    root.minsize(750, 750)
    root.resizable(0, 0)
    outputWindow = tkinter.Text(root)
    outputWindow.config(relief=tkinter.SUNKEN, bg='beige', font=("Cascadia Mono", 12))
    outputWindow.place(x=0, y=0, relheight=1, relwidth=1)   

    gameStart(outputWindow)
    root.mainloop() 

os.system('')

main()


