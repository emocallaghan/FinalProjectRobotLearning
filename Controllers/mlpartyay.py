# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 02:10:42 2014

@author: dmichael
"""
from random import *
class situations:
    def __init__(self ,pasthappyness,ir,touch):
        self.actiondict = {'fwd':5, 'left':5, 'right': 5}
        self.pasthappynes = pasthappyness
        self.ir = ir
        self.touch = touch
        self.lastact = 'forward'
    def act(self):
        temp = {}
        for keys in self.actiondict:
            temp.values = self.actiondict[keys]
        for values in temp:
            temp.values = temp.values*(randint(100,300)/100)
        self.lastact = max(temp,key=temp.get)
        return max(temp,key = temp.get)
    def ishappy(self):
        if self.ir >= .5 and self.touch == 0:
            return 2
        elif self.ir >= .5 and self.touch == 1:
            return 0
        elif self.ir < .5 and self.touch  == 0:
            return 1
        elif self.ir < .5 and self.touch == 1:
            return -2
    def dictupdat(self):
        if ishappy(self) == self.pasthappyness:
            pass
        elif ishappy(self) > self.pasthappynes:
            self.actiondict[lastact]+=1
        elif ishappy(self) < self.pasthappynes:
            self.actiondict[lastact]-=1
    def update(self):
        self.act(self)
        self.dictupdat(self)
        return self.ishappy(self)
    
class controller:
    def __init__(self, ir, touch):
        self.pasthappy = 0
        self.ir = ir
        self.touch
        self.situation1 = situations(self.pasthappy,self.ir,self.touch)
        self.situation2 = situations(self.pasthappy,self.ir,self.touch)
        self.situation3 = situations(self.pasthappy,self.ir,self.touch)
        self.situation4 = situations(self.pasthappy,self.ir,self.touch)
        self.situation5 = situations(self.pasthappy,self.ir,self.touch)
        self.situation6 = situations(self.pasthappy,self.ir,self.touch)
        self.situation7 = situations(self.pasthappy,self.ir,self.touch)
        self.situation8 = situations(self.pasthappy,self.ir,self.touch)
        
    def sortanddo(self):
        if ir > .5 and press == 0 and ultra < .5:
            pasthappy = self.situation1.update
        elif ir > .5 and press == 1 and ultra < .5:
            pasthappy = self.situation2.update
        elif ir <= .5 and press == 0 and ultra < .5:
            pasthappy = situation3.update
        elif ir <= .5 and press == 1 and ultra < .5:
            pasthappy = self.situation4.update
        elif ir > .5 and press == 0 and ultra >= .5:
            pasthappy = self.situation5.update
        elif ir > .5 and press == 1 and ultra >= .5:
            pasthappy = self.situation6.update
        elif ir <= .5 and press == 0 and ultra >= .5:
            pasthappy = self.situation7.update
        elif ir <= .5 and press == 1 and ultra >= .5:
            pasthappy = self.situation8.update

if __name__=='__main__':
    while running:
        ir = getir()
        touch = gettouch()
        ultra = getultra()
        controller.sortanddo()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

            