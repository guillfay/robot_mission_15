# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Agent
import random

from parametres import ZONE_GREEN, ZONE_YELLOW, ZONE_RED

class RobotAgent(Agent):
    """Classe de base pour tous les types de robots."""
    def __init__(self, model, robot_type, allowed_zones):
        super().__init__(model)
        self.knowledge = {}  # Base de connaissances
        self.inventory = None  # Déchet transporté actuellement
        self.robot_type = robot_type  # "green", "yellow", "red"
        self.allowed_zones = allowed_zones  # Zones où le robot peut se déplacer

        # self.unique_id = f"{self.robot_type}_{self.model.next_id()}"
        
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
    
    # def is_allowed_position(self, position):
    #     """Vérifie si la position est autorisée pour ce robot."""
    #     x, y = position
        
    #     # Zone verte
    #     if ZONE_GREEN[0] <= x <= ZONE_GREEN[1]:
    #         return 1 in self.allowed_zones
    #     # Zone jaune
    #     elif ZONE_YELLOW[0] <= x <= ZONE_YELLOW[1]:
    #         return 2 in self.allowed_zones
    #     # Zone rouge
    #     elif ZONE_RED[0] <= x <= ZONE_RED[1]:
    #         return 3 in self.allowed_zones
        
    #     return False

class GreenRobot(RobotAgent):
    """Robot qui ne peut se déplacer que dans la zone verte."""
    def __init__(self, model):
        super().__init__(model, "green", [1])  # Zone 1 = verte

   

    def deliberate(self, knowledge):
        """Stratégie de décision du robot vert."""
        # Si le robot a un déchet et est sur la dernière colonne de sa zone
        if self.inventory and self.pos[0] == 2:
            return "drop_waste"
        # Si le robot n'a pas de déchet
        elif not self.inventory:
            return "search_waste"
        # Si le robot a un déchet mais n'est pas sur la colonne de dépôt
        else:
            return "go_to_drop"

class YellowRobot(RobotAgent):
    """Robot qui peut se déplacer dans les zones jaune et la dernière colonne de la zone verte."""
    def __init__(self, model):
        super().__init__(model, "yellow", [2])  # Zone 2 = jaune
    
    def deliberate(self, knowledge):
        """Stratégie de décision du robot jaune."""
        # Si le robot est dans la zone jaune avec un déchet et sur la dernière colonne
        if self.inventory and self.pos[0] == 5:
            return "drop_waste"
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 2)
        elif not self.inventory and self.pos[0] == 2:
            return "search_waste"
        # Si le robot n'a pas de déchet, se diriger vers la colonne de collecte
        elif not self.inventory:
            return "go_to_pickup"
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        else:
            return "go_to_drop"

class RedRobot(RobotAgent):
    """Robot qui peut se déplacer dans la zone rouge et la dernière colonne de la zone jaune."""
    def __init__(self, model):
        super().__init__(model, "red", [3])  # Zone 3 = rouge
    
    def deliberate(self, knowledge):
        """Stratégie de décision du robot rouge."""
        # Si le robot est dans la zone rouge avec un déchet et sur la dernière colonne
        if self.inventory and self.pos[0] == 8:
            return "drop_waste"
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        elif not self.inventory and self.pos[0] == 5:
            return "search_waste"
        # Si le robot n'a pas de déchet, se diriger vers la colonne de collecte
        elif not self.inventory:
            return "go_to_pickup"
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        else:
            return "go_to_drop"