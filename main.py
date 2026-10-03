import random
import pygame
import sys

WIDTH = 900
HIGHT = 600

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH,HIGHT))

        self.game_over = pygame.image.load("Assets/Other/GameOver.png")
        self.game_return = pygame.image.load("Assets/Other/Reset.png")

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

        self.cactus_images = [
            pygame.transform.scale(pygame.image.load("Assets/Cactus/LargeCactus1.png"),(30,80)),
            pygame.transform.scale(pygame.image.load("Assets/Cactus/LargeCactus2.png"),(50,80)),
            pygame.transform.scale(pygame.image.load("Assets/Cactus/LargeCactus3.png"),(60,80)),
            pygame.transform.scale(pygame.image.load("Assets/Cactus/SmallCactus1.png"),(30,80)),
            pygame.transform.scale(pygame.image.load("Assets/Cactus/SmallCactus2.png"),(60,80)),
            pygame.transform.scale(pygame.image.load("Assets/Cactus/SmallCactus3.png"),(70,80))
        ]

        self.bird_images = {
            "Bird1" : pygame.transform.scale(pygame.image.load("Assets/Bird/Bird1.png"),(70,70)),
            "Bird2" : pygame.transform.scale(pygame.image.load("Assets/Bird/Bird2.png"),(70,70)),
        }

        self.dino_x = 40
        self.dino_y = 440

        self.bird_x = 1100
        self.bird_y = 70

        self.cactus_x = 1100
        self.cactus_y = 430
        self.cactus = self.cactus_images[0]

        self.font_small = pygame.font.Font("Assets/Font/Pixeltype.ttf",40)

        self.sound_over = pygame.mixer.Sound("Assets/audio/over.mp3")
        self.sound_jump = pygame.mixer.Sound("Assets/audio/jump.mp3")
        self.sound_jump.set_volume(0.1)
        pygame.mixer_music.load("Assets/audio/music.mp3")

        self.state = "menu"
        self.frame = 0
        self.jump = "no"
        self.gravity = 5
        self.point = 0
        self.point_added = False
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

                for i in range(5):
                    self.screen.blit(self.cactus_images[0],(i*200+50,20))
                    self.screen.blit(self.cactus_images[3],(i*200+30,500))

                for i in range(3):
                    if i==1:
                        continue
                    self.screen.blit(self.cactus_images[2],(i*200+230,140))
                    self.screen.blit(self.cactus_images[4],(i*200+230,350))
                
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.rect_play.collidepoint(event.pos):
                            self.state = "play"
                            self.frame = 0
                            pygame.mixer_music.play(-1)
                        elif self.rect_quit.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()                      

                pygame.display.update()

            while self.state=="play":
                self.screen.fill("#ffffff")

                if self.jump=="no":
                    self.dino = self.dino_images["DinoRun1"] if (self.frame//10)%2==0 else self.dino_images["DinoRun2"]
                elif self.jump=="up":
                    self.dino = self.dino_images["DinoJump"]
                    if self.dino_y >= 200:
                        self.dino_y = self.dino_y - self.gravity - 5
                    else:
                        self.jump="down"
                elif self.jump=="down":
                    self.dino = self.dino_images["DinoJump"]
                    if self.dino_y <= 435:
                        self.dino_y = self.dino_y + self.gravity + 5
                    else:
                        self.jump="no"

                self.screen.blit(self.dino,(self.dino_x,self.dino_y))
                
                self.screen.blit(self.track,(self.track_x1,500))
                self.screen.blit(self.track,(self.track_x2,500))

                self.bird = self.bird_images["Bird1"] if (self.frame//10)%2==0 else self.bird_images["Bird2"]
                self.screen.blit(self.bird,(self.bird_x,self.bird_y))

                self.screen.blit(self.cactus,(self.cactus_x,self.cactus_y))

                self.text_point = self.font_small.render("Your Point : "+str(self.point),False,"black")
                self.screen.blit(self.text_point,(30,30))

                self.track_x1 -= 4
                self.track_x2 -= 4

                if self.track_x1 <= -WIDTH:
                    self.track_x1 = self.track_x2 + WIDTH

                if self.track_x2 <= -WIDTH:
                    self.track_x2 = self.track_x1 + WIDTH

                if self.point>=3 and self.bird_x > -13:
                    self.bird_x -= 5
                else:
                    self.bird_x = 1100

                if self.cactus_x > -30:
                        self.cactus_x -= 4
                else:
                    self.cactus_x = 1100
                    self.point_added = False
                    self.cactus = random.choice(self.cactus_images)

                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()       
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE and self.jump=="no":
                            self.jump = "up"
                            self.sound_jump.play(0)

                
                dino_rect = self.dino.get_rect(topleft=(self.dino_x, self.dino_y))
                cactus_rect = self.cactus.get_rect(topleft=(self.cactus_x, self.cactus_y))

                if dino_rect.colliderect(cactus_rect):
                    self.dino=self.dino_images["DinoDead"]
                    pygame.mixer_music.stop()
                    self.sound_over.play(0)
                    self.state = "over" 

                if self.cactus_x <= -10 and not self.point_added:
                    self.point += 1
                    self.point_added = True
                        
                self.clock.tick(80)
                pygame.display.update()  
                self.frame += 1     

            while self.state=="over":
                self.screen.fill("#ffffff")

                self.screen.blit(self.dino,(self.dino_x,self.dino_y))
                
                self.screen.blit(self.track,(self.track_x1,500))
                self.screen.blit(self.track,(self.track_x2,500))

                self.screen.blit(self.game_over,(250,150))

                self.game_return_rect = self.game_return.get_rect(topleft=(400,230))
                self.screen.blit(self.game_return,self.game_return_rect)

                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()     
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.game_return_rect.collidepoint(event.pos):
                            self.sound_over.stop()
                            self.state = "play"
                            self.point = 0
                            self.frame = 0
                            self.dino_x = 40
                            self.dino_y = 440
                            self.bird_x = 1100
                            self.cactus_x = 1100
                            self.cactus = self.cactus_images[0]
                            self.track_x1 = 0
                            self.track_x2 = WIDTH
                            self.jump = "no"
                            pygame.mixer_music.play(-1)

                pygame.display.update() 
                
Game().run()