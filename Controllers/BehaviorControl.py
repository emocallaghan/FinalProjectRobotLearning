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
        self.lastabstract = self.situations[0]
        
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
        
    def update(self,sensors):
        
#        print ""
#        print sensors
        sensors = self.clean(sensors[0],sensors[1],sensors[2])                             
        self.pasthappy = self.lastabstract.update(self.pasthappy,(sensors[0],sensors[1]))#update last try
        self.lastabstract = self.situations[self.abstract.index((sensors[0],sensors[1],sensors[2],self.lastabstract.lastact))]      #choose new try
#        print self.abstract.index(sensors)
        return self.lastabstract.act(),self.pasthappy                                                  #act on new try


class Situation:
    def __init__(self,sensors):
        self.actions = {'fwd':5, 'left':3, 'right': 3}
        self.lastact = 'fwd'
        self.happiness = None
        self.ishappy(sensors)
            
    def act(self):
        temp = self.actions.copy()
        for act in temp:
            temp[act] = temp[act]*randint(1,3) 
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
                       (2,1): 0,
                       (1,1):-1,
                       (0,1):-2}                     
        self.happiness = happinesses[sensors]    # WHAT IF NONE RETURNED
        
            
    def update(self,past,(pleasure,pain)):  
        if self.lastact != None:            
            if self.happiness == past: #WHAT IF PAST MOST/LEAST HAPPY
                if past == -2:
                    self.actions[self.lastact] -= 1
                elif past == 2:
                    self.actions[self.lastact] += 1
                else:
                    pass
            elif self.happiness > past:
                self.actions[self.lastact] += 1
            elif self.happiness < past:
                self.actions[self.lastact] -= 1
            else:
                print "Dafuk?"
                
        return self.happiness
    

            