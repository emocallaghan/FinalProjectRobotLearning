# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:54:39 2014

@author: eocallaghan
"""

import pygame
from pygame.locals import *
import time
from abc import ABCMeta, abstractmethod

class Model:
    """ Encodes the game state of Galaga and keeps track of all attributes
        contains a fighter, a list of bullets fired by my fighter, a list of enemies
        and a list of bullets fired by the enemy"
    """
    def __init__(self, size):
        """ contructor for the GalagaModel class"""
        self.y = size[0]
        self.x = size[1]
        self.robot = Robot()
        self.myWalls = []
        self.brick = 50
        self.newWall(100,100,self.brick,100)
                
        self.newWall(0,0, self.x, self.brick)        
        self.newWall(0,0, self.brick,self.y)

        self.newWall(self.y-self.brick,0,self.x,self.brick)
        self.newWall(0,self.x-self.brick,self.brick, self.y)

    def newWall(self, x,y, height, width):
        """this function creates a new bullet fired from fighter at the passed in locations, x and y"""
        color = (0,0,0)
        self.myWalls.append(Wall(color,x,y,height,width))

    def update(self):
        """updates fighter, all bullets, and all enemies"""
        self.robot.update()
        
        
        
        
class Collidable(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def collide(self, collidable):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass         
        
        
class Robot():
    """fighter class contains a contruction and update method"""
    def __init__(self):
        """constructor for fighter sets location based ppppp given values, number of lives, pixle height
        and width inital speed as zero and loads the image of a fighter"""
        self.x = 400
        self.y = 600
        self.vx = 0
        self.vy = 0
        self.radius = 40
        self.color = pygame.Color(170,50,255)
        self.front = (self.x,self.y-self.radius)
        self.direction = 0
        self.directionBeforeCollision = 0
        self.canForward = True
        self.collided = False
        self.previousX = self.x
        self.previousY = self.y


    def collide(self,collidable):
        pass

    def update(self):
        """moves position based on velocity unless at either side of screen and attempting to move
        off screen where it is stopped"""
        """print("In update")
        print(self.canForward)
        print(self.direction)
        print self.directionBeforeCollision"""
        if(not (self.x == self.previousX and self.y == self.previousY)):
            self.collided = False
        if(self.canForward):
            self.move()
            
        elif(self.direction == self.directionBeforeCollision):
            self.stop()
            
        else:
            self.canForward = True
            self.move()



            
    def move(self):

        self.x += self.vx
        self.y += self.vy
        
        if(self.direction == 0):
            self.front = (self.x, self.y - self.radius)
            
        if(self.direction == 90):
            self.front = (self.x - self.radius, self.y)
            
        if(self.direction == 180):
            self.front = (self.x, self.y+self.radius)

        if(self.direction == 270):
            self.front = (self.x + self.radius, self.y)





    def stop(self):
        self.vx = 0
        self.vy = 0



        
    def foward(self):
        if(self.direction == 0):
            self.vy = -1
            self.vx = 0
        if(self.direction == 90):
            self.vy = 0
            self.vx = -1
        if(self.direction == 180):
            self.vy = 1
            self.vx  = 0
        if(self.direction == 270):
            self.vy = 0
            self.vx = 1


            
            
    def turnLeft(self):
        self.stop()
        if(self.direction == 0):
            self.front = (self.x - self.radius, self.y)
            self.direction = 90
        elif(self.direction == 90):
            self.front = (self.x, self.y+self.radius)
            self.direction = 180
        elif(self.direction == 180):
            self.front = (self.x + self.radius, self.y)
            self.direction = 270
        elif(self.direction == 270):
            self.front = (self.x, self.y - self.radius)
            self.direction = 0
            


            
    def turnRight(self):
        self.stop()
        if(self.direction == 0):
            self.front = (self.x + self.radius, self.y)
            self.direction = 270
        elif(self.direction == 270):
            self.front = (self.x, self.y+self.radius)
            self.direction = 180
        elif(self.direction == 180):
            self.front = (self.x - self.radius, self.y)
            self.direction = 90
        elif(self.direction == 90):
            self.front = (self.x, self.y - self.radius)
            self.direction = 0
        
    def setDirectionBeforeCollision(self, direction):
        self.directionBeforeCollision = direction
        
        
        
        
        

class Wall:
    """bullet class contains a constructor and update"""
    def __init__(self,color,x, y,height,width):
        """sets color, height, width, position, and velocity based on passed in parameters"""
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y        
        
        
        
        
        
        
        
        
        
        
        

class PyGameWindowView:
    """ A view of Galaga rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        """draws all of the elements on the screen uses a series of subfunctions
        to draw fighters, bullets, and enemy"""
        self.screen.fill(pygame.Color(255,255,255))
        for wall in self.model.myWalls:
            self.drawWall(wall)
        self.drawRobot(self.model.robot)
        
        pygame.display.update()
       
    def drawWall(self, wall):
        """draws a rectangle for a bullet based on passed in bullet and its parameters"""
        rectangle = pygame.Rect(wall.x,wall.y,wall.width,wall.height)
        pygame.draw.rect(self.screen, wall.color, rectangle)
        
    def drawRobot(self, robot):
        """draws a fighter from what is passed in"""
        pygame.draw.circle(self.screen, robot.color, (robot.x, robot.y), robot.radius, 0)
        pygame.draw.circle(self.screen, (0,0,0), robot.front, 5)



















class PyGameKeyboardController:
    """ Handles keyboard input for galaga"""
    def __init__(self,model):
        """contructor just sets the model to model"""
        self.model = model
    
    def handle_keyboard_event(self,event):
        """sets how the fighter moves and if the user shoots a bullet"""
        if event.type == KEYDOWN:
            """if the a key is pushed and held down the fighter moves to the left if the d
            key is pushed and held down the fighter moves to the right if the space bar is hit
            a bullet is created"""
            robot = self.model.robot
            if event.key == pygame.K_a:
                robot.turnLeft()
            if event.key == pygame.K_d:
                robot.turnRight()
            if event.key == pygame.K_w:
                robot.foward() 
        if event.type == KEYUP:
            """if the a key is lifted up and the player is traveling to the left the player will stop.
            if the d key is lifted and the player is traveling to the right the player will stop."""
            if event.key == pygame.K_w:
                self.model.robot.stop()

class CollisionController:
    """tests if any two objects colloide"""
    def __init__(self, model):
        self.model = model

    def checkCollisions(self):
        
        for wall in self.model.myWalls:
            robot = self.model.robot
            x1 = robot.x-robot.radius
            y1 = robot.y - robot.radius
            
            width1 = robot.radius*2
            height1 = robot.radius*2
            
            x2 = wall.x
            y2 = wall.y
            width2 = wall.width
            height2 = wall.height
            if (self.sameSpace(x1, y1, width1, height1, x2, y2, width2, height2)):
                """checks if the fighter is in the same place as any of the basic enemies and removes the enemy and takes away a life from the 
                    fighter if this is the case. if the fighter has no more lifes closes window and prints that the player 
                    lost and prints the score"""
                if(not self.model.robot.collided):
                    self.model.robot.setDirectionBeforeCollision(self.model.robot.direction)
                    self.model.robot.canForward = False
                    print("In Collision")
                    print(self.model.robot.direction)
                    print(self.model.robot.directionBeforeCollision)
                    self.model.robot.collided = True
                    print (self.model.robot.collided)
                    self.model.robot.previousX = self.model.robot.x
                    self.model.robot.previousY = self.model.robot.y
                    
                
    def sameSpace(self, x1, y1, width1, height1, x2, y2, width2, height2):
        """function checks if thetwo objects occupy the same space."""
        return (x2<= x1+width1 and x2+width2>= x1 and y2 <= y1+height2 and y2+height2 >= y1)





















        
if __name__ == '__main__':
    pygame.init()

    size = (1000,700)
    screen = pygame.display.set_mode(size)

    model = Model(size)
    view = PyGameWindowView(model,screen)

    KeyBoardcontroller = PyGameKeyboardController(model)
    collisionController = CollisionController(model)    
    running = True
    
    startTime = time.time()
    xTime = time.time()
    
    
    while running:
        collisionController.checkCollisions()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            KeyBoardcontroller.handle_keyboard_event(event)
            collisionController.checkCollisions()
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
  