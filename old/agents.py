# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa.datacollection import DataCollector
from mesa import Agent, Model

from model import NuclearModel
def update(knowledge, percepts, actions):
    if percepts:
        knowledge["percepts"].append(percepts)
    if actions:
        knowledge["actions"].append(actions)

class NuclearAgent(Agent):
    def __init__(self, model : NuclearModel, color):
        super.__init__(model)
        self.color = color
        self.knwoledge = {
            "percepts" : [],
            "actions" : [],
            "max_waste" : self.model.max_wastes,
            "last_pos" : (0,0),
            "grid_width" : self.model.width,
            "grid_heigth" : self.model.heigth
        }
        
        self.percept={
            "radioactivity" : 0,
            "wastes" : [],
            "pos" : (0,0),
            "surrounding" : []
        }

        self.action = 0
        self.step_count = 0
    
    def deliberate(self):
        pass
    
    def last_percept(self):
        return self.percept

    def step_agent(self):
        update(self.knowledge, self.percept, self.action)
        action = self.deliberate()
        self.action = action
        self.percept = self.model.do(self, action)


    