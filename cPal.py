import pygame

class cPal:
        """The 'stick' class.. the player"""
        __MOV_SPEED = 5;
        __ROT_SPEED = 45;
        __BACK_TICKS = 12
        
        def __init__(self,x,y,rot):
                
                self.image      = pygame.image.load("stick.png")
                self.baseImage  = pygame.image.load("stick.png")
                self.mask       = pygame.mask.from_surface(self.image);
                
                self.rect = self.image.get_rect();
                
                self.movx = 0;
                self.movy = 0;

                self.rot = rot;
                
                #backwards move
                self.tbackwards = False
                self.tbackwards_ticks = self.__BACK_TICKS

                self.rect.x,self.rect.y = x,y
        
        #Rotate function. Called continuously
        def rotate(self,amount):
                """rotate an image while keeping its center"""

                #Check if temporal backwards rotation is set
                if self.tbackwards:
                        self.rot -= amount
                        self.tbackwards_ticks -= 1
                else:
                        self.rot += amount

                if self.tbackwards_ticks == 0:
                        self.tbackwards = False
                        self.tbackwards_ticks = self.__BACK_TICKS

                if self.rot >= 360: self.rot = 0;

                self.image = pygame.transform.rotate(self.baseImage, self.rot)
                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = pygame.mask.from_surface(self.image)

        """Moving functions"""
        def move_left(self):    self.movx -= cPal.__MOV_SPEED;
        def move_right(self):   self.movx += cPal.__MOV_SPEED;
        def move_up(self):      self.movy -= cPal.__MOV_SPEED;
        def move_down(self):    self.movy += cPal.__MOV_SPEED;
        

        def movement(self):
                self.rect = self.rect.move(self.movx,self.movy);

        def flip_rotation_tmp(self):
                if self.tbackwards: self.tbackwards = False
                else: self.tbackwards = True


        def fancy_rotation_death(self,amount,scale):
                self.rot += amount

                if self.rot >= 360: self.rot = 0;

                self.image = pygame.transform.rotozoom(self.baseImage, self.rot,scale)
                self.rect = self.image.get_rect(center=self.rect.center)
