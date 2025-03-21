# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agent import greenAgent
from object import Radioactivity

import random
class NuclearModel(Model):
    def __init__(
            self,
            width=10,
            height=10,
            n_green_agents=1,
            n_yellow_agents=1,
            n_red_agents=1,
            n_wastes=1,
            max_wastes=2,
            seed=None):
        super.__init__(seed=seed)

        self.width=width
        self.heigth=height
        self.n_green_agents=n_green_agents
        self.n_yellow_agents=n_yellow_agents
        self.n_red_agents=n_red_agents
        self.n_agents=n_green_agents+n_yellow_agents+n_red_agents
        self.n_wastes=n_wastes
        self.n_wastes_remaining=n_wastes
        self.max_wastes=max_wastes,
        self.red_wastes_remaining = 0
        self.yellow_wastes_remaining = 0
        self.green_wastes_remaining = 0
        self.obj_id=0
        
        self.grid = MultiGrid(width, height, True)

        agents = greenAgent.create_agents(model=self, n=n_green_agents)
        # Create x and y coordinates for agents
        x = self.rng.integers(0, self.grid.width, size=(n_green_agents+n_yellow_agents+n_red_agents,))
        y = self.rng.integers(0, self.grid.height, size=(n_green_agents+n_yellow_agents+n_red_agents,))

        for a, i, j in zip(agents, x, y):
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (i, j))

        # Créer les agents
        width_zone=self.width//3
        id, radio, model
        def initialize_zones(x1, x2, radio_range, env, id):
            for i in range(x1,x2):
                for j in range(self.height):
                    if i==self.width-1 and j == self.height:
                        a = Radioactivity(id, DESPOSIT_RADIOACTIVITY, env)
                    else:
                        a=Radioactivity(id,random.uniform(*radio_range),env)


    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step_agent")
        
def do (self, agent, action):
    return handle_action
    # IF ACTION == MOVE
    ## CHECK IF THE ACTION IS FEASIBLE
    …
    ## IF FEASIBLE, PERFORM THE ACTION
    agent.pos = …
    percepts = {pos1 : {contents of case at pos1},
    pos2 : {contents of tile at pos2},
    …}
    # IF ACTION = …
    …
    return percepts

