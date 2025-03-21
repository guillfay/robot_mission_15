# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Agent
import random

class RobotAgent(Agent):
    """Classe de base pour tous les types de robots."""
    def __init__(self, model, robot_type, allowed_zones):
        super().__init__(model)
        self.knowledge = {}  # Base de connaissances
        self.inventory = []  # Déchet transporté actuellement
        self.got_waste = False
        self.robot_type = robot_type  # "green", "yellow", "red"
        self.allowed_zones = allowed_zones  # Zones où le robot peut se déplacer
    
    def step_agent(self):
        # Mise à jour des perceptions
        percepts = self.model.get_percepts(self)
        self.knowledge.update(percepts)

        # Choix d'une action
        action = self.deliberate(self.knowledge)

        # Exécution de l'action et mise à jour des perceptions
        percepts = self.model.do(self, action)
        self.knowledge.update(percepts)
    
    def deliberate(self, knowledge):
        """Détermine l'action à effectuer selon les perceptions. Cette méthode doit être surchargée."""
        pass
    

class GreenRobot(RobotAgent):
    """Robot qui ne peut se déplacer que dans la zone verte."""
    def __init__(self, model):
        super().__init__(model, "green", [1])  # Zone 1 = verte
    
    def deliberate(self, knowledge):
        """Stratégie de décision du robot vert."""
        # Si le robot a un déchet et est sur la dernière colonne de sa zone
        if len(self.inventory)==2 and self.model.checkdrop(self):
            return "drop_waste"
        # Si le robot n'a pas de déchet
        elif len(self.inventory)!=2:
            return "search_waste"
        # Si le robot a un déchet mais n'est pas sur la colonne de dépôt
        elif len(self.inventory)==2:
            return "go_to_drop"

class YellowRobot(RobotAgent):
    """Robot qui peut se déplacer dans les zones jaune et la dernière colonne de la zone verte."""
    def __init__(self, model):
        super().__init__(model, "yellow", [2])  # Zone 2 = jaune
    
    def deliberate(self, knowledge):
        """Stratégie de décision du robot jaune."""
        # Si le robot est dans la zone jaune avec un déchet et sur la dernière colonne
        if len(self.inventory)==2 and self.pos[0] == self.model.checkdrop(self):
            return "drop_waste"
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 2)
        elif len(self.inventory)!=2:
            return "search_waste"
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif len(self.inventory)==2:
            return "go_to_drop"

class RedRobot(RobotAgent):
    """Robot qui peut se déplacer dans la zone rouge et la dernière colonne de la zone jaune."""
    def __init__(self, model):
        super().__init__(model, "red", [3])  # Zone 3 = rouge
    
    def deliberate(self, knowledge):
        """Stratégie de décision du robot rouge."""
        # Si le robot est dans la zone rouge avec un déchet et sur la dernière colonne
        if len(self.inventory)==2 and self.pos[0] == self.model.checkdrop(self):
            return "drop_waste"
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        elif len(self.inventory)!=2:
            return "search_waste"
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif len(self.inventory)==2:
            return "go_to_drop"