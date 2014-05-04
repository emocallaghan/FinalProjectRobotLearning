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
    def __init__(self,model,screen,graph):
        self.model = model
        self.screen = screen
        self.graph = graph
        self.happyGrapher = HappinessGrapher(screen,graph)
           
    def draw(self):
        """ draws all of the elements on the screen by calling draw function of model objects"""
        self.screen.fill(pygame.Color(255,255,255))
        for wall in self.model.myWalls:
            wall.draw(self.screen)
        self.model.light.draw(self.screen)
        self.model.robot.draw(self.screen)
        
        if self.model.preWall:
            self.model.preWall.draw(self.screen)
              
        pygame.display.update()
       
       
class HappinessGrapher:
    def __init__(self,screen,graph):
        self.screen = screen
        self.graph = graph
        self.padding = 50
        self.tempMem = [0] * self.padding
        self.happinessMem = []       
              
    def addHappiness(self,happy):        
        self.happinessMem.append(happy)
    
    def movingGraph(self):
        size = self.graph.get_size()
        
        padding = 50
        graphsize = (size[0]-2*padding,size[1]-2*padding)
        
        
        
        
        
        a.insert(0, 7)
         
    
    def happyGraph(self):
        size = self.screen.get_size()
        
        padding = self.padding
        barWidth = 3.0
        
        graphsize = (size[0]-2*padding,size[1]-2*padding)
        num_bars = int(graphsize[0]/barWidth)
        bar_sample_size = int(len(self.happinessMem)/num_bars) 
        miniList = []
        for mini in range(0,len(self.happinessMem)-bar_sample_size, bar_sample_size):
            sumBar = 0
            for barVal in range(0, bar_sample_size-1):
                sumBar += self.happinessMem[mini+barVal]
            sumBar = float(sumBar)/bar_sample_size
            miniList.append(sumBar)
            
        graphPlus  = pygame.Surface((graphsize[0],int(graphsize[1]/2))) 
        graphMinus = pygame.Surface((graphsize[0],int(graphsize[1]/2)))
        
        graphPlus.fill((50,0,50,255))
        graphMinus.fill((50,0,50,255))
        
        mag = max([abs(x) for x in miniList])
        norm = [ int( (float(x)/float(mag))*(graphsize[1]/2) ) for x in miniList]
        
        for bar in range(len(miniList)):
            x = barWidth*bar
            width = int(barWidth)
            height = abs(norm[bar])
            if norm[bar] > 0:        
                y = int(graphsize[1]/2) - norm[bar]
                pygame.draw.rect( graphPlus, (0,255,255,255),(x,y,width,height) )
            elif norm[bar] < 0:
                y = 0
                pygame.draw.rect( graphMinus, (200,0,0,200),(x,y,width,height) )
            else:
                pass
            
        self.screen.fill((50,0,50,255))
        self.screen.blit(graphPlus, (padding,padding)) 
        self.screen.blit(graphMinus,(padding,padding + int(graphsize[1]/2)))
        
        pygame.display.update()   
                
        
