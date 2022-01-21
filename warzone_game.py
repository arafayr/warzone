#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import random
from pygame import mixer
import pygame



pygame.init()


#set framerates
clock = pygame.time.Clock()
FPS = 60

class initializing_world:
    def __init__(self):
        # Intialize the pygame
        
        # creating the screen
        self.screen_ratio= pygame.display.set_mode((800, 600))

        #Setting Background
        self.bg= pygame.image.load('bg.jpeg')

        #Setting Sound
        mixer.music.load("background.mp3")
        mixer.music.play(-1)

        # Caption and Icon
        pygame.display.set_caption("Warzone")
        self.icon = pygame.image.load('icon.jpeg')
        pygame.display.set_icon(self.icon)
        
        #Setting Score

        self.score_num  = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.textX = 10
        self.testY = 10

        # Game Over
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)

        
        
        
    #Initializing player
    def player_initialize(self):

        # Player
        Image = pygame.image.load('player.png')
        self.playerImg = pygame.transform.scale(Image, (115, 130)) 

        self.player_Xaxis = 370
        self.player_Yaxis = 480
        self.player_Xaxis_change = 0
        
        
    #Initializing Enemy
    def enemy_initialize(self):

        # Enemy
        self.enemyImg = []
        self.enemy_Xaxis = []
        self.enemy_Yaxis  = []
        self.enemy_Xaxis_change = []
        self.enemy_Yaxis_change = []
        self.no_of_enemies = 6
        
    #Dislpaying Enemy
    def enemy_display(self):
        #Initializing_Enemy_display
        for i in range(self.no_of_enemies):
            image = pygame.transform.scale(pygame.image.load('enemy.png'), (65, 65)) 
            self.enemyImg.append(image)
            self.enemy_Xaxis.append(random.randint(0, 736))
            self.enemy_Yaxis.append(random.randint(50, 150))
            self.enemy_Xaxis_change.append(4)
            self.enemy_Yaxis_change.append(40)
            
    #Initializing Bullet    
    def bullet(self):


        # Bullet

        # Ready - You can't see the bullet on the screen
        # Fire - The bullet is currently moving

        bullet_image = pygame.image.load('bullet1.png')
        self.bulletImg = pygame.transform.scale(bullet_image, (10, 45)) 

        self.bullet_Xaxis = 0
        self.bullet_Yaxis = 480
        self.bullet_Xaxis_change = 0
        self.bullet_Yaxis_change = 10
        self.bullet_state = "ready"
        

        
        

    

#Game Mechanism
class gameloop(initializing_world):
    def __init__(self):
        
        #Calling Functions
        super().__init__()
        super().enemy_initialize()
        super().enemy_display()
        super().bullet()
        super().player_initialize()
        
        
        
        
        
    #Dsiplaying Score
    def show_score(self,x, y):
        self.score = self.font.render("Score : " + str(self.score_num ), True, (255, 255, 255))
        self.screen_ratio.blit(self.score, (x, y))

    #Dsiplaying Game Over Text
    def game_over_text(self):
        self.over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen_ratio.blit(self.over_text, (200, 250))

    #Dsiplaying Player
    def player(self,x, y):
        self.screen_ratio.blit(self.playerImg, (x, y))

    #Dsiplaying Enemy
    def enemy(self,x, y, i):
        self.screen_ratio.blit(self.enemyImg[i], (x, y))

    #Dsiplaying Bullet    
    def fire_bullet(self,x, y):
        
        self.bullet_state = "fire"
        self.screen_ratio.blit(self.bulletImg, (x + 16, y + 10))

    #Dsiplaying Collision of Enemy and Bullet
    def isCollision(self,enemy_Xaxis, enemy_Yaxis, bullet_Xaxis, bullet_Yaxis):
        distance = math.sqrt(math.pow(enemy_Xaxis - bullet_Xaxis, 2) + (math.pow(enemy_Yaxis - bullet_Yaxis, 2)))
        if distance < 27:
            return True
        else:
            return False
    
    #Working
    def game(self):
        
        
        # Game Loop
        ongoing = True
        while ongoing:
            clock.tick(FPS)

            # RGB = Red, Green, Blue
            self.screen_ratio.fill((0, 0, 0))
            # Background Image
            self.screen_ratio.blit(self.bg, (0, 0))
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ongoing = False

                # if keystroke is pressed check whether its right or left
                
                #Resume Mechanism with "r"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # ongoing = True
                        super().enemy_initialize()
                        super().enemy_display()
                        self.score_num  = 0

                    #Quit Mechanism with "Esc"
                    if event.key == pygame.K_ESCAPE:
                        ongoing = False 
                        
                    #Left movement Mechanism with "Left arrow key"
                    if event.key == pygame.K_LEFT:
                        self.player_Xaxis_change = -5
                        
                    #Right movement Mechanism with "Right arrow key"
                    if event.key == pygame.K_RIGHT:
                        self.player_Xaxis_change = 5
                        
                    #Shooting Mechanism with "Space bar"
                    if event.key == pygame.K_SPACE:
                        if self.bullet_state == "ready":
                            bulletSound = mixer.Sound("gun.mp3")
                            bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            self.bullet_Xaxis = self.player_Xaxis
                            self.fire_bullet(self.bullet_Xaxis, self.bullet_Yaxis)
                            
                    
                #Stop Mechanism when key is up
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player_Xaxis_change = 0

            # 5 = 5 + -0.1 -> 5 = 5 - 0.1
            # 5 = 5 + 0.1
            
            #Player Movement
            self.player_Xaxis += self.player_Xaxis_change
            #Player Movement Boundries
            if self.player_Xaxis <= 0:
                self.player_Xaxis = 0
            elif self.player_Xaxis >= 700:
                self.player_Xaxis = 700

            # Enemy Movement
            for i in range(self.no_of_enemies):

                # Game Over
                if self.enemy_Yaxis[i] > 440:
                    for j in range(self.no_of_enemies):
                        self.enemy_Yaxis[j] = 2000
                    self.game_over_text()
                    break

                self.enemy_Xaxis[i] += self.enemy_Xaxis_change[i]
                
                #Enemy Movement Boundries
                if self.enemy_Xaxis[i] <= 0:
                    self.enemy_Xaxis_change[i] = 4
                    self.enemy_Yaxis[i] += self.enemy_Yaxis_change[i]
                elif self.enemy_Xaxis[i] >= 736:
                    self.enemy_Xaxis_change[i] = -4
                    self.enemy_Yaxis[i] += self.enemy_Yaxis_change[i]

                # Collision
                collision = self.isCollision(self.enemy_Xaxis[i], self.enemy_Yaxis[i], self.bullet_Xaxis, self.bullet_Yaxis)
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    self.bullet_Yaxis = 480
                    self.bullet_state = "ready"
                    self.score_num  += 1
                    self.enemy_Xaxis[i] = random.randint(0, 736)
                    self.enemy_Yaxis[i] = random.randint(50, 150)

                self.enemy(self.enemy_Xaxis[i], self.enemy_Yaxis[i], i)

            # Bullet Movement
            if self.bullet_Yaxis <= 0:
                self.bullet_Yaxis = 480
                self.bullet_state = "ready"

            if self.bullet_state == "fire":
                self.fire_bullet(self.bullet_Xaxis, self.bullet_Yaxis)
                self.bullet_Yaxis -= self.bullet_Yaxis_change

            self.player(self.player_Xaxis, self.player_Yaxis)
            self.show_score(self.textX, self.testY)
            pygame.display.update()
            
obj=gameloop()
obj.game()


# In[ ]:





# In[ ]:




