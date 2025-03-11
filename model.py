# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Model
from mesa.space import MultiGrid
from agents import GreenRobot, YellowRobot, RedRobot
from objects import Waste, Radioactivity, WasteDisposalZone
import random

from parametres import GRID_WIDTH, GRID_HEIGHT, ZONE_GREEN, ZONE_YELLOW, ZONE_RED

class RobotMission(Model):
    def __init__(self, width=GRID_WIDTH, height=GRID_HEIGHT):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, torus=False)
        self.running = True
        
        # Création des zones de radioactivité
        self.setup_radioactivity_zones()
        
        # Création des robots
        self.green_robot = GreenRobot(self)
        self.yellow_robot = YellowRobot(self)
        self.red_robot = RedRobot(self)
        
        # Placement des robots dans leurs zones respectives
        self.setup_robots()
        
        # Ajout d'un déchet initial dans la zone verte
        self.setup_initial_waste()
        
        # Création de la zone de dépôt final (dernière colonne)
        self.setup_disposal_zone()

    def setup_radioactivity_zones(self):
        """Configure les zones de radioactivité."""
        # Zone verte
        for x in range(ZONE_GREEN[0], ZONE_GREEN[1] + 1):
            for y in range(self.height):
                radioactivity = Radioactivity(self, zone=1)
                self.grid.place_agent(radioactivity, (x, y))
        
        # Zone jaune
        for x in range(ZONE_YELLOW[0], ZONE_YELLOW[1] + 1):
            for y in range(self.height):
                radioactivity = Radioactivity(self, zone=2)
                self.grid.place_agent(radioactivity, (x, y))
        
        # Zone rouge
        for x in range(ZONE_RED[0], ZONE_RED[1] + 1):
            for y in range(self.height):
                radioactivity = Radioactivity(self, zone=3)
                self.grid.place_agent(radioactivity, (x, y))

    def setup_robots(self):
        """Place les robots dans leurs zones respectives."""
        # Robot vert dans la zone verte
        green_pos = (random.randint(ZONE_GREEN[0], ZONE_GREEN[1]), random.randint(0, self.height - 1))
        self.grid.place_agent(self.green_robot, green_pos)
        
        # Robot jaune dans la zone jaune
        yellow_pos = (random.randint(ZONE_YELLOW[0], ZONE_YELLOW[1]), random.randint(0, self.height - 1))
        self.grid.place_agent(self.yellow_robot, yellow_pos)
        
        # Robot rouge dans la zone rouge
        red_pos = (random.randint(ZONE_RED[0], ZONE_RED[1]), random.randint(0, self.height - 1))
        self.grid.place_agent(self.red_robot, red_pos)

    def setup_initial_waste(self):
        """Place un déchet initial dans la zone verte."""
        waste_pos = (random.randint(ZONE_GREEN[0], ZONE_GREEN[1]), random.randint(0, self.height - 1))
        waste = Waste(self, waste_type="green")
        self.grid.place_agent(waste, waste_pos)

    def setup_disposal_zone(self):
        """Configure la zone de dépôt final."""
        for y in range(self.height):
            disposal = WasteDisposalZone(self)
            self.grid.place_agent(disposal, (self.width - 1, y))

    def get_percepts(self, agent):
        """Retourne les informations sur l'environnement autour de l'agent."""
        # Obtenir les cellules voisines et leur contenu
        neighbors = self.grid.get_neighborhood(agent.pos, moore=True, include_center=True)
        percepts = {}
        
        for pos in neighbors:
            cell_content = self.grid.get_cell_list_contents([pos])
            if cell_content:
                percepts[pos] = cell_content
                
        return percepts

    def do(self, agent, action):
        """Exécute une action et retourne les nouvelles perceptions."""
        print(f"{agent.robot_type} robot at {agent.pos} doing: {action}")
        
        if action == "search_waste":
            # Vérifier si l'agent est sur une cellule avec un déchet
            cell_contents = self.grid.get_cell_list_contents([agent.pos])
            for obj in cell_contents:
                if isinstance(obj, Waste) and obj.waste_type == agent.robot_type:
                    # Collecter le déchet
                    agent.inventory = obj
                    self.grid.remove_agent(obj)
                    print(f"{agent.robot_type} robot collected a {obj.waste_type} waste")
                    break
            
            # Si aucun déchet n'a été collecté, déplacer l'agent aléatoirement dans sa zone
            if not agent.inventory:
                self.move_agent_randomly(agent)
                
        elif action == "drop_waste":
            # L'agent dépose le déchet s'il en a un
            if agent.inventory:
                waste_type = "yellow" if agent.robot_type == "green" else "red" if agent.robot_type == "yellow" else "disposed"
                
                # Si le déchet est "disposed", on le supprime simplement
                if waste_type != "disposed":
                    waste = Waste(self, waste_type=waste_type)
                    self.grid.place_agent(waste, agent.pos)
                    print(f"{agent.robot_type} robot dropped a {waste_type} waste at {agent.pos}")
                else:
                    print(f"{agent.robot_type} robot disposed of the waste at {agent.pos}")
                
                agent.inventory = None
            
        elif action == "go_to_pickup":
            # L'agent se déplace vers la colonne de collecte
            target_column = 2 if agent.robot_type == "yellow" else 5 if agent.robot_type == "red" else 0
            self.move_towards_column(agent, target_column)
            
        elif action == "go_to_drop":
            # L'agent se déplace vers la colonne de dépôt
            target_column = 2 if agent.robot_type == "green" else 5 if agent.robot_type == "yellow" else 8
            self.move_towards_column(agent, target_column)
        
        # Retourner les nouvelles perceptions
        return self.get_percepts(agent)
    
    def move_agent_randomly(self, agent):
        """Déplace l'agent de manière aléatoire dans sa zone autorisée."""
        possible_moves = []
        
        # Obtenir toutes les cellules voisines
        neighbors = self.grid.get_neighborhood(agent.pos, moore=False, include_center=False)
        
        # Filtrer les cellules autorisées
        for pos in neighbors:
            # Vérifier si la position est dans les zones autorisées du robot
            if self.is_position_allowed(agent, pos):
                possible_moves.append(pos)
        
        if possible_moves:
            new_position = random.choice(possible_moves)
            self.grid.move_agent(agent, new_position)
            print(f"{agent.robot_type} robot moved to {new_position}")
    
    def move_towards_column(self, agent, target_column):
        """Déplace l'agent vers une colonne cible."""
        current_x, current_y = agent.pos
        
        # Obtenir les cellules voisines
        neighbors = self.grid.get_neighborhood(agent.pos, moore=False, include_center=False)
        best_move = None
        best_distance = float('inf')
        
        # Chercher le mouvement qui rapproche le plus de la colonne cible
        for pos in neighbors:
            x, y = pos
            if self.is_position_allowed(agent, pos):
                distance = abs(x - target_column)
                if distance < best_distance:
                    best_distance = distance
                    best_move = pos
        
        # Si un mouvement est possible, déplacer l'agent
        if best_move:
            self.grid.move_agent(agent, best_move)
            print(f"{agent.robot_type} robot moved towards column {target_column}, now at {best_move}")
        else:
            # Si aucun mouvement n'est possible, déplacer aléatoirement
            self.move_agent_randomly(agent)
    
    def is_position_allowed(self, agent, position):
        """Vérifie si la position est autorisée pour le robot."""
        x, y = position
        
        # Définir les zones autorisées en fonction du type de robot
        if agent.robot_type == "green":
            # Robot vert: uniquement zone verte (colonnes 0-2)
            return 0 <= x <= 2
        elif agent.robot_type == "yellow":
            # Robot jaune: zone jaune (colonnes 3-5) + dernière colonne verte (colonne 2)
            return (3 <= x <= 5) or x == 2
        elif agent.robot_type == "red":
            # Robot rouge: zone rouge (colonnes 6-8) + dernière colonne jaune (colonne 5)
            return (6 <= x <= 8) or x == 5
        
        return False
        
    def step(self):
        """Avance la simulation d'un pas."""
        # Créer une copie de la liste des agents pour éviter de modifier la structure pendant l'itération
        agents_copy = list(self.agents)
        
        # Ne faire avancer que les robots, pas les objets Radioactivity
        for agent in agents_copy:
            if isinstance(agent, (GreenRobot, YellowRobot, RedRobot)):
                agent.step_agent()