# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa.datacollection import DataCollector
from mesa import Agent, Model

def update(knowledge, percepts, actions):
    if percepts:
        knowledge["percepts"].append(percepts)
        knowledge["actions"].append(actions)


class Action():

class greenAgent(Agent):
    def __init__(self, model):
        super.__init__(model)
        self.color = "green"
        self.knwoledge = {
            "percepts" : [],
            "actions" : [],
            "max_waste" : 2,
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



# class yellowAgent(Agent):
#     def __init__(self, model):
#         super.__init__(model)
# class redAgent(Agent): 
#     def __init__(self, model):
#         super.__init__(model)

    def step_agent (self):
        update(self.knowledge, self.percept, self.action)
        action = self.deliberate()
        self.action = action
        self.percept = self.model.do(self, action)


    