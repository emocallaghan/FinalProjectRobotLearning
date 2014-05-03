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
    def __init__(self, position,radius=10,color=(0,255,255,70)):
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
        
        #outer circle
        oCR = int(0.8*self.range)
        outerCircle = pygame.Surface((oCR*2,oCR*2))
        pygame.draw.circle(outerCircle, self.color, (oCR, oCR), oCR)
        outerCircle.set_colorkey((0,0,0))
        assert(len(self.color) == 4),"no alpha value for light"
        outerCircle.set_alpha(self.color[3])                        
        screen.blit(outerCircle, (self.x-oCR,self.y-oCR)) 
        
        #innercircle
        iCR = int(0.3*self.range)
        innerCircle = pygame.Surface((iCR*2,iCR*2))
        pygame.draw.circle(innerCircle, self.color, (iCR, iCR), iCR)
        innerCircle.set_colorkey((0,0,0))
        assert(len(self.color) == 4),"no alpha value for light"
        innerCircle.set_alpha(self.color[3])                        
        screen.blit(innerCircle, (self.x-iCR,self.y-iCR)) 
        

        
        #source
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
        rect = pygame.Surface((self.width,self.height))  
        assert(len(self.color) == 4),"no alpha value for wall"
        rect.set_alpha(self.color[3])                
        rect.fill((self.color[0],self.color[1],self.color[2]))          
        screen.blit(rect, (self.x,self.y))    
        