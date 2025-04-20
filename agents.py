# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Agent
import random
import numpy as np

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
        self.go_fuze = False
        self.just_dropped = False
        self.ID = 0  # ID unique du robot
        self.coverage_zone = (None, None)
        self.just_spawned = True  # Indique si le robot vient d'apparaître
        self.random_direction = 0


    def step_agent(self):
        """Mise à jour des perceptions"""

        # Choix d'une action
        if self.model.strategy == 1: #Non visited
            action = self.deliberate_1(self.knowledge)
        elif self.model.strategy == 2: #Visited
            action = self.deliberate_2(self.knowledge)
        elif self.model.strategy == 3: #OnebyOne
            action = self.deliberate_3(self.knowledge)
        elif self.model.strategy == 4: #OnebyOneDivided
            action = self.deliberate_4(self.knowledge)
            

        # Exécution de l'action et mise à jour des perceptions
        self.knowledge = self.model.do(self, action)

        # Enregistre la position actuelle comme visitée
        self.visited.add(self.pos)  
    

    # def deliberate_1(self, knowledge):
    #     """Détermine l'action à effectuer selon les perceptions. Cette méthode doit être surchargée."""
    #     pass

    # def deliberate_2(self, knowledge):
    #     """Détermine l'action à effectuer selon les perceptions. Cette méthode doit être surchargée."""
    #     pass

    # def deliberate_3(self, knowledge):
    #     """Détermine l'action à effectuer selon les perceptions. Cette méthode doit être surchargée."""
    #     pass

    # def deliberate_4(self, knowledge):
    #     """Détermine l'action à effectuer selon les perceptions. Cette méthode doit être surchargée."""
    #     pass

    def move_towards(self, target_pos):
        """Renvoie une action pour aller vers target_pos."""
        x, y = self.pos
        target_x, target_y = target_pos
        if y < target_y:
            return "move_up"
        elif y > target_y:
            return "move_down"
        elif x < target_x:
            return "move_right"
        elif x > target_x:
            return "move_left"
        
        return "search_waste"  # Si déjà sur place, continuer à chercher
    

class GreenRobot(RobotAgent):
    """Robot qui ne peut se déplacer que dans la zone verte."""
    def __init__(self, model):
        super().__init__(model, "green", [1])  # Zone 1 = verte
    

    def deliberate_1(self, knowledge):
        """Non visited + dépot droite fusion"""
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        if self.weight_inventory!=2:

            # Si Waste à proximité, il y va
            is_waste, pos = self.model.checkwaste(self)
            if is_waste:
                return self.move_towards(pos)

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            if self.model.deliberate_1_checkdrop(self):
                return "drop_waste"
            else:
                return "deliberate_1_go_to_drop"
            

    def deliberate_2(self, knowledge):
        """Visited + pdépot droite fusion"""
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
                    return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            if self.model.deliberate_1_checkdrop(self):
                return "drop_waste"
            else:
                return "deliberate_1_go_to_drop"
            
    
    def deliberate_3(self, knowledge):
        """Visited + ONEbyONEnSTEP"""

        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        if self.weight_inventory==0:

            # Si Waste à proximité, il y va
            is_waste, pos = self.model.checkwaste(self)
            # On prend en compte le fait que la case de dépôt est une case de déchet où on ne veut pas aller pour ne pas faire des aller retour oscillant quand on y dépose un dechet
            if pos == (self.model.ZONE_GREEN[-1], self.model.grid.height - 1):
                is_waste = False
                pos = None

            if is_waste:
                return self.move_towards(pos)

            # Rechercher des zones non visitées
            else: 
                unexplored = [pos for pos in knowledge.keys() if pos not in self.visited]
                if unexplored:
                    return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet ou une fusion, se diriger vers la case de dépôt
        elif self.weight_inventory==1 or self.weight_inventory==2:
            if self.model.deliberate_3_checkdrop(self):
                return "drop_waste"
            else:
                return self.move_towards([self.model.ZONE_GREEN[-1], self.model.grid.height - 1])


    def deliberate_4(self, knowledge):
        """Visited + ONEbyONEnSTEP + space divided"""

        # Comportement initial : va à sa zone de dépôt
        if self.pos == (self.model.ZONE_GREEN[-1], self.coverage_zone[1]):
            self.just_spawned = False
        if self.just_spawned:
            return self.move_towards((self.model.ZONE_GREEN[-1], self.coverage_zone[1]))

        # annule coverage zone à la fin pour fucionner dechet séparer dans les différetnes decheteries
        if self.random_direction == 5*(self.model.ZONE_GREEN[1]- self.model.ZONE_GREEN[0]) * (self.coverage_zone[1] - self.coverage_zone[0]):
            self.model.change_strategy(3) #l'agent change sa propre strategy

        # Si le robot n'a pas de déchet
        if self.weight_inventory==0:

            # Si Waste à proximité, il y va
            is_waste, pos = self.model.checkwaste(self)
            # On prend en compte le fait que la case de dépôt est une case de déchet où on ne veut pas aller pour ne pas faire des aller retour oscillant quand on y dépose un dechet
            if pos and (pos == (self.model.ZONE_GREEN[-1], self.coverage_zone[1]) or not self.coverage_zone[0] <= pos[1] <= self.coverage_zone[1]): 
                is_waste = False
                pos = None

            if is_waste:
                self.random_direction = 0
                return self.move_towards(pos)

            # Rechercher des zones non visitées
            else: 
                unexplored = [pos for pos in knowledge.keys() if pos not in self.visited and self.coverage_zone[0] <= pos[1] <= self.coverage_zone[1]]
                if unexplored:
                    self.random_direction = 0
                    return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

            # Si tout a été exploré, marcher aléatoirement
            self.random_direction += 1
            return "search_waste_4"
        
        # Si le robot a un déchet ou une fusion, se diriger vers la case de dépôt
        elif self.weight_inventory==1 or self.weight_inventory==2:
            if self.model.deliberate_4_checkdrop(self):
                return "drop_waste"
            else:
                self.random_direction = 0
                return self.move_towards([self.model.ZONE_GREEN[-1], self.coverage_zone[1]])
            


class YellowRobot(RobotAgent):
    """Robot qui peut se déplacer dans les zones jaune et la dernière colonne de la zone verte."""
    def __init__(self, model):
        super().__init__(model, "yellow", [1, 2])  # Zone 2 = jaune
    
    def deliberate_1(self, knowledge):
        """Non visited + dépot droite fusion"""
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        if self.weight_inventory!=2:

            # Si Waste à proximité, il y va
            is_waste, pos = self.model.checkwaste(self)
            if is_waste:
                return self.move_towards(pos)

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            if self.model.deliberate_1_checkdrop(self):
                return "drop_waste"
            else:
                return "deliberate_1_go_to_drop"
            

    def deliberate_2(self, knowledge):
        """Visited + pdépot droite fusion"""
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
                    return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            if self.model.deliberate_1_checkdrop(self):
                return "drop_waste"
            else:
                return "deliberate_1_go_to_drop"


    def deliberate_3(self, knowledge):
        """Visited + ONEbyONEnSTEP"""

        # Va récupere les dechets dans la zone de dépot verte
        if self.model.time_step % self.ID == 0:
            self.go_fuze = True
        if self.pos == (self.model.ZONE_GREEN[-1], self.model.grid.height - 1):
            self.go_fuze = False

        if self.go_fuze:
            return self.move_towards([self.model.ZONE_GREEN[-1], self.model.grid.height - 1])
        else : 
            # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
            if self.weight_inventory==0:

                # Si Waste à proximité, il y va
                is_waste, pos = self.model.checkwaste(self)
                # On prend en compte le fait que la case de dépôt est une case de déchet où on ne veut pas aller pour ne pas faire des aller retour oscillant quand on y dépose un dechet
                if pos == (self.model.ZONE_YELLOW[-1], self.model.grid.height - 1):
                    is_waste = False
                    pos = None

                if is_waste:
                    return self.move_towards(pos)

                # Rechercher des zones non visitées
                else: 
                    unexplored = [pos for pos in knowledge.keys() if pos not in self.visited]
                    if unexplored:
                        return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

                # Si tout a été exploré, marcher aléatoirement
                return "search_waste"
            
            # Si le robot a un déchet ou une fusion, se diriger vers la case de dépôt
            elif self.weight_inventory==1 or self.weight_inventory==2:
                if self.model.deliberate_3_checkdrop(self):
                    return "drop_waste"
                else:
                    return self.move_towards([self.model.ZONE_YELLOW[-1], self.model.grid.height - 1])
        
        
    
    def deliberate_4(self, knowledge):
        """Visited + ONEbyONEnSTEP + divided"""

        # Comportement initial : va à sa zone de dépôt
        if self.pos == (self.model.ZONE_YELLOW[-1], self.coverage_zone[1]):
            self.just_spawned = False
        if self.just_spawned:
            return self.move_towards((self.model.ZONE_YELLOW[-1], self.coverage_zone[1]))
        
        # annule coverage zone à la fin pour fucionner dechet séparer dans les différetnes decheteries
        if self.random_direction == 5*(self.model.ZONE_YELLOW[1]- self.model.ZONE_YELLOW[0]) * (self.coverage_zone[1] - self.coverage_zone[0]):
            self.model.change_strategy(3) #l'agent change sa propre strategy

        # Va récupere les dechets dans la zone de dépot verte
        if self.model.time_step % self.ID == 0:
            self.go_fuze = True
        if self.pos == (self.model.ZONE_GREEN[-1], self.coverage_zone[1]):
            self.go_fuze = False


        if self.go_fuze:
            self.random_direction = 0
            return self.move_towards([self.model.ZONE_GREEN[-1], self.coverage_zone[1]])
        else : 
            # Si le robot n'a pas de déchet
            if self.weight_inventory==0:

                # Si Waste à proximité, il y va
                is_waste, pos = self.model.checkwaste(self)
                # On prend en compte le fait que la case de dépôt est une case de déchet où on ne veut pas aller pour ne pas faire des aller retour oscillant quand on y dépose un dechet
                if pos and (pos == (self.model.ZONE_YELLOW[-1], self.coverage_zone[1]) or not self.coverage_zone[0] <= pos[1] <= self.coverage_zone[1]): 
                    is_waste = False
                    pos = None

                if is_waste:
                    self.random_direction = 0
                    return self.move_towards(pos)

                # Rechercher des zones non visitées
                else: 
                    unexplored = [pos for pos in knowledge.keys() if pos not in self.visited and self.coverage_zone[0] <= pos[1] <= self.coverage_zone[1]]
                    if unexplored:
                        self.random_direction = 0
                        return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

                # Si tout a été exploré, marcher aléatoirement
                self.random_direction += 1
                return "search_waste_4"
            
            # Si le robot a un déchet ou une fusion, se diriger vers la case de dépôt
            elif self.weight_inventory==1 or self.weight_inventory==2:
                if self.model.deliberate_4_checkdrop(self):
                    return "drop_waste"
                else:
                    self.random_direction = 0
                    return self.move_towards([self.model.ZONE_YELLOW[-1], self.coverage_zone[1]])
            


class RedRobot(RobotAgent):
    """Robot qui peut se déplacer dans la zone rouge et la dernière colonne de la zone jaune."""
    def __init__(self, model):
        super().__init__(model, "red", [1, 2, 3])  # Zone 3 = rouge
    
    def deliberate_1(self, knowledge):
        """Non visited + dépot droite fusion"""
        # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
        if self.weight_inventory!=2:

            # Si Waste à proximité, il y va
            is_waste, pos = self.model.checkwaste(self)
            if is_waste:
                return self.move_towards(pos)

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            if self.model.deliberate_1_checkdrop(self):
                return "drop_waste"
            else:
                return "deliberate_1_go_to_drop"
            

    def deliberate_2(self, knowledge):
        """Visited + pdépot droite fusion"""
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
                    return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

            # Si tout a été exploré, marcher aléatoirement
            return "search_waste"
        
        # Si le robot a un déchet, se diriger vers la colonne de dépôt
        elif self.weight_inventory==2:
            if self.model.deliberate_1_checkdrop(self):
                return "drop_waste"
            else:
                return "deliberate_1_go_to_drop"
    

    def deliberate_3(self, knowledge):
        """Visited + ONEbyONEnSTEP"""

        # Va récupere les dechets dans la zone de dépot verte
        if self.model.time_step % self.ID == 0:
            self.go_fuze = True
        if self.pos == (self.model.ZONE_YELLOW[-1], self.model.grid.height - 1):
            self.go_fuze = False

        if self.go_fuze:
            return self.move_towards([self.model.ZONE_YELLOW[-1], self.model.grid.height - 1])
        else : 
            # Si le robot n'a pas de déchet et se trouve sur la colonne de collecte (colonne 5)
            if self.weight_inventory==0:

                # Si Waste à proximité, il y va
                is_waste, pos = self.model.checkwaste(self)
                # On prend en compte le fait que la case de dépôt est une case de déchet où on ne veut pas aller pour ne pas faire des aller retour oscillant quand on y dépose un dechet
                if pos == (self.model.ZONE_RED[-1], self.model.grid.height - 1):
                    is_waste = False
                    pos = None

                if is_waste:
                    return self.move_towards(pos)

                # Rechercher des zones non visitées
                else: 
                    unexplored = [pos for pos in knowledge.keys() if pos not in self.visited]
                    if unexplored:
                        return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

                # Si tout a été exploré, marcher aléatoirement
                return "search_waste"
            
            # Si le robot a un déchet ou une fusion, se diriger vers la case de dépôt
            elif self.weight_inventory==1 or self.weight_inventory==2:
                if self.model.deliberate_3_checkdrop(self):
                    return "drop_waste"
                else:
                    return self.move_towards([self.model.ZONE_RED[-1], self.model.grid.height - 1])
        


    def deliberate_4(self, knowledge):
        """Visited + ONEbyONEnSTEP + divided"""

        # Comportement initial : va à sa zone de dépôt
        if self.pos == (self.model.ZONE_RED[-1], self.coverage_zone[1]):
            self.just_spawned = False
        if self.just_spawned:
            return self.move_towards((self.model.ZONE_RED[-1], self.coverage_zone[1]))
        
        # annule coverage zone à la fin pour fucionner dechet séparer dans les différetnes decheteries
        if self.random_direction == 5*(self.model.ZONE_RED[1]- self.model.ZONE_RED[0]) * (self.coverage_zone[1] - self.coverage_zone[0]):
            self.model.change_strategy(3) #l'agent change sa propre strategy


        # Va récupere les dechets dans la zone de dépot verte
        if self.model.time_step % self.ID == 0:
            self.go_fuze = True
        if self.pos == (self.model.ZONE_YELLOW[-1], self.coverage_zone[1]):
            self.go_fuze = False

        if self.go_fuze:
            self.random_direction = 0
            return self.move_towards([self.model.ZONE_YELLOW[-1], self.coverage_zone[1]])
        else : 
            # Si le robot n'a pas de déchet
            if self.weight_inventory==0:

                # Si Waste à proximité, il y va
                is_waste, pos = self.model.checkwaste(self)
                # On prend en compte le fait que la case de dépôt est une case de déchet où on ne veut pas aller pour ne pas faire des aller retour oscillant quand on y dépose un dechet
                if pos and (pos == (self.model.ZONE_RED[-1], self.coverage_zone[1]) or not self.coverage_zone[0] <= pos[1] <= self.coverage_zone[1]): 
                    is_waste = False
                    pos = None

                if is_waste:
                    self.random_direction = 0
                    return self.move_towards(pos)

                # Rechercher des zones non visitées
                else: 
                    unexplored = [pos for pos in knowledge.keys() if pos not in self.visited and self.coverage_zone[0] <= pos[1] <= self.coverage_zone[1]]
                    if unexplored:
                        self.random_direction = 0
                        return self.move_towards(random.choice(unexplored))  # Aller vers une zone inexplorée

                # Si tout a été exploré, marcher aléatoirement
                self.random_direction += 1
                return "search_waste_4"
            
            # Si le robot a un déchet ou une fusion, se diriger vers la case de dépôt
            elif self.weight_inventory==1 or self.weight_inventory==2:
                if self.model.deliberate_4_checkdrop(self):
                    return "drop_waste"
                else:
                    self.random_direction = 0
                    return self.move_towards([self.model.ZONE_RED[-1], self.coverage_zone[1]])