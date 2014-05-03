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

#Somewhere here or in the above DATA should be imported

        
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """
Running Code
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """
            
if __name__ == '__main__':
    pygame.init()

    size = (400,600)
    screen = pygame.display.set_mode(size)
    
    model = VirtualWorld3.Model(size)
    controller = behave.Controller()
#    data = 
    
    view = PygameTurtleViewer.View(model,screen)
    editor = EditTurtleWorld.WorldEditor(model,screen)

    running = True
    
#    inizalize first sent of data
    sensed = model.robot.sensorPack.getSensorData() #<---depth 1, reaction only
    action = None
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            editor.update(event)
        """
        the view of hte model is updated for our viewing pleasure
        """        
        view.draw()
        """
        instead of having thecontroller own the model, it is given some of 
        the model data to work with
        """
        action,happy = controller.update(sensed)
        """
        in turn, the model is informed of the choice made
        """
        sensed = model.update(action)

        view.happyGrapher.addHappiness(happy)
        print happy
        print action
        time.sleep(.05)
        
    running = True
    view.happyGrapher.happyGraph()
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == pygame.K_ESCAPE:
                running = False
        time.sleep(.01)
    
    
    pygame.quit()