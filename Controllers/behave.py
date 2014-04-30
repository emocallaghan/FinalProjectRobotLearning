# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 02:10:42 2014

@author: dmichael

Edited on Wed Apr 30 01:27 2014

@editor: cbeery
"""

from random import randint
class Situation:
    def __init__(self,sensors):
        self.actions = {'fwd':5, 'left':5, 'right': 5}
        self.lastact = None
        self.happiness = None
        self.ishappy(sensors)
            
    def act(self):
        temp = self.actions.copy()
        for act in temp:
            temp[act] = temp[act]*randint(1,3) 
        self.lastact = max(temp,key=temp.get)
        
        return self.lastact # WHAT IF NONE RETURNED
        
    def ishappy(self,sensors):
        """ 
        denotes one of four results of action
        this will never change per situation as the sensor values
        determine the call of this scenario
        """        
        happinesses = {(1,0): 2,
                       (1,1): 0,
                       (0,0): 1,
                       (0,1):-1}                     
        self.happiness = happinesses[sensors]    # WHAT IF NONE RETURNED
        
            
    def update(self,past,pleasure,pain):  
        if self.lastact != None:
            if self.happiness == self.past: #WHAT IF PAST MOST/LEAST HAPPY
                pass
            elif self.happiness > past:
                self.actions[self.lastact] += 1
            elif self.happiness < past:
                self.actions[self.lastact] -= 1
            else:
                print "Dafuk?"
                
        return self.happiness
    
class Controller:
    def __init__(self):
        #Situational Abstractions
        self.abstract = [(1,0,0),
                         (1,1,0),
                         (0,0,0),
                         (0,1,0),
                         (1,1,0),
                         (1,1,1),
                         (0,0,1),
                         (0,1,1)]            
          
        #Situation Behaviors
        self.situations = []
        for scenario in self.abstract:
            self.situations.append(Situation())
            
        self.pasthappy = 0
        self.action = None
        self.lastabstract = None
        
    def clean(self,ir,touch,ultra):
        #ir
        if ir > .5:
            ir = 1
        else:
            ir = 0           
        #Ultrasonic
        if ultra < .5:
            ultra = 0
        else:
            ultra = 1          
        #sensorPack
        return (ir,touch,ultra)
        
    def update(self,ir,touch,ultra):
        sensors = self.clean(ir,touch,ultra)                                
        self.pasthappy = self.lastabstract.update(self.pasthappy,(sensors[0],sensors[1]))#update last try
        self.lastabstract = self.situations[self.abstract.index(sensors)]                #choose new try
        return self.lastabstract.act()                                                   #act on new try

            