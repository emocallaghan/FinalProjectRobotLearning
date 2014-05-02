# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 15:23:47 2014

@author: cbeery
"""
from math import exp
from random import randrange

class Neural_Network():
    
    def __init__(self, num_layers, neuronsPerLayer):
        self.a = 0.02   #learningRate
        self.B = 0.6    #momentum       
        
        self.hypotheses = [] #list of hypotheses, form [[first layer],[secondLayer],...,[scenarios]]
        self.chosen = None #keeps track of the most resently chosen scenario
        self.scenarioProb = []
        
        self.createHiddenLayers(num_layers,neuronsPerLayer)
    
    def createHiddenLayers(self,num_layers,neuronsPerLayer):
        """ 
        Creates the framework of network by populating self.hypotheses 
        INPUTS: num_layers, number of hidden and output layers in network
                neuronsPerLayer, number of hypotheses in each hidden layer
                        assumes each layer will have same number
        """
        assert(not len(self.hypotheses)), "You Fool! Network already initilized?!"
        
        for layer in range(num_layers - 1):
            hiddenLayer = []
            for term in range(neuronsPerLayer):
                hiddenLayer.append(HiddenNeuron(neuronsPerLayer)) #create HiddenLayerInstance
            self.hypothesis.append(hiddenLayer) 
        self.hypothesis.append([]) #adds empty scenario list
        
        assert(len(self.hypotheses) >= num_layers),"Hidden Layers not successfully created"
        assert(len(self.hypotheses) == num_layers),"Scenario Layer not successfully created"
        
    def chooseScenario(self,nData):
        """
        Updates self.chosen by picking from list of scenarios or creates new scenario 
        INPUTS: nData, expanded and normalized data of current environment, list
        """
        cutOff = 0.3 #denotes needed probablity of a situation to be in a scenario
        self.scenarioProb = self.evaluateNetwork(nData)
        assert(len(self.scenarioProb[-1]) == len(self.hypotheses[-1])),"chooseScenario: number of predictions and number of scenarios differ"

        scenarioKey = max( range(len(self.scenarioProb[-1])), key=self.scenarioProb[-1].__getitem__ )
        
        if self.scenarioProb[-1][scenarioKey] > cutOff:
            self.chosen = self.hypotheses[-1][scenarioKey]
        else:
            self.chosen = self.addHypothesis()
    
    def evaluateNetwork(self, nData):
        """ Find outputs of Scenarios """
        currentLayerData = list(nData)
        results = []
        for layer in self.hypotheses:
            nextLayerData = []
            for hypothesis in layer:               
                nextLayerData.append( hypothesis.evaluate(nData) )
            currentLayerData = list(nextLayerData)
            results.append(nextLayerData)
        return results

    def addHypothesis(self):
        """
        Creates a new hypothesis, adds scenario to hypotheses 
        of network 
        OUTPUT: created hypothesis
        """
        pass
    
    def update(self,nData):
        """ Runs back propagation to update the network weights """
        #outputLayer      
        for hIdx in range(len(self.hypotheses[-1])):
            if self.hypotheses[-1][hIdx] is self.chosen:
                desired = 1
            else:
                desired = 0
            output = self.scenarioProb[-1][hIdx]
            delta = (output-desired)**2
            self.hypotheses[-1][hIdx].error = delta
            
        #hiddenLayers
        for rLayerIdx in list( reversed(range(len(self.hypotheses)-1)) ):
            for hIdx in range(len(self.hypotheses[rLayerIdx])):                 
                weightErrorSum = 0
                for dependant in self.hypotheses[rLayerIdx +1]:
                    weightErrorSum += dependant.thetas[hIdx]*dependant.error                   
                output = self.scenarioProb[rLayerIdx][hIdx]    
                delta = output*(1-output)*weightErrorSum
                self.hypotheses[rLayerIdx][hIdx].error = delta
        
        #updateWeights
        
       
class Hypothesis:
    def __init__(self,num_layer_inputs):
        self.thetas = [] #list of weights
        self.error = None
        constructDefaultTheta(num_layer_inputs)
    
    def __str__(self):
        pass
    
    def update(self):
        pass 

       
    def constructDefaultTheta(self,num_layer_inputs):
           """ Initialize theta to historical cases """
        
        # Populates self.thetas with random values between 1 and 0
        for theta in range(num_layer_inputs+1):
            self.thetas.append( randrange(-5, 5) / 10.0 )
            
        descendInBunch() ######### not created yet ##########
    

    def evaluate(self, nData):
        """ 
        Evaluates the sigmoid of the sum of the weighted parameters
        INPUTS: nData, expanded and normalized data of current environment, list
        OUTPUT: sigmoid, value of sigmoid, value
        Attr_Dependant: self.thetas, list
        """
        x = [-1]  #initialize with bias term
        x.extend(nData) #creates complete input set
        assert ( len(x) == len(self.thetas) ), "Hypothesis.evaluate: number of weights does not match number of inputs (+ bias term)"    
        
        z = sum( parameter*weight for parameter,weight in zip(x,self.theta) ) #sigmoid input
        sigmoid = (1 + exp(-z))**(-1) 
        assert ( sigmoid > 0 and sigmoid < 1 ), "Sigmoid Function Value !E (0,1)"
        
        return sigmoid    

class HiddenNeuron(Hypothesis): 
 
    def __init__(self,num_layer_inputs):
         super(HiddenNeuron,self).__init__(num_layer_inputs)
         
    def __str__(self):
         return "I'm a hidden layer"
      
class Scenario(Hypothesis):
    
    def __init__(self,num_layer_inputs, behavior=None):
        super(Scenario,self).__init__(num_layer_inputs)
        self.behavior = behavior
        self.behaviorList = []

        self.createBehaviorList()
  
        if self.behavior == None:
            self.chooseBehavior()
        
       
    def chooseBehavior(self):
        """ Updates action choice based on last use """
        self.createBehaviorList()
 
        assert(len(self.behaviorList) > 0),"Behavior List is empty: Robot has nothing he can do!!"
        
        ## Duncan ##
    
    def createBehaviorList(self):
        """ Creates an initial list of allowed behaviors in the proper quantities """
        
        ## Duncan ##
      
if __name__ == '__main__':