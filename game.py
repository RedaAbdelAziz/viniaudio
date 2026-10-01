import pygame
from pygame.locals import *
import pygame_menu
from pygame import mixer
from typing import Tuple, Any 
from time import sleep
import sys


import youtube_dl
import click


global map
finished = True


pygame.init()
pygame.mixer.init()

FILETYPE = ['.mp3']

screen = pygame.display.set_mode([900 , 900]) 
#background_image = pygame_menu.BaseImage(
#   image_path='Z:\Homework\Pictures\BlueStacks\w1.png'
#)


def start_up():    
    pianoslide = pygame.mixer.Sound('Resources/sound/startup.wav')
    hola = pygame.mixer.Sound('Resources/sound/hardtime.wav')
    pygame.mixer.Channel(1).play(pianoslide)    
    pygame.mixer.Channel(1).queue(hola)


def main_background():
    #background_image.draw(screen)
    pass

def main():
    global main_menu

    main_menu = pygame_menu.Menu(
        onclose=pygame_menu.events.EXIT,
        title='Vini Audio',
        height=900,
        width=900
    )
    mmblabel = main_menu.add.label(
        'Vini Audio',
        background_color='#FFF000',
        background_inflate=(150,0),
        float=True).translate(0,-300)
    
    rhythmgamemenu = pygame_menu.Menu( #rhythm game play 
        onclose=pygame_menu.events.EXIT,
        title='Vini Audio Rhythm Game',
        height=900,
        width=900)
    
    playgame = main_menu.add.button(
        'Play Game', rhythmgamemenu,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10,-235)
    
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################
    ####################################

    def rhythmgame(map):
        pygame.mixer.Channel(1).pause()
        clock = pygame.time.Clock()
        good = pygame.mixer.Sound('Resources/sound/good.wav')
        no = pygame.mixer.Sound('Resources/sound/no.wav')
        combosound = pygame.mixer.Sound('Resources/sound/combo.wav')
        holy = pygame.mixer.Sound('Resources/sound/holy.wav')
        no.set_volume(0.5)

        combo = 0
        score = 0
        finished = False

        pygame.init()
        screen = pygame.display.set_mode((420, 800))
        mixer.init()
        class Key():
            def __init__(self,x,y,color1,color2,key):
                self.x = x
                self.y = y
                self.color1 = color1
                self.color2 = color2
                self.key = key
                self.rect = pygame.Rect(self.x,self.y,100,10)
                self.handled = False

        #now we will make a list of keys

        keys = [
            Key(0,700,(255,0,0),(220,0,0),pygame.K_a),
            Key(105,700,(0,255,0),(0,220,0),pygame.K_s),
            Key(210,700,(0,0,255),(0,0,220),pygame.K_k),
            Key(315,700,(255,255,0),(220,220,0),pygame.K_l),
        ]

        #lets load the map into the game 
        def load(map):
            rects = []
            mixer.music.load("Resources/sound/" + map + ".wav")
            mixer.music.play()
            f = open("Resources/sound/" + map + ".txt", 'r')
            data = f.readlines()

            for y in range(len(data)):
                for x in range(len(data[y])):
                    if data[y][x] == '0':
                        rects.append(pygame.Rect(keys[x].rect.centerx - 25,y * -100,50,25))
            return rects

        map_rect = load(map)
        mapimg = map
        bad_key_press = {pygame.K_a: False, pygame.K_s: False, pygame.K_d: False, pygame.K_f: False}
        while not finished:
            font = pygame.font.Font('freesansbold.ttf', 32)
            showscore = font.render('Score: ' + str(score), True, (0, 0, 128), (255, 255, 255))
            textRect = showscore.get_rect()
            textRect.center = (210, 30)

            

            background = pygame.image.load('Resources/images/' + mapimg + '.png').convert()       
            screen.blit(background, (0, 0)) 
            screen.blit(showscore, textRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True

            #now we will loop through the keys and handle the events
            k = pygame.key.get_pressed()
            for key in keys:
                if k[key.key]:
                    pygame.draw.rect(screen, key.color1, key.rect)
                    key.handled = False

                    # Check if the key was not handled for score subtraction
                    if not bad_key_press[key.key]:
                        has_collision = False
                        for rect in map_rect:
                            if key.rect.colliderect(rect):
                                has_collision = True
                                break

                        if not has_collision:
                            score -= 20
                            bad_key_press[key.key] = True
                else:
                    pygame.draw.rect(screen, key.color2, key.rect)
                    key.handled = True
                    bad_key_press[key.key] = False

                #now when we press our keys they will change color
            for rect in map_rect:
                pygame.draw.rect(screen,(200,0,0),rect)
                rect.y += 6
                for key in keys: 
                    if key.rect.colliderect(rect) and not key.handled:
                        map_rect.remove(rect)
                        good.play()
                        score += 100
                        key.handled = True
                        combo += 1
                        print(combo)
                        break
                    if rect.y == 700:
                        combo = 0
                        score -= 20
                        no.play()
            if (combo == 5):
                combosound.play()
                score += 10
            if (combo == 10):
                holy.play()
                score += 20

                                     


                


            pygame.display.update()
            clock.tick(60)
            if finished == True:
                print(score)
                screen = pygame.display.set_mode([900 , 900])
                pygame.mixer.pause()
                pygame.mixer.music.load('Resources/sound/manhunt.wav')
                start_up()
            
    def beatmap():
        pygame.mixer.Channel(1).pause()
        beatmap = "gruppakrovi"
        mixer.init()
        mixer.music.load("Resources/sound/" + beatmap + ".wav")
        mixer.music.play()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((420, 800))
        background = pygame.image.load('Resources/images/beatmapguide.png').convert()       
        screen.blit(background, (0, 0)) 
        pygame.display.update()   


        created = False
        while not created:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    created = True
            notes = pygame.key.get_pressed()
            

            with open("Resources/sound/" + beatmap + ".txt", mode='a') as f:
                if notes[K_a]:
                    f.write('0   \n')
                if notes[K_s]:
                    f.write(' 0  \n')
                if notes[K_d]:
                    f.write('  0 \n')
                if notes[K_f]:
                    f.write('   0\n')
                if notes[K_z]:
                    f.write('00  \n')
                if notes[K_x]:
                    f.write('0 0 \n')
                if notes[K_c]:
                    f.write('0  0\n')
                if notes[K_v]:
                    f.write(' 00 \n')
                if notes[K_q]:
                    f.write(' 0 0\n') 
                if notes[K_w]:
                    f.write(' 00\n')       
                if notes[K_SPACE]:
                    f.write('0000\n')         
                if notes[K_e]:
                    f.write('\n')                      
        if created == True:
            screen = pygame.display.set_mode([900 , 900])
            pygame.mixer.pause()
            pygame.mixer.music.load('Resources/sound/manhunt.wav')
            start_up()

    def startmanhunt():
        rhythmgame("manhunt")
    def starteuropa():
        rhythmgame("europa")
    def startdarwin():
        rhythmgame("darwin")                                
    def startp4():
        rhythmgame("illfacemyself")     
    def startcloseeyes():
        rhythmgame("closeeyes")       
    def startgruppakrovi():
        rhythmgame("gruppakrovi")       



            







    manhuntheme = rhythmgamemenu.add.button(
        'Manhunt Theme', startmanhunt,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10,-235),
    europaleaguetheme = rhythmgamemenu.add.button(
        'Europa League Theme', starteuropa,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10,-170)
    darwizzy = rhythmgamemenu.add.button(
        'I Need a Nunez', startdarwin,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10,-105)
    p4 = rhythmgamemenu.add.button(
        'Ill Face Myself', startp4,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10,-40)
    closeeyes = rhythmgamemenu.add.button(
        'Close Eyes', startcloseeyes,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10,20)
    gruppakrovis = rhythmgamemenu.add.button(
        'Gruppa Krovi', startgruppakrovi,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10,85)
    






    beatmapcreator = rhythmgamemenu.add.button(
        'Beat Map Creator', beatmap,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10, 200)
    

    def creditsshowcase():
        finished = False
        screen = pygame.display.set_mode((900, 900))
        background = pygame.image.load('Resources/images/credits.png').convert()    
        screen.blit(background, (0, 0))  
        pygame.display.update()   


        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True

    credits = main_menu.add.button(
        'Credits',
        creditsshowcase,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10, -150)
    
    quitgame = main_menu.add.button(
        'Quit',
        pygame_menu.events.EXIT,
        align=pygame_menu.locals.ALIGN_LEFT,
        float=True,
        selection_color='#808080').translate(10,-55)
    
    

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    main()
    start_up()
    main_menu.mainloop(screen, main_background)

pygame.quit()