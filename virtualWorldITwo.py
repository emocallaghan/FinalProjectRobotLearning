# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 23:41:48 2014

@author: eocallaghan
"""

import pygame
from pygame.locals import *
import time
from abc import ABCMeta, abstractmethod

"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """  
                                    MODEL 
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """  


class Model:
    """ Encodes the world state of It's Learning and keeps track of all attributes
        contains a turtle, a list of walls, and a light
    """  
    def __init__(self, boundarySize):
        """ contructor for the WorldModel class"""
        self.light = LEDRing([100,100]) #assumes not placed within 50 pixels of World's Edge
        self.myWalls = []
        
        self.createWorldMap(boundarySize)
        
        self.robot = Robot(self.myWalls, self.light)

    def createWorldMap(self, boundarySize):
        """ 
        Create wall borders around world, walls as obstacles denoted here
        INPUTS: boundarySize, (x,y) coordinate of lower righthand corner of screen  
        """       
        #Block World's Edge 
        width = boundarySize[0]
        height = boundarySize[1]
        thickness = 50 #depth of border walls
                
        self.myWalls.append( Wall([0,0], [width,thickness]))                   #Ceiling
        self.myWalls.append( Wall([0,height-thickness], [width,thickness]))    #Floor        
        self.myWalls.append( Wall([width-thickness,0],[thickness,height]))     #Right       
        self.myWalls.append( Wall([0,0],[thickness,height]),color )                   #Left

        #Create World Obstacles
            ##None

    def update(self, action):
        self.robot.update(action)

class Drawable(object):
    """Abstract class for objects to be drawn on pygame window"""
    __metaclass__ = ABCMeta
    def __init__(self, position, dimensions, color):
        """
        constructor for Drawable class
        ATTRIBUTES: "position", (x,y) coordinates of primary locator
                    color, RGB values
                    "dimensions",
                        if (width,height): (x,y) length 
                        if (width,None): radius
        """
        assert(len(postion) == 2),"Drawable Object Location not defined in 2D"
        self.x = position[0]
        self.y = position[1]
        
        assert(len(color) == 3),"Drawable Object Color not defined in RGB"
        self.color = pygame.Color(color[0],color[1],color[2])
        
        assert(len(dimensions) == 2),"Drawable Object Size not defined in 2D"
        if dimensions[0] and dimensions[1] == None:
            self.radius = dimensions[0]
        elif dimensions[0] and dimensions[1]:
            self.width = dimensions[0]
            self.height = dimensions[1]
        else:
            print "WTF, object has neither radial nor cartesian dimensions..."
            global running
            running = False
            
    @abstractmethod    
    def draw():
        pass
"""--------------------------------Robot----------------------------------"""

"""--------------------Not Finished-----------------------"""
class Robot(Drawable):
    def __init__(self, walls, lightSource):
        super(Robot,self).__init__([400,600],[40,None],[170,50,255])
        self.front = (self.x,self.y-self.radius)
        self.direction = 0 #degrees
        self.walls = walls 
        
        self.sensorPack = SensorPack(self.front,self.direction,walls,lightSource)

    def update(self, action):
        if (action == 'fwd'):
            for i in range(10):
                if(self.checkCollision()):
                    break
                self.fwd()
        elif (action == 'left'):
            self.left()
        elif (action == 'right'):
            self.right()

    def fwd(self):
        if (self.direction == 0):
            self.y +=-1
            self.front(1) += -1
        elif(self.direction == 90):
            self.x += -1
            self.front(0) += -1
        elif(self.direction == 180):
            self.y += 1
            self.front(1) += 1
        elif(self.direction == 270):
            self.x += 1
            self.front(0) += 1
        self.sensorPack.update(self.front, self.direction)
    
    def left(self):
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
        self.sensorPack.update(self.front, self.direction)
    
    def right(self):
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
        self.sensorPack.update(self.front, self.direction)
    
    def checkCollision(self):
        for wall in walls:
            if(wall.betweenX(self.front(0)) and wall.betweenY(self.front(1))):
                return True
        return False
   
    def getTouch(self):
        data = self.sensorpack.getSensorData()
        return data[0]
        
    def getIR(self):
        data = self.sensorpack.getSensorData()
        return data[1]
    
    def getUltra(self):
        data = self.sensorpack.getSensorData()
        return data[2]
    
    


"""-----------------------------SensorPack--------------------------------"""

class SensorPack(Drawable):

    def __init__(self,position,direction,walls,lightSource):
        super(SensorPack,self).__init__(position,[5,None],[0,255,100])
        self.direction = direction       
        self.irSensor = IRSensor(lightSource)
        self.ultrasonicSensor = UltraSonicSensor(walls)
        self.touchSensor = TouchSensor(walls)
   
    def getSensorData(self):
        sensorData = []
        sensorData.append(self.touchSensor.getData([self.x,self.y]))
        sensorData.append(self.irSensor.getData([self.x,self.y],self.direction))
        sensorData.append(self.ultrasonicSensor.getData([self.x,self.y],self.direction))
        return sensorData
        
    def update(self,position,direction):
        self.x = position[0]
        self.y = position[1]
        self.direction = direction
        
class Sensor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getData(self):
        pass


class IRSensor(Sensor):
    def __init__(self, lightSource):
        """ 
        constructor for IRSensor class
        ATTRIBUTES: lightSource, instance of LEDRing
                        used to find intensity of light at sensor location
                        assumes one lightSource
        """
        self.lightSource = lightSource 
        
    def getData(self,positon,direction):
        """Determines intensity of light IR sensor is receiving""" 
        x = position[0]
        y = position[1]
        hasData = False #off/on variable for sensor direction compared to location of light
        
        # Determines if sensor pointing in a useful direction
        if(direction == 0):
            if(y > self.lightSource.y):
                hasData = True
        elif(direction == 90):
            if(x > self.lightSource.x):
                hasData = True
        elif(direction == 180):
            if(y < self.lightSource.y):
                hasData = True
        elif(direction == 270):
            if(x < self.lightSource.x):
                hasData = True
        
        #returns intensity if sensor is pointing "toward" light, else returns zero        
        if(hasData):
            return self.lightSource.intensity()
        else:
            return 0
            
class UltraSonicSensor(Sensor):
    def __init__(self, walls):
        """ 
        constructor for UltraSonicSensor class
        ATTRIBUTES: walls, list of wall instances in model
                        used to find distance to wall from sensor (in sensor direction)
                        assumes one lightSource
        """
        self.walls = walls
    
    def getData(self, position, direction):
        """Determines intensity of light IR sensor is receiving"""
        x = position[0]
        y = position[1]
        wallsInFront = []
        wallToUse = None
        
        #finds all walls in front of turtle
        for wall in self.walls:
            if(direction == 0 and y > wall.y):
                wallInFront.append(wall)
            if(direction == 90 and x > wall.x):
                wallInFront.append(wall)
            if(direction == 180 and y < wall.y):
                wallInFront.append(wall)
            if(direction == 270 and x < wall.x):
                wallInFront.append(wall)
                
        #if no walls in front
        #assumedly this will never happen if the world is properly bounded by walls
        if(len(wallsInFront) == 0):
            return 1
                    
        #pick closest wall
        if(len(wallsInFront)>1):
            #compares to last closest wall
            closestWall = wallsInFront[0]
            for wall in wallsInFront:
                if(direction == 0 and wall.y > closestWall.y):
                    closestWall = wall
                elif(direction == 90 and wall.x > closestWall.x):
                    closestWall = wall
                elif(direction == 180 and wall.y < closestWall.y):
                    closestWall = wall
                elif(direction == 270 and wall.x < closestWall.x):
                    closestWall = wall
            wallToUse = closestWall
        #if only one wall            
        elif(len(wallsInFront) == 1):
            wallToUse = wallsInFront[0]
        
        #value to return
        #assert(wallToUse),"UltraSonic: No wall chosen"
        distance = self.distanceToWall(wallToUse,position,direction)   #distance to wallToUse
        assert(distance),"UltraSonic: No distance returned"
        if(distance > 300):
            distance = 300      #greatest noticable distance           
        norm = distance/300.0   #normalized distance
        return norm
                 
    def distanceToWall(wall,position,direction):
        """ Finds Distance to wall """
        x = position[0]
        y = position[1]
        
        if(direction == 0):
            return y - (wall.y + wall.height)
        if(direction == 90):
            return x - (wall.x + wall.width)
        if(direction == 180):
            return wall.y - y
        if(direction == 270):
            return wall.x - x
            
class TouchSensor(Sensor):
    def __init__(self,walls):
        self.walls = walls
    
    def getData(self,position):
        for wall in walls:
            return self.isTouching(wall,position)

    def isTouching(self,wall,position):
        return self.betweenX(wall,position[0]) and self.betweenY(wall,position[1])        
        
    def betweenX(self,wall,x):
        return (wall.x <= x) and (x <= wall.x + wall.width)
        
    def betweenY(self,wall,y):
        return (wall.y <= y) and(y <= wall.y + wall.height)
  

"""----------------------------World Elements-----------------------------""" 
     
class LEDRing:
    """provides a light source in the world: includes a constructor and an intensity(distance) evaluator"""
    def __init__(self, position):
        """ 
        constructor for the LEDRing class
        ATTRIBUTES: x denotes the x center coordinate of the light source
                    y denotes the y center coordinate of the light source  
        """
        self.x = position[0]
        self.y = position[1]
        
    def intensity(self, measurePosition):
        deltax = measurePosition[0]-self.x
        deltay = measurePosition[1]-self.y
        distance = (deltax**2+deltay**2)**.5
        distanceReverseMap = 160 - distance
        if(distanceReverseMap < 0):
            distanceReverseMap = 0
        norm = distanceReverseMap/160.0
        return norm
        
    
class Wall(Drawable):
    """provides a walls in the world: includes a constructor and a collision evaluator"""
    def __init__(self,position, dimensions, color=(0,0,0)):
        """
        constructor for Wall class
        ATTRIBUTES: "position", (x,y) coordinates of upper lefthand corner of wall
                    "dimensions", (x,y) length of wall
                    color, RGB turple of wall, defaults as black
        """
        super(Wall,self).__init__(position,dimesnsions,color)
        self.x = position(0)
        self.y = position(1)

    def betweenX(self, x):
        return (self.x <= x) and (x <= self.x + self.width)
    
    def betweenY(self, y):
        return (self.y <= y) and (y <= self.y + self.height)
        
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
                                View
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
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
         
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """  
                               Running Code  
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """ 
            
if __name__ == '__main__':
    pygame.init()

    size = (1000,700)
    screen = pygame.display.set_mode(size)

    model = Model(size)
    
    
    
     """---Nothing Below has been updated to the new architecture---"""
    
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
    
        
        