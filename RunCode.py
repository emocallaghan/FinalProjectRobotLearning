# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 12:22:24 2014

@author: cbeery
"""
import pygame
from pygame.locals import *
import time
from abc import ABCMeta, abstractmethod

from Models import virtualWorldITwo
from Controllers import behave
from Views import PygameTurtleViewer

        
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """
Running Code
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """
            
if __name__ == '__main__':
    pygame.init()

    size = (1000,700)
    screen = pygame.display.set_mode(size)
    model = virtualWorldITwo.Model(size,screen)
    view = PygameTurtleViewer.View(model,screen)
    controller = behave.Controller()    


    running = True
    
    startTime = time.time()
    xTime = time.time()
    
    sensed = model.robot.sensorPack.getSensorData()
    action = None
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
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
        
        time.sleep(.01)

    pygame.quit()