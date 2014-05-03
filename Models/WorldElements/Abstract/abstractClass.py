# -*- coding: utf-8 -*-
"""
Created on Fri May  2 12:18:16 2014

@author: cbeery
"""
import pygame
from pygame.locals import *
from abc import ABCMeta, abstractmethod

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
        assert(len(position) == 2),"Drawable Object Location not defined in 2D"
        self.x = position[0]
        self.y = position[1]
        
        
        assert(len(color) == 3 or len(color) == 4),"Drawable Object Color not defined in RGB or RGBa"
        if len(color) == 3:
            self.color = pygame.Color(color[0],color[1],color[2])
        else:
            self.color = color
        
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
    
class Sensor:
    __metaclass__ = ABCMeta
                     
    @abstractmethod
    def getData(self):
        pass
