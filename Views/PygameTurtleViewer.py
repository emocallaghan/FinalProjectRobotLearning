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
        self.happyGrapher = HappinessGrapher(screen)
        
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
    def __init__(self,screen):
        self.screen = screen
        self.happinessMem = []
              
    def addHappiness(self,happy):        
        self.happinessMem.append(happy)
        
    def happyGraph(self):
        print len(self.happinessMem)
        size = self.screen.get_size()
        
        padding = 50
        barWidth = 50.0
        
        graphsize = (size[0]-2*padding,size[1]-2*padding)
        num_bars = int(graphsize[0]/barWidth)
        bar_sample_size = int(len(self.happinessMem)/num_bars) 
        print "# of samples per bar = ", 
        print bar_sample_size
        miniList = []
        for mini in range(0,len(self.happinessMem)-bar_sample_size, bar_sample_size):
            sumBar = 0
            print "mini = ",
            print mini
            for barVal in range(0, bar_sample_size-1):
                sumBar += self.happinessMem[mini+barVal]
            sumBar = sumBar
            miniList.append(sumBar)
            
        graph = pygame.Surface(graphsize) 
        graph.fill((50,0,50,255))
        high = max(miniList)
        low = min(miniList)
        
        for bar in range(len(miniList)):
            normBar = (miniList[bar]+ abs(low)) / (high+abs(low))
            scaledBar = int(normBar*graphsize[1])
            print ""
            print bar
            print graphsize[0]*bar,
            print graphsize[1] - scaledBar,
            print int(barWidth),
            print scaledBar
            pygame.draw.rect(graph, (0,255,255,255),(graphsize[0]*bar,graphsize[1] - scaledBar,int(barWidth),scaledBar) )
        
        self.screen.fill((0,0,0,255))
        self.screen.blit(graph, (padding,padding)) 
        
        pygame.display.update()   
                
        
