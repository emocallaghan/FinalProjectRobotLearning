# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 11:56:52 2014

@author: cbeery
"""
import pygame
from pygame.locals import *
        
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
                                View
"""  """  """  """  """  """  """  """  """  """  """  """  """  """  """
class View:
    """ A view of Turtle's World rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        """ draws all of the elements on the screen by calling draw function of model objects"""
        self.screen.fill(pygame.Color(255,255,255))
        for wall in self.model.myWalls:
            wal.draw(self.screen)
        self.model.light.draw(self.screen)
        self.model.robot.draw(self.screen)
              
        pygame.display.update()
       

        
