import random
import pygame
import sys

WIDTH = 900
HIGHT = 600

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH,HIGHT))

        self.track = pygame.image.load("Assets/Other/Track.png")
        self.track = pygame.transform.scale(self.track,(WIDTH,20))
        self.track_x1 = 0
        self.track_x2 = WIDTH

        self.cloud = pygame.image.load("Assets/Other/Cloud.png")
        self.cloud = pygame.transform.scale(self.cloud,(WIDTH,20))

        self.dino_images = {
            "DinoDuck1" : pygame.transform.scale(pygame.image.load("Assets/Dino/DinoDuck1.png"),(70,70)),
            "DinoDuck2" : pygame.transform.scale(pygame.image.load("Assets/Dino/DinoDuck2.png"),(70,70)),
            "DinoJump" : pygame.transform.scale(pygame.image.load("Assets/Dino/DinoJump.png"),(70,70)),
            "DinoRun2" : pygame.transform.scale(pygame.image.load("Assets/Dino/DinoRun2.png"),(70,70)),
            "DinoRun1" : pygame.transform.scale(pygame.image.load("Assets/Dino/DinoRun1.png"),(70,70)),
            "DinoDead" : pygame.transform.scale(pygame.image.load("Assets/Dino/DinoDead.png"),(70,70)),
            "DinoStart" : pygame.transform.scale(pygame.image.load("Assets/Dino/DinoStart.png"),(70,70))
        }

        self.cactus_images = {
            "LargeCactus1" : pygame.transform.scale(pygame.image.load("Assets/Cactus/LargeCactus1.png"),(70,70)),
            "LargeCactus2" : pygame.transform.scale(pygame.image.load("Assets/Cactus/LargeCactus2.png"),(70,70)),
            "LargeCactus3" : pygame.transform.scale(pygame.image.load("Assets/Cactus/LargeCactus3.png"),(70,70)),
            "SmallCactus1" : pygame.transform.scale(pygame.image.load("Assets/Cactus/SmallCactus1.png"),(70,70)),
            "SmallCactus2" : pygame.transform.scale(pygame.image.load("Assets/Cactus/SmallCactus2.png"),(70,70)),
            "SmallCactus3" : pygame.transform.scale(pygame.image.load("Assets/Cactus/SmallCactus3.png"),(70,70))
        }

        self.bird_images = {
            "Bird1" : pygame.transform.scale(pygame.image.load("Assets/Bird/Bird1.png"),(70,70)),
            "Bird2" : pygame.transform.scale(pygame.image.load("Assets/Bird/Bird2.png"),(70,70)),
        }

        self.dino_x = 40
        self.dino_y = 450
        self.bird_x = 1100
        self.bird_y = 40

        self.font_small = pygame.font.Font("Assets/Font/Pixeltype.ttf",40)

        self.state = "menu"
        self.frame = 0
        self.jump = False
        self.point = 0
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            while self.state=="menu":
                self.screen.fill("#ffffff")

                self.rect_play = pygame.Rect(WIDTH/2-50 , HIGHT/2-50, 100 , 40)
                self.rect_quit = pygame.Rect(WIDTH/2-50 , HIGHT/2 , 100 , 40)

                pygame.draw.rect(self.screen,"black",self.rect_play,2,10)
                pygame.draw.rect(self.screen,"black",self.rect_quit,2,10)

                self.text_play = self.font_small.render("PLAY",False,"black")
                self.text_quit = self.font_small.render("QUIT",False,"black")

                self.screen.blit(self.text_play,(WIDTH/2-30 , HIGHT/2-40))
                self.screen.blit(self.text_quit,(WIDTH/2-30 , HIGHT/2+10))
                
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.rect_play.collidepoint(event.pos):
                            self.state = "play"
                            self.frame = 0
                        elif self.rect_quit.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()                      

                pygame.display.update()

            while self.state=="play":
                self.screen.fill("#ffffff")

                self.track_x1 -= 4
                self.track_x2 -= 4

                if self.track_x1 <= -WIDTH:
                    self.track_x1 = self.track_x2 + WIDTH

                if self.track_x2 <= -WIDTH:
                    self.track_x2 = self.track_x1 + WIDTH

                self.screen.blit(self.track,(self.track_x1,500))
                self.screen.blit(self.track,(self.track_x2,500))

                self.dino = self.dino_images["DinoRun1"] if (self.frame//10)%2==0 else self.dino_images["DinoRun2"]
                self.screen.blit(self.dino,(self.dino_x,self.dino_y))

                self.bird = self.bird_images["Bird1"] if (self.frame//10)%2==0 else self.bird_images["Bird2"]
                self.screen.blit(self.bird,(self.bird_x,self.bird_y))

                if self.point>10 and self.bird_x > -10:
                    self.bird_x -= 4
                else:
                    self.bird_x = 1100

                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()       

                self.clock.tick(80)
                pygame.display.update()  
                self.frame += 1     
                
Game().run()