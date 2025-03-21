# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Agent

class Waste(Agent):
    """Représente un déchet à collecter."""
    def __init__(self, model, waste_type="green"):
        super().__init__(model)
        self.waste_type = waste_type  # Types possibles: "green", "yellow", "red"
        
class Radioactivity(Agent):
    """Représente une zone de radioactivité."""
    def __init__(self, model, zone, radioactivity_level=None):
        super().__init__(model)
        self.zone = zone  # 1=vert, 2=jaune, 3=rouge
        
        # Calcul du niveau de radioactivité en fonction de la zone
        if radioactivity_level is None:
            if zone == 1:
                # Zone verte: niveau bas (0 - 0.33)
                self.radioactivity_level = self.random.uniform(0, 0.33)
            elif zone == 2:
                # Zone jaune: niveau moyen (0.33 - 0.66)
                self.radioactivity_level = self.random.uniform(0.33, 0.66)
            elif zone == 3:
                # Zone rouge: niveau élevé (0.66 - 1)
                self.radioactivity_level = self.random.uniform(0.66, 1)
        else:
            self.radioactivity_level = radioactivity_level

class WasteDisposalZone(Agent):
    """Représente la zone de dépôt final des déchets."""
    def __init__(self, model):
        super().__init__(model)