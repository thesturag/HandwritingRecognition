import pygame, sys, os
from pygame.locals import *


class Main():

    def outputToFile(self,pix):
        if os.path.exists("output.txt"):
            os.remove("output.txt")
        with open("output.txt",'a') as o:
            for px in pix:
                o.write(str(px) + "\n")
            o.close()

    def getPixels(self):
        x = 0
        pix = []
        print "start"
        while x < 1080:
            y = 0
            pixy = []
            while y < 720:
                pic = self.screen.get_at((x,y))
                pixy.append(pic)
                y += 1
            pix.append(pixy)
            x += 1
        print "done"
        return pix

    def findBlack(self):
        pix = self.getPixels()
        x = 0
        self.black = (0, 0, 0, 255)
        blk = []
        while x < 1080:
            y = 0
            blky = []
            while y < 720:
                if(pix[x][y] == self.black):
                    blky.append(1)
                else:
                    blky.append(0)
                y += 1
            x += 1
            blk.append(blky)
        return blk 
    
    #Extraction *logic error
    def noMoreBlack(self,blk,x,y,mode):
        print "x = " + str(x)
        print "y = " + str(y)
        if mode == 0:
            print "Y's"
            while y < 720:
                if blk[x][y] == 1:
                    return False
                y += 1
            return True
        else:
            print "X's"
            while x < 1080:
                if blk[x][y] == 1:
                    return False
                x += 1
            return True
        return True
    
    def extractCharacters(self, blk):
        left = []
        right = []
        top = []
        bottom = []
        x = 0
        inBlack = False
        while x < 1080:
            y = 0
            while y < 720:
                if blk[x][y] == 1:
                    if inBlack == False:
                        left.append(x)
                        y = 720
                        inBlack = True
                else:
                    if inBlack:
                        if self.noMoreBlack(blk,x,y,0):
                            right.append(x-1)
                            inBlack = False
                        y = 720
                y += 1
            x += 1
        y = 0
        inBlack = False
        while y < 720:
            x = 0
            while x < 1080:
                if blk[x][y] == 1:
                    if inBlack == False:  
                        top.append(y)
                        x = 1080
                        inBlack = True
                else:
                    if inBlack:
                        if self.noMoreBlack(blk,x,y,1):
                            bottom.append(y-1)
                            inBlack = False
                        x = 1080
                x += 1
            y += 1
        print left
        print right
        print top
        print bottom
        return "Finished"            
    #End extraction          
          
    def plotPixels(self, pos):
        pygame.draw.rect(self.screen, (0,0,0), Rect((pos[0]-2,pos[1]-2),(4,4)))

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.plotPixels(event.pos)
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.outputToFile(self.extractCharacters(self.findBlack()))
                elif event.key == K_SPACE:
                    self.screen.fill((255,255,255))

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080,720),0,0)
        self.screen.fill((255,255,255))
        pygame.display.flip()

    def __init__(self):
        self.initialize()
        while True:
            self.events()
            pygame.display.flip()

Main()