# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 12:22:24 2014

@author: cbeery
"""
import pygame
from pygame.locals import *
import time

from Models import VirtualWorld3
from Controllers import behave, EditTurtleWorld
from Views import PygameTurtleViewer

        
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """
Running Code
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """
            
if __name__ == '__main__':
    pygame.init()

    size = (1000,700)
    screen = pygame.display.set_mode(size)
    
    model = VirtualWorld3.Model(size)
    controller = behave.Controller() 
    
    view = PygameTurtleViewer.View(model,screen)
    editor = EditTurtleWorld.WorldEditor(model,screen)

    running = True
    
    sensed = model.robot.sensorPack.getSensorData()
    action = None
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            editor.update(event)
        
        view.draw()
        """
        instead of having thecontroller own the model, it is given some of 
        the model data to work with
        """
        action = controller.update(sensed)
        """
        in turn, the model is informed of the choice made
        """
        sensed = model.update(action)
        """
        the view of hte model is updated for our viewing pleasure
        """
        
        time.sleep(.05)

    pygame.quit()