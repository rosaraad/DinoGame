import random
import pygame
import sys
from datetime import datetime

WIDTH = 1000
HEIGHT = 700

class Game:
    def __init__(self):
        pygame.init()

        # Create the game window
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))

        # Load game over images
        self.game_over = pygame.image.load("Assets/Other/GameOver.png")
        self.game_return = pygame.image.load("Assets/Other/Reset.png")

        # Load and resize the track
        self.track = pygame.image.load("Assets/Other/Track.png")
        self.track = pygame.transform.scale(self.track,(WIDTH,20))
        self.track_x1 = 0
        self.track_x2 = WIDTH

        # Place clouds outside the screen
        self.cloud = pygame.image.load("Assets/Other/Cloud.png")
        self.cloud_rect_1 = self.cloud.get_rect(bottomleft=(1500,260))
        self.cloud_rect_2 = self.cloud.get_rect(bottomleft=(2000,300))

        # Load all dino animations
        self.dino_images = {
            "DinoDuck1" : pygame.image.load("Assets/Dino/DinoDuck1.png"),
            "DinoDuck2" : pygame.image.load("Assets/Dino/DinoDuck2.png"),
            "DinoJump" : pygame.image.load("Assets/Dino/DinoJump.png"),
            "DinoRun2" : pygame.image.load("Assets/Dino/DinoRun2.png"),
            "DinoRun1" : pygame.image.load("Assets/Dino/DinoRun1.png"),
            "DinoDead" : pygame.image.load("Assets/Dino/DinoDead.png"),
            "DinoStart" : pygame.image.load("Assets/Dino/DinoStart.png")
        }

        # Store all cactus images in a list
        self.cactus_images = [
            pygame.image.load("Assets/Cactus/LargeCactus1.png"),
            pygame.image.load("Assets/Cactus/LargeCactus2.png"),
            pygame.image.load("Assets/Cactus/LargeCactus3.png"),
            pygame.image.load("Assets/Cactus/SmallCactus1.png"),
            pygame.image.load("Assets/Cactus/SmallCactus2.png"),
            pygame.image.load("Assets/Cactus/SmallCactus3.png")
        ]

        # Load the two bird animation frames
        self.bird_images = {
            "Bird1" : pygame.image.load("Assets/Bird/Bird1.png"),
            "Bird2" : pygame.image.load("Assets/Bird/Bird2.png"),
        }

        # Set the dino's starting position
        self.dino_x = 40
        self.dino_y = 550

        # Obstacles start outside the screen
        self.bird_x = 1100
        self.bird_y = 470

        self.cactus_x = 1100
        self.cactus_y = 550
        self.cactus = self.cactus_images[0]

        # Create the fonts
        self.font_small = pygame.font.Font("Assets/Font/Pixeltype.ttf",40)
        self.font_made = pygame.font.SysFont("Arial", 18)
        self.text_made = self.font_made.render("Made by rosaraad", True, "#777777")

        # Load game sounds
        self.sound_over = pygame.mixer.Sound("Assets/audio/over.mp3")
        self.sound_jump = pygame.mixer.Sound("Assets/audio/jump.mp3")
        self.sound_jump.set_volume(0.1)
        pygame.mixer_music.load("Assets/audio/music.mp3")

        # Set the initial game state
        self.state = "menu"
        self.frame = 0
        self.jump = "no"
        self.duck = False
        self.gravity = 5
        self.point = 0

        # Prevent the same cactus from giving points twice
        self.point_added = False

        # Control the game FPS
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            #-------------------------Menu-------------------------
            if self.state=="menu":
                self.screen.fill("#ffffff")

                # Create the Play and Quit buttons
                self.rect_play = pygame.Rect(WIDTH/2-50 , HEIGHT/2-50, 100 , 40)
                self.rect_quit = pygame.Rect(WIDTH/2-50 , HEIGHT/2 , 100 , 40)

                pygame.draw.rect(self.screen,"black",self.rect_play,2,10)
                pygame.draw.rect(self.screen,"black",self.rect_quit,2,10)

                self.text_play = self.font_small.render("PLAY",False,"black")
                self.text_quit = self.font_small.render("QUIT",False,"black")

                self.screen.blit(self.text_play,(WIDTH/2-30 , HEIGHT/2-40))
                self.screen.blit(self.text_quit,(WIDTH/2-30 , HEIGHT/2+10))

                # Add cacti to the menu background
                for i in range(5):
                    if i%2==0:
                        self.screen.blit(self.cactus_images[0],(i*200+70,40))
                        self.screen.blit(self.cactus_images[0],(i*200+70,550))
                    else:
                        self.screen.blit(self.cactus_images[0],(i*200+70,20))
                        self.screen.blit(self.cactus_images[0],(i*200+70,600))

                for i in range(3):
                    if i==1:
                        continue
                    self.screen.blit(self.cactus_images[2],(i*200+260,200))
                    self.screen.blit(self.cactus_images[2],(i*200+260,400))
                
                # Handle menu events
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

                made_rect = self.text_made.get_rect(bottomright=(WIDTH - 15, HEIGHT - 10))
                self.screen.blit(self.text_made, made_rect)           
                pygame.display.update()
                self.clock.tick(60)

            #-------------------------Play-------------------------
            elif self.state=="play":
                self.screen.fill("#ffffff")

                # Choose the dino animation
                if self.jump=="no" and not self.duck:
                    self.dino = self.dino_images["DinoRun1"] if (self.frame//10)%2==0 else self.dino_images["DinoRun2"]
                elif self.jump=="no" and self.duck:
                    self.dino = self.dino_images["DinoDuck1"] if (self.frame//10)%2==0 else self.dino_images["DinoDuck2"]
                elif self.jump=="up":
                    self.dino = self.dino_images["DinoJump"]
                    if self.dino_y >= 280:
                        self.dino_y = self.dino_y - self.gravity - 3
                    else:
                        self.jump="down"
                elif self.jump=="down":
                    self.dino = self.dino_images["DinoJump"]
                    if self.dino_y <= 547:
                        self.dino_y = self.dino_y + self.gravity + 3
                    else:
                        self.jump="no"

                # Draw the clouds
                self.screen.blit(self.cloud,self.cloud_rect_1)
                self.screen.blit(self.cloud,self.cloud_rect_2)

                # Draw the moving track
                self.screen.blit(self.track,(self.track_x1,540))
                self.screen.blit(self.track,(self.track_x2,540))

                # Create the dino's collision rectangle
                self.dino_rect = self.dino.get_rect(bottomleft = (self.dino_x,self.dino_y))
                self.screen.blit(self.dino,self.dino_rect)

                # Create the bird's frame and collision rectangle
                self.bird = self.bird_images["Bird1"] if (self.frame//10)%2==0 else self.bird_images["Bird2"]
                self.bird_rect = self.bird.get_rect(bottomleft = (self.bird_x,self.bird_y))
                self.screen.blit(self.bird,self.bird_rect)

                # Create the cactus collision rectangle
                self.cactus_rect = self.cactus.get_rect(bottomleft = (self.cactus_x,self.cactus_y))
                self.screen.blit(self.cactus,self.cactus_rect)

                # Show the current score
                self.text_point = self.font_small.render("Your Point : "+str(self.point),False,"black")
                self.screen.blit(self.text_point,(30,30))

                # Show the current FPS
                fps = int(self.clock.get_fps())
                fps_text = self.font_small.render(f"FPS: {fps}", False, "black")
                self.screen.blit(fps_text, (870, 30))

                # Move the track
                self.track_x1 -= 4
                self.track_x2 -= 4

                # Reset the track when it leaves the screen
                if self.track_x1 <= -WIDTH:
                    self.track_x1 = self.track_x2 + WIDTH

                if self.track_x2 <= -WIDTH:
                    self.track_x2 = self.track_x1 + WIDTH

                # Make the bird appear after 3 points
                if self.point>=3 and self.bird_x > -13:
                    self.bird_x -= 5
                else:
                    self.bird_x = 1100

                # Move the cactus and reset it when it leaves
                if self.cactus_x > -30:
                        self.cactus_x -= 4
                else:
                    self.cactus_x = 1100
                    self.point_added = False
                    self.cactus = random.choice(self.cactus_images)

                # Move the first cloud
                if self.cloud_rect_1.x > -50:
                        self.cloud_rect_1.x -= 4
                else:
                    self.cloud_rect_1.x = 1100

                # Move the second cloud
                if self.cloud_rect_2.x > -70:
                        self.cloud_rect_2.x -= 4
                else:
                    self.cloud_rect_2.x = 1500

                # Handle keyboard input
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()       
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE and self.jump=="no":
                            self.jump = "up"
                            self.sound_jump.play(0)

                # Check if the Down key is pressed
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    self.duck = True
                else:
                    self.duck = False

                # Check for collisions
                if self.dino_rect.colliderect(self.cactus_rect) or self.dino_rect.colliderect(self.bird_rect):
                    self.dino=self.dino_images["DinoDead"]
                    pygame.mixer_music.stop()
                    self.sound_over.play(0)
                    self.state = "over" 

                    # Finding the best point
                    with open("points.txt","+a") as file:
                        now = datetime.now()
                        file.write(f"{now.strftime('%Y/%m/%d - %H:%M:%S')} ---> point(s) = {self.point}\n")
                        file.seek(0)
                        data = file.readlines()
                        list_points = [int(li.split("=")[1].strip()) for li in data]
                        self.text_max_point = self.font_small.render("Maximum Points = "+str(max(list_points)),False,"#717B84")

                # Add a point after passing the cactus
                if self.cactus_x <= -10 and not self.point_added:
                    self.point += 1
                    self.point_added = True

                made_rect = self.text_made.get_rect(bottomright=(WIDTH - 15, HEIGHT - 10))
                self.screen.blit(self.text_made, made_rect)
                pygame.display.update()  
                self.clock.tick(60)
                self.frame += 1     

            #-------------------------Game-Over-------------------------
            elif self.state=="over":

                self.screen.fill("#ffffff")

                self.screen.blit(self.dino,self.dino_rect)
                
                self.screen.blit(self.track,(self.track_x1,540))
                self.screen.blit(self.track,(self.track_x2,540))

                self.screen.blit(self.cloud,self.cloud_rect_1)
                self.screen.blit(self.cloud,self.cloud_rect_2)

                self.screen.blit(self.bird,self.bird_rect)

                self.screen.blit(self.cactus,self.cactus_rect)

                self.screen.blit(self.text_point,(30,30))

                self.screen.blit(self.game_over,(300,150))

                self.max_point_rect = self.text_max_point.get_rect(topleft=(380,230))
                self.screen.blit(self.text_max_point,self.max_point_rect)

                self.game_return_rect = self.game_return.get_rect(topleft=(450,300))
                self.screen.blit(self.game_return,self.game_return_rect)

                # Handle the reset button
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
                            self.dino_y = 555
                            self.bird_x = 1100
                            self.cactus_x = 1100
                            self.cactus = self.cactus_images[0]
                            self.track_x1 = 0
                            self.track_x2 = WIDTH
                            self.cloud_rect_1.x = 1500
                            self.cloud_rect_2.x = 2000
                            self.jump = "no"
                            pygame.mixer_music.play(-1)


                made_rect = self.text_made.get_rect(bottomright=(WIDTH - 15, HEIGHT - 10))
                self.screen.blit(self.text_made, made_rect)
                pygame.display.update() 
                self.clock.tick(60)
                
Game().run()