# -*- coding: utf-8 -*-
"""
Created on Fri May  2 12:22:17 2014

@author: cbeery
"""

import pygame
from pygame.locals import *
from Abstract import abstractClass
"""--------------------------------Robot----------------------------------"""

class Robot(abstractClass.Drawable):
    def __init__(self, walls, lightSource):
        super(Robot,self).__init__([100,100],[40,None],[170,50,255,255])
        self.front = [self.x,self.y-self.radius]
        self.direction = 0 #degrees
        self.sensorPack = SensorPack(self.front,self.direction,lightSource,walls)
        self.walls = walls
    
    def update(self, action):
        if (action == 'fwd'):
            for i in range(9):
                if(self.checkCollision()):
                    break
                self.fwd()
        elif (action == 'left'):
            self.left()
        elif (action == 'right'):
            self.right()
            
        if(self.checkCollision()):
            self.sensorPack.touchSensor = True
        else:
            self.sensorPack.touchSensor = False    
            
        self.sensorPack.update(self.front,self.direction)

    def fwd(self):
        if (self.direction == 0):
            self.y +=-1
            self.front[1] = self.front[1] - 1
        elif(self.direction == 90):
            self.x += -1
            self.front[0] = self.front[0] - 1
        elif(self.direction == 180):
            self.y += 1
            self.front[1] = self.front[1]+1
        elif(self.direction == 270):
            self.x += 1
            self.front[0] = self.front[0] + 1
    
    def left(self):
        if(self.direction == 0):
            self.front = [self.x - self.radius, self.y]
            self.direction = 90
        elif(self.direction == 90):
            self.front = [self.x, self.y+self.radius]
            self.direction = 180
        elif(self.direction == 180):
            self.front = [self.x + self.radius, self.y]
            self.direction = 270
        elif(self.direction == 270):
            self.front = [self.x, self.y - self.radius]
            self.direction = 0

    def right(self):
        if(self.direction == 0):
            self.front = [self.x + self.radius, self.y]
            self.direction = 270
        elif(self.direction == 270):
            self.front = [self.x, self.y+self.radius]
            self.direction = 180
        elif(self.direction == 180):
            self.front = [self.x - self.radius, self.y]
            self.direction = 90
        elif(self.direction == 90):
            self.front = [self.x, self.y - self.radius]
            self.direction = 0
    
    def checkCollision(self):
        for wall in self.walls:
            if(wall.betweenX(self.front[0]) and wall.betweenY(self.front[1])):
                return True
        return False
        
    def draw(self,screen):
        """draws robot  as a circle"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        self.sensorPack.draw(screen)
        
        
        
"""-----------------------------SensorPack--------------------------------"""

class SensorPack(abstractClass.Drawable):

    def __init__(self,position,direction,lightSource,wall,):
        super(SensorPack,self).__init__(position,[5,None],[50,0,50])
        self.direction = direction
        self.ultrasonicSensor = UltraSonicSensor(wall,lightSource)
        self.irSensor = IRSensor(lightSource, self.ultrasonicSensor)
        self.touchSensor = True
    def getSensorData(self):
        sensorData = []
        sensorData.append(self.irSensor.getData([self.x,self.y], self.direction))
        sensorData.append(self.touchSensor)
        sensorData.append(self.ultrasonicSensor.getData([self.x,self.y], self.direction))
        return sensorData
        
    def update(self,position,direction):
        self.x = position[0]
        self.y = position[1]
        self.direction = direction
        
    def draw(self,screen):
        """draws sensor pack ring  as a circle"""
        if self.touchSensor == True:
            self.color = (255,0,0,225)
        else:
            self.color = (50,0,50,255)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
       


class IRSensor(abstractClass.Sensor):
    def __init__(self, lightSource, UltraSonicSensor):
        """
        constructor for IRSensor class
        ATTRIBUTES: lightSource, instance of LEDRing
        used to find intensity of light at sensor location
        assumes one lightSource
        """
        self.lightSource = lightSource
        self.UltraSonicSensor = UltraSonicSensor
        
    def getData(self,position,direction):
        """Determines intensity of light IR sensor is receiving"""
        x = position[0]
        y = position[1]
        hasData = False #off/on variable for sensor direction compared to location of light
        
        # Determines if sensor pointing in a useful direction
        if(direction == 0):
            if(y > self.lightSource.y and self.correctOther(self.lightSource.x, x)):
                print "LIZZY FUCKED IT FUUCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCK"
                if(self.UltraSonicSensor.getData(position,direction) > abs(y-self.lightSource.y)):
                    print "And Now I See the Light fuck"                
                    hasData = True 
        elif(direction == 90): 
            if(x > self.lightSource.x and self.correctOther(self.lightSource.y, y)):
                print "Lizzy fucked it. bitch"
                if(self.UltraSonicSensor.getData(position, direction) > abs(x-self.lightSource.x)):
                    print "And Now I See the Light bitch"                
                    hasData = True
        elif(direction == 180):
            if(y < self.lightSource.y and self.correctOther(self.lightSource.x, x)):
                print "Lizzy fucked it. twat"
                if(self.UltraSonicSensor.getData(position, direction) > abs(y-self.lightSource.y)):
                    print "And Now I See the Light twat"
                    hasData = True
        elif(direction == 270):
            if(x < self.lightSource.x and self.correctOther(self.lightSource.y, y)):
                print "Lizzy fucked it. dick"
                if(self.UltraSonicSensor.getData(position, direction) > abs(x-self.lightSource.x)):
                    print "And Now I See the Light dick"
                    hasData = True
        
        #returns intensity if seBehaviorControl as nsor is pointing "toward" light, else returns zero
        if(hasData):
            return self.lightSource.intensity(position)
        else:
            return 0
        
        def correctOther(self, lightSourceDir, robotDir):
            if((lightSourceDir - self.lightSource.oCR < robotDir) and (robotDir < lightSourceDir + self.lightSource.oCr )):
                return True
            return False
           
           

class UltraSonicSensor(abstractClass.Sensor):
    def __init__(self, walls,light):
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
        sight = 50.0
        
        #finds all walls in front of turtle
        for wall in self.walls:
            wall.color = (0,0,0,255)
            if(direction == 0 and y > wall.y):
                if(wall.x < x and x < wall.x + wall.width):
                    wallsInFront.append(wall)
            if(direction == 90 and x > wall.x):
                if(wall.y < y and y < wall.y + wall.height):
                    wallsInFront.append(wall)
            if(direction == 180 and y < wall.y):
                if(wall.x < x and x < wall.x + wall.width):
                    wallsInFront.append(wall)
            if(direction == 270 and x < wall.x):
                if(wall.y < y and y < wall.y + wall.height):
                    wallsInFront.append(wall)
                
     
        #if no walls in front
        #assumedly this will never happen if the world is properly bounded by walls
        if(len(wallsInFront) == 0):
            return 1
                    
        #pick closest wall
        if(len(wallsInFront)>1):
            #compares to last closest wall
            closestWall = wallsInFront[0]
            for wall in wallsInFront:
                wall.color = (0,255,255,255)
                if(direction == 0 and wall.y > closestWall.y+1):
                    closestWall = wall
                    
                elif(direction == 90 and wall.x > closestWall.x+1):
                    closestWall = wall
                    
                elif(direction == 180 and wall.y < closestWall.y):
                    closestWall = wall
                    
                elif(direction == 270 and wall.x < closestWall.x):
                    closestWall = wall

              
            wallToUse = closestWall
        #if only one wall
        elif(len(wallsInFront) == 1):
            wallToUse = wallsInFront[0]
        wallToUse.color = (0,255,0,255) 
        
        distance = self.distanceToWall(wallToUse,position,direction) #distance to wallToUse

        assert(distance != None),"UltraSonic: No distance returned"
        if(distance > sight):
            distance = sight #greatest noticable distance
        
        norm = distance/sight #normalized distance
        return norm
            
    def distanceToWall(self, wall,position,direction):
        """ Finds Distance to wall """
        x = position[0]
        y = position[1]
        if(direction == 0):
            if(y - (wall.y+wall.height)<5):
                print 'YOU THINK THIS IS A GAME?!?!?!?!?!?!'
                print y - (wall.y+wall.height)
            return y - (wall.y + wall.height)
        if(direction == 90):
            if(x - (wall.x + wall.width+1) < 5):
                print 'Ehhhhh sexy lady ;)'
                print x - (wall.x + wall.width)
            return x - (wall.x + wall.width)
        if(direction == 180):
            if((wall.y - y)<5):
                print 'COCAINE!!!!!!! FUCKERS'
                print wall.y - y
            return wall.y - y
        if(direction == 270):
            if((wall.x-x) < 5):
                print 'BEAT IT CLAIRE BEAT IT'
                print wall.x - x
            return wall.x - x 