# -*- coding: utf-8 -*-
"""
Created on Fri May  2 12:08:15 2014

@author: cbeery
"""

from WorldElements import Robot,Elements

class Model:
    """ 
    Encodes the world state of It's Learning: contains a turtle, a list of 
    walls, and a light
    """
    def __init__(self, boundarySize):
        """ contructor for the WorldModel class"""
        
        self.light = Elements.LEDRing([400,400]) #assumes not placed within 50v pixels of World's Edge
        self.myWalls = []
        
        self.createWorldMap(boundarySize)
        self.robot = Robot.Robot(self.myWalls,self.light)

    def createWorldMap(self, boundarySize):
        """
        Create wall borders around world, walls as obstacles denoted here
        INPUTS: boundarySize, (x,y) coordinate of lower righthand corner of screen
        """
        #Block World's Edge
        width = boundarySize[0]
        height = boundarySize[1]
        thickness = 20 #depth of border walls
                
        self.myWalls.append( Elements.Wall([thickness,0], [width-2*thickness,thickness])) #Ceiling
        self.myWalls.append( Elements.Wall([thickness,height-thickness], [width-2*thickness,thickness])) #Floor
        self.myWalls.append( Elements.Wall([width-thickness,thickness],[thickness,height-2*thickness])) #Right
        self.myWalls.append( Elements.Wall([0,thickness],[thickness,height-2*thickness])) #Left

        #Create World Obstacles
    def createWalls(self,position, dimensions):       
        self.myWalls.append( Elements.Wall(position, dimensions) )
        
    def update(self, action):
        self.robot.update(action)
        return self.robot.sensorPack.getSensorData()