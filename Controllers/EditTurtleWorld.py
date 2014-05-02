# -*- coding: utf-8 -*-
"""
Created on Fri May  2 12:49:42 2014

@author: cbeery
"""
import pygame
from pygame.locals import *

class WorldEditor:
    def __init__(self,model,screen):
        self.screen = screen
        self.model = model
        self.creatingWall = False
        self.draggingLight = False
        self.firstFrame = True
        
    def LightDrag(self,x,y):
        self.model.light.x = x
        self.model.light.y = y

    def update(self,event):
        
        x,y = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:        
            if self.screen.get_at((x,y)) == self.model.light.color:
                self.draggingLight = True
            else: 
                self.creatingWall = True
                
        if event.type  == MOUSEBUTTONUP:
            self.draggingLight = False
            self.creatingWall = False
        
        if self.draggingLight == True:
            self.LightDrag(x,y)
