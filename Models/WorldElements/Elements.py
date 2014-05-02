# -*- coding: utf-8 -*-
"""
Created on Fri May  2 12:28:14 2014

@author: cbeery
"""

import pygame
from pygame.locals import *
from Abstract import abstractClass

class LEDRing(abstractClass.Drawable):
    """provides a light source in the world: includes a constructor and an intensity(distance) evaluator"""
    def __init__(self, position,radius=10,color=(0,255,255)):
        """
        constructor for LED class
        ATTRIBUTES: "position", (x,y) coordinates of center of LED
                    radius, radius of LED
                    color, RGB of LED, defaults as cyan
        """
        super(LEDRing,self).__init__(position,[radius,None],color)
        self.range = 300
        
    def intensity(self, measurePosition):
        deltax = measurePosition[0]-self.x
        deltay = measurePosition[1]-self.y
        distance = (deltax**2+deltay**2)**.5
        distanceReverseMap = self.range - distance
        if(distanceReverseMap < 0):
            distanceReverseMap = 0
        norm = distanceReverseMap/self.range
        return norm
        
    def draw(self,screen):
        """draws LED ring  as a circle"""
        pygame.draw.circle(screen, (0,255,255,100), (self.x, self.y), int(0.8*self.range),1)
        pygame.draw.circle(screen, (0,255,255,200), (self.x, self.y), int(0.3*self.range),3)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
        
class Wall(abstractClass.Drawable):
    """provides a walls in the world: includes a constructor and a collision evaluator"""
    def __init__(self,position, dimensions, color=(0,0,0)):
        """
        constructor for Wall class
        ATTRIBUTES: "position", (x,y) coordinates of upper lefthand corner of wall
                    "dimensions", (x,y) length of wall
                    color, RGB of wall, defaults as black
        """
        super(Wall,self).__init__(position,dimensions,color)

    def betweenX(self, x):
        return (self.x <= x) and (x <= self.x + self.width)
    
    def betweenY(self, y):
        return (self.y <= y) and (y <= self.y + self.height)
        
    def draw(self,screen):
        """draws wall as a rectangle"""
        rectangle = pygame.Rect(self.x,self.y,self.width,self.height)
        pygame.draw.rect(screen, self.color, rectangle)       