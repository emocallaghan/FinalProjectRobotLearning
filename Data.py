# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 16:13:34 2014

@author: cbeery
"""

#current implimentation uses stmem of depth 1 (+1 current)and used simply for storing last processed data set before annotation


class Data:
    
    def init(self, memory_length):
        self.MEMORY_LENGTH = memory_length #number of data sets in memory
        self.history = {} #all past data sets and annotations thereof
        
        self.raw = ["Touch", "IR", "UltraSonic", "LastMotorBehavior"] #latest raw data from environment
        self.pData = [] #processed data of appropraite new order
        self.memory = [] #nested list of processed data in "short term" memory
        
        self.populateInitialDataSet()


    def pullEnvironment(self):
        """ Retrieve data from environment """
    
    def populateInitialDataSet(self):
        """ Create an initial set of data/mem before doing actions """
    
    def processData(self, order exponentials):
    """ Change raw data into appropriate order (increase curve complexity) """ 
    
    def annotate(self):
    """ Add annotations to data """

    def updateMemory(self):
    """ Adds newest data set to memory and removes oldest """
    
    def addToHistory(self):
    """ Adds old set (with annotation) to history """
   
   def update(self):
       #for instance studies:
       #annonate last data set and add to history before updating memory!!!!
       #else you will erase data needing annotating

      


if __name__ == '__main__':
          

    
  

     
    