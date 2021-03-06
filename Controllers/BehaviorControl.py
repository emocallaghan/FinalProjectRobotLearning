# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 02:10:42 2014

@author: dmichael

"""
from random import randint

class Controller:
    def __init__(self):
        #Situational Abstractions

        self.abstract = [(0,0,0,'fwd'),
                         (0,0,0,'left'),
                         (0,0,0,'right'),
                         (0,0,1,'fwd'),
                         (0,0,1,'left'),
                         (0,0,1,'right'),
                         (0,0,2,'fwd'),
                         (0,0,2,'left'),
                         (0,0,2,'right'),
                         (0,1,1,'fwd'),
                         (0,1,1,'left'),
                         (0,1,1,'right'),
                         (0,1,2,'fwd'),
                         (0,1,2,'left'),
                         (0,1,2,'right'),
                         (0,1,0,'fwd'),
                         (0,1,0,'left'),
                         (0,1,0,'right'),
                         (1,0,0,'fwd'),
                         (1,0,0,'left'),
                         (1,0,0,'right'),
                         (1,0,1,'fwd'),
                         (1,0,1,'left'),
                         (1,0,1,'right'),
                         (1,0,2,'fwd'),
                         (1,0,2,'left'),
                         (1,0,2,'right'),
                         (1,1,1,'fwd'),
                         (1,1,1,'left'),
                         (1,1,1,'right'),
                         (1,1,2,'fwd'),
                         (1,1,2,'left'),
                         (1,1,2,'right'),
                         (1,1,0,'fwd'),
                         (1,1,0,'left'),
                         (1,1,0,'right'),
                         (2,0,0,'fwd'),
                         (2,0,0,'left'),
                         (2,0,0,'right'),
                         (2,0,1,'fwd'),
                         (2,0,1,'left'),
                         (2,0,1,'right'),
                         (2,0,2,'fwd'),
                         (2,0,2,'left'),
                         (2,0,2,'right'),
                         (2,1,1,'fwd'),
                         (2,1,1,'left'),
                         (2,1,1,'right'),
                         (2,1,2,'fwd'),
                         (2,1,2,'left'),
                         (2,1,2,'right'),
                         (2,1,0,'fwd'),
                         (2,1,0,'left'),
                         (2,1,0,'right')]
   
        #Situation Behaviors
        self.situations = []
        for scenario in self.abstract:
            self.situations.append(Situation( (scenario[0],scenario[1]) ))
            
        self.pasthappy = 0
        self.action = 'fwd'
        self.lastabstract = self.situations[self.abstract.index((0,0,0,'fwd'))]
        
    def clean(self,ir,touch,ultra):
        #ir
        if ir > .8:
            ir = 2
        elif ir > .2:
            ir = 1
        else:
            ir = 0           
        
        #Ultrasonic
        if ultra < .2:
            ultra = 0
        elif ultra < .8:
            ultra = 1
        else:
            ultra = 2   
            
        #sensorPack
        return (ir,touch, ultra)
                                                         #act on new try
    def update(self,sensors):
        if self.lastabstract  != None:

            if self.lastabstract is self.situations[2]:
                    print sensors
#        print ""
#        print sensors
        sensors = self.clean(sensors[0],sensors[1],sensors[2]) 
#        print sensors
        
        if self.lastabstract  != None:

            if self.lastabstract is self.situations[2]:
                print sensors
                print self.pasthappy  
                print self.lastabstract.actions
                print self.lastabstract.lastact                  
                    
            self.pasthappy = self.lastabstract.update((sensors[0],sensors[1]))#update last try
            
            if self.lastabstract is self.situations[2]:
                print self.lastabstract.ishappy((sensors[0],sensors[1]))
                print self.pasthappy 
                print self.lastabstract.actions
            
        #choose new try    
        self.lastabstract = self.situations[self.abstract.index((sensors[0],sensors[1],sensors[2],self.lastabstract.lastact))] 
        
        if self.lastabstract is self.situations[2]:
            print ""
            print sensors
        
        #act on new try        
        return self.lastabstract.act(),self.pasthappy   

class Situation:
    def __init__(self,sensors):
        self.actions = {'fwd':50, 'left':3, 'right': 3}
        self.lastact = 'fwd'
        self.happiness = self.ishappy(sensors)
        
            
    def act(self):
        temp = self.actions.copy()
        for act in temp:
            temp[act] = temp[act]*randint(1,20) 
        self.lastact = max(temp,key=temp.get)
#        print self.lastact
        return self.lastact # WHAT IF NONE RETURNED
        
    def ishappy(self,sensors):
        """ 
        denotes one of four results of action
        this will never change per situation as the sensor values
        determine the call of this scenario
        """        
        happinesses = {(2,0): 2,
                       (1,0): 1,
                       (0,0): 0,
                       (2,1):-1,
                       (1,1):-2,
                       (0,1):-3}                     
        return happinesses[sensors]    # WHAT IF NONE RETURNED
        
            
    def update(self,sensors):  
        current = self.ishappy(sensors)
        if self.lastact != None:  
            
            if self.happiness == current: #WHAT IF PAST MOST/LEAST HAPPY
                if current == -3:
                    self.actions[self.lastact] += -2
                elif current == 2:
                    self.actions[self.lastact] += 2
                else:
                    self.actions[self.lastact] -= 1
            elif self.happiness > current:
                self.actions[self.lastact] += -2
            elif self.happiness < current:
                self.actions[self.lastact] +=  2
            else:
                print "Dafuk?"
                
        return current