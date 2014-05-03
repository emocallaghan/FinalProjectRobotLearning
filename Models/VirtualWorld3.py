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
        self.preWall = None

    def createWorldMap(self, boundarySize):
        """
        Create wall borders around world, walls as obstacles denoted here
        INPUTS: boundarySize, (x,y) coordinate of lower righthand corner of screen
        """
        #Block World's Edge
        width = boundarySize[0]
        height = boundarySize[1]
        thickness = 20 #depth of border walls
                
        self.myWalls.append( Elements.Wall([0,0], [width-thickness,thickness])) #Ceiling
        self.myWalls.append( Elements.Wall([thickness,height-thickness], [width-thickness,thickness])) #Floor
        self.myWalls.append( Elements.Wall([width-thickness,0],[thickness,height-thickness])) #Right
        self.myWalls.append( Elements.Wall([0,thickness],[thickness,height-thickness])) #Left

        #Create World Obstacles
    def createWalls(self,position, dimensions):       
        self.myWalls.append( Elements.Wall(position, dimensions) )
        
    def createPreWall(self,position,dimensions):
        self.preWall =  Elements.Wall(position, dimensions,(200,0,0,200))
        
    def update(self, action):
        self.robot.update(action)
        return self.robot.sensorPack.getSensorData()