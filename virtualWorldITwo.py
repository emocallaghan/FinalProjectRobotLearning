# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 23:41:48 2014

@author: eocallaghan
"""

import pygame
from pygame.locals import *
import time
from abc import ABCMeta, abstractmethod

class Sensor:
    __metaclass__ = ABCMeta
    def __init__(self, initialPos, direction):
        self.x = initialPos(0)
        self.y = initialPos(1)
        self.direction = direction
    @abstractmethod
    def getData(self):
        pass
    def update(self,position,direction):
        self.x = position(0)
        self.y = position(1)
        self.direction = direction

class IRSensor(Sensor):
    def __init__(self, initalPos, direction, lightSource):
        super(IRSensor,self).__init__(initalPos, direction)
        self.lightSource = lightSource
        
    def getData(self):
        hasData = False
        if(self.direction == 0):
            if(self.y > self.lightSource.y):
                hasData = True
        elif(self.direction == 90):
            if(self.x > self.lightSource.x):
                hasData = True
        elif(self.direction == 180):
            if(self.y < self.lightSource.y):
                hasData = True
        elif(self.direction == 270):
            if(self.x < self.lightSource.x):
                hasData = True
        if(hasData):
            return self.lightSource.intesity()
        else:
            return 0
            
class UltraSonicSensor(Sensor):
    def __init__(self, initalPos, direction, walls):
        super(UltraSonicSensor,self).__init__(initalPos, direction)
        self.walls = walls
    
    def getData(self):
        wallsInFront = []
        wallToUse = walls[0]
        for wall in self.walls:
            if(self.direction == 0 and self.y > wall.y):
                wallInFront.append(wall)
            if(self.direction == 90 and self.x > wall.x):
                wallInFront.append(wall)
            if(self.direction == 180 and self.y < wall.y):
                wallInFront.append(wall)
            if(self.direction == 270 and self.x < wall.x):
                wallInFront.append(wall)
        if(len(wallsInFront) == 0):
            return 1
        if(len(wallsInFront)>1):
            closestWall = wallInFront[0]
            for wall in wallsInFront:
                if(self.direction == 0 and wall.y > closestWall.y):
                    closestWall = wall
                elif(self.direction == 90 and wall.x > closestWall.x):
                    closestWall = wall
                elif(self.direction == 180 and wall.y < closestWall.y):
                    closestWall = wall
                elif(self.direction == 270 and wall.x < closestWall.x):
                    closestWall = wall
            wallToUse = closestWall
        elif(len(wallsInFront) == 1):
            wallToUse = wallsInFront[0]
        distance = self.distanceToWall(wallToUse)
        if(distance > 300):
            distance = 300
        norm = distance/300.0
        return norm
        
            
    def distanceToWall(wall):
        if(self.direction == 0):
            return self.y - (wall.y + wall.height)
        if(self.direction == 90):
            return self.x - (wall.x + wall.width)
        if(self.direction == 180):
            return wall.y - self.y
        if(self.direction == 270):
            return wall.x - self.x
            
class TouchSensor(Sensor):
    def __init__(self,position,direction,walls):
        super(touchSensor,self).__init__(position,direction)
        self.walls = walls
    
    def getData(self):
        for wall in walls:
            return self.isTouching(wall)

    def isTouching(self,wall):
        return self.betweenX(wall) and self.betweenY(wall)        
        
    def betweenX(self,wall):
        return (wall.x <= self.x) and (self.x <= wall.x + wall.width)
        
    def betweenY(self,wall):
        return (wall.y <= self.y) and(self.y <= wall.y + wall.height)
        
class LedRing:
    def __init__(self, position):
        self.x = position(0)
        self.y = position(1)
        
    def intestity(self, measurePosition):
        deltax = measurePosition(0)-self.x
        deltay = measurePosition(1)-self.y
        distance = (deltax**2+deltay**2)**.5
        distanceReverseMap = 160 - distance
        if(distanceReverseMap < 0):
            distanceReverseMap = 0
        norm = distanceReverseMap/160.0
        return norm
        
        
        
class Wall:
    def __init__(self,position, dimensions, color):
        self.x = position(0)
        self.y = position(1)
        self.height = dimensions(0)
        self.width = dimensions(1)
        self.color = color
        
    def betweenX(self, x):
        return (self.x <= x) and (x <= self.x + self.width)
    
    def betweenY(self, y):
        return (self.y <= y) and (y <= self.y + self.height)
        
class Robot:
    def __init__(self, walls, lightSource):
        self.x = 400
        self.y = 600
        self.radius = 40
        self.color = pygame.Color(170,50,255)
        self.front = (self.x,self.y-self.radius)
        self.direction = 0
        self.walls = walls

        self.irSensor = IRSensor(self.front, self.direction, lightSource)
        self.ultrasonicSensor = UltraSonicSensor(self.front, self.direction, walls)
        self.touchSensor = TouchSensor(self.front, self.direction, walls)
        
        
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
        elif(self.direction == 90):
            self.x += -1
        elif(self.direction == 180):
            self.y += 1
    
    def left(self):
        pass
    
    def right(self):
        pass
    
    def checkCollision(self):
        for wall in walls:
            if(wall.betweenX(self.front(0)) and wall.betweenY(self.front(1))):
                return True
        return False
    
    def getIR(self):
        self.irSensor.getData()
    
    def getUltra(self):
        self.ultrasonicSensor.getData()
    
    def getTouch(self):
        self.touchSensor.getData()
    
        
        