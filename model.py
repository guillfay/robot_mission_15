# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import greenAgent

class NuclearModel(Model):
    def __init__(
            self,
            width=10,
            height=10,
            n_green_agents=1,
            n_yellow_agents=0,
            n_red_agents=0,
            n_wastes=1,
            seed=None):
        super.__init__(seed=seed)
        self.width=width
        self.heigth=height
        self.n_green_agents=n_green_agents
        self.n_yellow_agents=n_yellow_agents
        self.n_red_agents=n_red_agents
        self.n_agents=n_green_agents+n_yellow_agents+n_red_agents
        self.n_wastes=n_wastes
        self.wastes_remaining=n_wastes
        
        self.grid = MultiGrid(width, height, True)

        agents = greenAgent.create_agents(model=self, n=n_green_agents)
        # Create x and y coordinates for agents
        x = self.rng.integers(0, self.grid.width, size=(n_green_agents+n_yellow_agents+n_red_agents,))
        y = self.rng.integers(0, self.grid.height, size=(n_green_agents+n_yellow_agents+n_red_agents,))

        for a, i, j in zip(agents, x, y):
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (i, j))

        init_agent


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

