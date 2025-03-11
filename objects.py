# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Agent, Model
from model import NuclearModel
class Radioactivity(Agent):
    def __init__(self, model : NuclearModel, zone : str, radioactivity : float):
        super.__init__(model)
        self.zone = zone
        self.radioactivity = radioactivity

class Waste(Agent):
    def __init__(self, model : NuclearModel, zone : str):
        super().__init__(model)
        self.zone=zone