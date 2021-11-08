import pygame
import sys
import os
import getopt
from pygame import color
from pygame.locals import *
from socket import *
import constants as const


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        # raise SystemExit, message
    return image, image.get_rect() #returns both the image and the rectangle




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image, self.rect = load_png('player.png') #loads both the image and the rectangle

        self.standbyPos = (const.SCREENHEIGHT-self.rect[3])/2 
        self.downPos = self.standbyPos+const.SCREENHEIGHT/4
        self.upPos = self.standbyPos-const.SCREENHEIGHT/4

        self.state = "center"
        self.cooldown = -1 #player cooldown: time for pos reset to standby y
        self.rect[1] = self.standbyPos #y


    def update(self):
        # print(self.cooldown)
        self.cooldown += -1
        if 0 < self.cooldown < const.PLAYER_COOLDOWN: 
            if self.state=="center":
                self.rect[1]= self.standbyPos
            elif self.state=="up":
                self.rect[1]= self.upPos
            elif self.state=="down":
                self.rect[1]= self.downPos
        elif self.cooldown < 0:
            self.state = "center"
            self.rect[1]= self.standbyPos


    def isActive(self): #time after key press when the player can catch bullets
        if self.cooldown>(const.PLAYER_COOLDOWN-const.PLAYER_ACTIVE_FRAMES): return True

    def moveup(self):
        self.state="up"
        self.cooldown=const.PLAYER_COOLDOWN

    def movedown(self):
        self.state="down"
        self.cooldown=const.PLAYER_COOLDOWN




class Bullet(pygame.sprite.Sprite):
    def __init__(self, bType,t):
        super().__init__()
        #self.image, self.rect = load_png('intro_ball.gif') #loads both the image and the rectangle
        self.bType = bType
        self.position = 800 + t #position = timing + screen width
        if bType == 'up':
                self.image, self.rect = load_png('bullet_top.png') #loads both the image and the rectangle
                tmp = (const.SCREENHEIGHT-self.rect[3])/2
                self.rect[1] = tmp-const.SCREENHEIGHT/4
        elif bType == 'down':
                self.image, self.rect = load_png('bullet_bottom.png') #loads both the image and the rectangle
                tmp = (const.SCREENHEIGHT-self.rect[3])/2                
                self.rect[1] = tmp+const.SCREENHEIGHT/4


    def update(self):
        self.position = self.position - const.BULLET_VELOCITY
        self.rect[0] = self.position #float to int conversion




class ScoreCounter():
    pass




class CollisionDetector(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cooldown = 0
        self.state = 'null'
        self.missImg, self.missRect = load_png('miss.png')
        self.hitImg, self.hitRect = load_png('pass.png')
        self.missRect[0] = const.SCREENWIDTH/2
        self.hitRect[0] = const.SCREENWIDTH/2

        self.nullRect = Rect(const.SCREENWIDTH*2,0,0,0)


    def update(self):
        self.cooldown = self.cooldown -1
        if self.cooldown<0 : self.state = 'null'


    def detectCollisions(self,player,bulletList):
        self.update()
        # for b in bulletList:
        b = bulletList[0]
        if b.position<-1:
            self.cooldown = const.HITMISS_TIMEONSCREEN
            self.state = 'miss'
            bulletList.remove(b)
            return #miss
        if player.isActive():
            if 10<b.position<100 and b.bType == player.state:
                bulletList.remove(b)
                # print('test')
                self.cooldown = const.HITMISS_TIMEONSCREEN
                self.state = 'hit'
                return #success
        # if b.position<-10: #cleaning bullet list, not necessary
        #     bulletList.remove(b)
        return


    def get_hit_miss_images(self):
        if self.state == 'hit':
            return self.hitImg, self.hitRect
        if self.state == 'miss':
            return self.missImg, self.missRect
        if self.state == 'null':
            return self.hitImg, self.nullRect