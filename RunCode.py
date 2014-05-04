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

""" """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """
Running Code
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """
            
if __name__ == '__main__':
    #THIS IS PYGAME!!! not sparta
    pygame.init()

    """__________Initiates Class Objects and Umbrella Variables___________"""

    #Creates display surface
    graphSize = 120
    size = (1500,800)
    screen = pygame.display.set_mode(size) 
    
    #Virtual World and Active
    model = VirtualWorld3.Model(size,graphSize)
    controller = behave.Controller()
   
    #Creates objects to see and modify virtual world
    view = PygameTurtleViewer.View(model,screen,graphSize)
    editor = EditTurtleWorld.WorldEditor(model,screen)

    #denote if pygame screen should be visible
    running = True
    
    #Creates storage for subsystem transfers
    sensed = model.robot.sensorPack.getSensorData() 
    action = None
    
    """____________Turtle Explores and Learns the Consequences____________"""
    
    while running:
        for event in pygame.event.get():
            #End of World Conditions
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            editor.update(event)
        """
        The window to paradise is fluid, allowing us to bear it witness
        """        
        view.draw()
        """
        No one owns the world; they can but precieve some small subreality, 
        """
        action,happy = controller.update(sensed)
        """
        yet the world must have changed by your choice, little devil
        """
        sensed = model.update(action)
        """
        Happy, sad, or full of pride: Bury that feeling in memory
        """
        view.happyGrapher.addHappiness(happy)
        
        # Print to terminal/spider window  
#        print happy
#        print action

        # Slow down, and enjoy the moment
        time.sleep(.01)
        
        
    """_________________Pleasure and Pain for All to See__________________"""
    
    running = True
    
    #Analyze happiness record and graph behavior
    view.happyGrapher.happyGraph()
    
    #Display Graph until End of World
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == pygame.K_ESCAPE:
                running = False
    
    
    pygame.quit() #You don't have to go home but you can't stay here