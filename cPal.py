import pygame

class cPal:
        """The 'stick' class.. the player"""
        __MOV_SPEED = 5;
        __ROT_SPEED = 3;
        __BACK_TICKS = 12;
        __JUMP_LENGTH = 5;
        
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

                #Movement Flag
                self.fmove = True

        
        #Rotate function. Called continuously
        def rotate(self,amount=__ROT_SPEED):
                """
                        rotate an image while keeping its center in the specified
                        amount attribute in degrees.

                        self.tbackwards defines a temporal rotation
                """
                
                if self.tbackwards:             #Check if temporal backwards rotation is set
                        self.rot -= amount + 2  #When rotating back has to be faster
                        self.tbackwards_ticks -= 1
                else:
                        self.rot += amount

                if self.tbackwards_ticks == 0:
                        self.tbackwards = False
                        #self.tbackwards_ticks = self.__BACK_TICKS

                if self.rot >= 360: self.rot = 0;

                self.image = pygame.transform.rotate(self.baseImage, self.rot)
                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = pygame.mask.from_surface(self.image)

        #
        # Moving Functions
        #
        def move_left(self):
                if self.fmove: self.movx -= cPal.__MOV_SPEED;
        def move_right(self):
                if self.fmove: self.movx += cPal.__MOV_SPEED;
        def move_up(self):
                if self.fmove: self.movy -= cPal.__MOV_SPEED;
        def move_down(self):
                if self.fmove: self.movy += cPal.__MOV_SPEED;
        

        def movement(self):
                """Move the Stick Rectangle"""
                if self.fmove:
                        self.rect = self.rect.move(self.movx,self.movy);

        def enable_disable_movement(self):
                """sets the movement flag"""
                if self.fmove: self.fmove = False
                else: self.fmove = True

        #
        # Colision Back Rotation and jump back
        #
        def flip_rotation_tmp(self,nframes=__BACK_TICKS):
                """
                        Flips the rotation temporally for a specified number
                        of frames
                """
                if self.tbackwards: self.tbackwards = False
                else: self.tbackwards = True

                self.tbackwards_ticks = nframes

        def jump_back(self,cx,cy):
                """
                        The stick Jumps Back to avoid further colisions
                        cx and xy are the MAP points of collision.

                        The jump back is decided by quadrants of stick collision
                        To decide which direction to jump
                        Q1|Q3
                        ------
                        Q2|Q4
                        
                """
                #JUMP directions
                jx = 0
                jy = 0
                #Check colision position of stick (which quadrant)
                sx = cx - self.rect.x
                sy = cy - self.rect.y
                sxc = self.rect.width/2
                syc = self.rect.height/2


                if sx < sxc and sy < syc :      #Q1
                        jx = cPal.__JUMP_LENGTH
                        jy = cPal.__JUMP_LENGTH
                elif sx < sxc and sy > syc:     #Q2
                        jx = cPal.__JUMP_LENGTH
                        jy = -cPal.__JUMP_LENGTH
                elif sx > sxc and sy < syc:     #Q3
                        jx = -cPal.__JUMP_LENGTH
                        jy = cPal.__JUMP_LENGTH
                else:                           #Q4
                        jx = -cPal.__JUMP_LENGTH
                        ju = -cPal.__JUMP_LENGTH

                self.rect = self.rect.move(jx,jy);

        def fancy_rotation_death(self,amount,scale):
                self.rot += amount

                if self.rot >= 360: self.rot = 0;

                self.image = pygame.transform.rotozoom(self.baseImage, self.rot,scale)
                self.rect = self.image.get_rect(center=self.rect.center)
