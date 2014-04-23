# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:54:39 2014

@author: eocallaghan
"""

import pygame
from pygame.locals import *
import time
from abc import abstractmethod, ABCMeta

class Model:
    """ Encodes the world state of It's Learning and keeps track of all attributes
        contains a turtle, a list of walls, and  a list of lights
    """
    def __init__(self):
        """ contructor for the WorldModel class"""
        self.robot = Robot()
        self.myWalls = []
        self.myLights = []
        self.newWall(100,100,50,100)

    def newWall(self, x,y, height, width):
        """this function creates a new wall at the passed in locations, x and y"""
        color = (0,0,0)
        self.myWalls.append(Wall(color,x,y,height,width))

    def update(self):
        """updates turtle, all walls, and all lights"""
        self.robot.update()

class PyGameWindowView:
    """ A view of the world rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        """draws all of the elements on the screen useing a series of subfunctions
        to draw turtle, walls, and lights"""
        self.screen.fill(pygame.Color(255,255,255))
        for wall in self.model.myWalls:
            self.drawWall(wall)
        self.drawRobot(self.model.robot)
        
        pygame.display.update()
       
    def drawWall(self, wall):
        """draws a rectangle for a wall based on passed in wall and its parameters"""
        rectangle = pygame.Rect(wall.x,wall.y,wall.width,wall.height)
        pygame.draw.rect(self.screen, wall.color, rectangle)
        
    def drawRobot(self, robot):
        """draws a turtle from what is passed in"""
        pygame.draw.circle(self.screen, robot.color, (robot.x, robot.y), robot.radius, 0)
        pygame.draw.circle(self.screen, (0,0,0), robot.front, 5)

class PyGameKeyboardController:
    """ Handles keyboard input for turtle"""
    def __init__(self,model):
        """contructor just sets the model to model"""
        self.model = model
    
    def handle_keyboard_event(self,event):
        """sets how the turtle moves"""
        if event.type == KEYDOWN:            
            robot = self.model.robot
            """if the a key is pushed and held down, the turtle point-turns left 90degrees""" 
            if event.key == pygame.K_a:
                robot.turnLeft()
            """if the d key is pushed and held down, the turtle point-turns right 90degrees"""    
            if event.key == pygame.K_d:
                robot.turnRight()
            """if the w key is pushed and held down, the turtle moves straight"""   
            if event.key == pygame.K_w:
                robot.forward() 
        if event.type == KEYUP:
            """if the w key is lifted up, the turtle will stop """
            if event.key == pygame.K_w:
                self.model.robot.stop()

class CollisionController:
    """tests if any two objects collide"""
    def __init__(self, model):
        self.model = model

    def checkCollisions(self):
        
        for wall in self.model.myWalls:
            robot = self.model.robot
            x1 = robot.x - robot.radius
            y1 = robot.y - robot.radius
            
            width1 = robot.radius*2
            height1 = robot.radius*2
            
            x2 = wall.x
            y2 = wall.y
            width2 = wall.width
            height2 = wall.height
            
            if (self.sameSpace(x1, y1, width1, height1, x2, y2, width2, height2)):
                """checks if the turtle is in the same place as any of the walls and sets 
                the ability to move forward to false"""
                robot.directionBeforeCollison = robot.direction
                robot.canForward = False
                print "Collision"
                
    def sameSpace(self, x1, y1, width1, height1, x2, y2, width2, height2):
        """function checks if the         self.color = colortwo objects occupy the same space."""
        return (x2<= x1+width1 and x2+width2>= x1 and y2 <= y1+height2 and y2+height2 >= y1)

class Drawable(object):
    """StaticObject class contains a constructor for moject appearence and location"""
    def __init__(self,color,x, y,height,width=None):
        """sets color, height, width, and center position on passed in parameters"""
        self.color = color
        self.x = x
        self.y = y
        self.height = height
        if width:
            self.width = width
        else:
            self.width = self.height    
        
class Robot(Drawable):
    """Turtle class contains a contruction and update method"""
    def __init__(self):
        """constructor for turtle sets location based given values, creates pixel height
        and width, inital speed and colision as zero and defines the color of the turtle"""
        self.radius = 40
        super(Robot,self).__init__(pygame.Color(170,50,255),400,600,self.radius*2)        
        self.front = (self.x,self.y-self.radius)
        self.direction = 0
        self.directionBeforeCollision = 0
        self.canForward = True
        self.vx = 0
        self.vy = 0


    def update(self):
        """moves position based on velocity unless at either side of screen and attempting to move
        off screen where it is stopped"""
        if(self.canForward):
            self.move()
            print"can moveForward"
        elif(self.direction == self.directionBeforeCollision):
            self.vx = 0
            self.vy = 0
        else:
            self.canForward = True
            self.move()
            
    def move(self):
        if (self.x-self.radius == 0 and self.vx < 0) or (self.x+self.radius == 1000 and self.vx>0):
            self.vx = 0            
        if (self.y-self.radius == 0 and self.vy < 0) or (self.y+self.radius == 700 and self.vy>0):
            self.vy = 0
            
        self.x += self.vx
        self.y += self.vy
          
        directionOptions = {
                0   :lambda:(self.x, self.y - self.radius), 
                90  :lambda:(self.x - self.radius, self.y), 
                180 :lambda:(self.x, self.y+self.radius),   
                270 :lambda:(self.x + self.radius, self.y)
                }        
        assert(self.direction in directionOptions), "move: Direction " + str(self.direction) + "deg not found as an option"
        self.front = directionOptions[self.direction]()

    def stop(self):
        self.vx = 0
        self.vy = 0        
        
    def forward(self):      
        self.directionOptions = {
                0   :{"vx": 0,"vy":-1},
                90  :{"vx":-1,"vy": 0}, 
                180 :{"vx": 0,"vy": 1}, 
                270 :{"vx": 1,"vy": 0}
                }        
        assert(self.direction in directionOptions), "forward: Direction " + str(self.direction) + "deg not found as an option"
        self.vx = directionOptions[self.direction]["vx"]()
        self.vy = directionOptions[self.direction]["vy"]()
            

    def turn(self,spin):
        self.vx = 0
        self.vy = 0
        
        if spin: 
            directionOptions = {
                0   : lambda h:(self.x - h*self.radius, self.y),
                90  : lambda h:(self.x, self.y + h*self.radius),
                180 : lambda h:(self.x + h*self.radius, self.y),
                270 : lambda h:(self.x, self.y - h*self.radius)
                } 
                        
            assert(self.direction in directionOptions), "turn " + str(spin) + ": Direction " + str(self.direction) + "deg not found as an option"
            self.front = directionOptions[self.direction](spin)
        
        if (self.direction + 90*spin > 270) or (self.direction + 90*spin < 0):
            self.direction = 0
        else:
            self.direction = self.direction + 90*spin
            
        assert(self.direction in [0,90,180,270]), "turn " + str(spin) + ": Direction " + str(self.direction) + "deg not found as an option"
        
    def turnLeft(self):
        self.front, self.direction = self.turn(1)         
             
    def turnRight(self):
        self.front, self.direction = self.turn(-1)   

class SensorPack(Drawable):
    """Sensor class contains a construc        self.color = colortor and update function to determine sensor values and location"""
    def __init__(self,x, y,radius):
        """sets color, height, width, center position, and initial velocities on passed in parameters"""
        self.radius = radius
        super(SensorPack,self).__init__((100,100,100),x, y,self.radius*2)
        
    def update(self,robot):
        self.x = robot.front[0]
        self.y = robot.front[1]
        
class Wall(Drawable):
    """wall class contains a constructor"""
    def __init__(self,color,x, y,height,width):
        """sets color, height, width, and position on passed in parameters"""
        super(Wall,self).__init__(color,x, y,height,width)
        self.color = color
class Light(Drawable):
    """light class contains a constructor"""
    def __init__(self,color,x, y,height,width,intensity):
        """sets color, height, width, and position on passed in parameters"""
        super(Wall,self).__init__(color,x, y,height,width)
        self.maxIntensity = intensity

#### need a intensity gauge for distance W/m^2 and intensityMod based on angle of sensor to light
#### angle for angle intensity can be determined by line of sensor/head to turtle center
    
if __name__ == '__main__':
    pygame.init()

    size = (1000,700)
    screen = pygame.display.set_mode(size)

    model = Model()
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
  