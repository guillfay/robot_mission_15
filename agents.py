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
        self.weight_inventory = 0  # Poids total des déchets transportés
        self.got_waste = False
        self.robot_type = robot_type  # "green", "yellow", "red"
        self.allowed_zones = allowed_zones  # Zones où le robot peut se déplacer
        self.visited = set()  # Ensemble des cellules visitées
    
    def step_agent(self):
        """Mise à jour des perceptions"""

        # Choix d'une action
        action = self.deliberate(self.knowledge)

        # Exécution de l'action et mise à jour des perceptions
        self.knowledge = self.model.do(self, action)

        # Enregistre la position actuelle comme visitée
        self.visited.add(self.pos)  
    

    def deliberate(self, knowledge):
        """Détermine l'action à effectuer selon les perceptions. Cette méthode doit être surchargée."""
        pass

    def move_towards(self, target_pos):
        """Renvoie une action pour aller vers target_pos."""
        x, y = self.pos
        target_x, target_y = target_pos

        if x < target_x:
            return "move_right"
        elif x > target_x:
            return "move_left"
        elif y < target_y:
            return "move_up"
        elif y > target_y:
            return "move_down"
        return "search_waste"  # Si déjà sur place, continuer à chercher
    

class GreenRobot(RobotAgent):
    """Robot qui ne peut se déplacer que dans la zone verte."""
    def __init__(self, model):
        super().__init__(model, "green", [1])  # Zone 1 = verte
    
    def deliberate(self, knowledge):
        """Stratégie de décision du robot."""
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        if self.weight_inventory!=2:

            # Si Waste à proximité, il y va
            is_waste, pos = self.model.checkwaste(self)
            if is_waste:
                return self.move_towards(pos)

            # Rechercher des zones non visitées
            else: 
                unexplored = [pos for pos in knowledge.keys() if pos not in self.visited]
                if unexplored:
                    return self.move_towards(unexplored[0])  # Aller vers une zone inexplorée

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            print("full")
            if self.model.checkdrop(self):
                return "drop_waste"
            else:
                return "go_to_drop"
    
    
    

class YellowRobot(RobotAgent):
    """Robot qui peut se déplacer dans les zones jaune et la dernière colonne de la zone verte."""
    def __init__(self, model):
        super().__init__(model, "yellow", [1, 2])  # Zone 2 = jaune
    
    def deliberate(self, knowledge):
        """Stratégie de décision du robot."""
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        if self.weight_inventory!=2:

            # Si Waste à proximité, il y va
            is_waste, pos = self.model.checkwaste(self)
            if is_waste:
                return self.move_towards(pos)

            # Rechercher des zones non visitées
            else: 
                unexplored = [pos for pos in knowledge.keys() if pos not in self.visited]
                if unexplored:
                    return self.move_towards(unexplored[0])  # Aller vers une zone inexplorée

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            print("full")
            if self.model.checkdrop(self):
                return "drop_waste"
            else:
                return "go_to_drop"
    
    


class RedRobot(RobotAgent):
    """Robot qui peut se déplacer dans la zone rouge et la dernière colonne de la zone jaune."""
    def __init__(self, model):
        super().__init__(model, "red", [1, 2, 3])  # Zone 3 = rouge
    
    def deliberate(self, knowledge):
        """Stratégie de décision du robot."""
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        if self.weight_inventory!=2:

            # Si Waste à proximité, il y va
            is_waste, pos = self.model.checkwaste(self)
            if is_waste:
                return self.move_towards(pos)

            # Rechercher des zones non visitées
            else: 
                unexplored = [pos for pos in knowledge.keys() if pos not in self.visited]
                if unexplored:
                    return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée aléatoire

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            print("full")
            if self.model.checkdrop(self):
                return "drop_waste"
            else:
                return "go_to_drop"
    
    