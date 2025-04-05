# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa import Model
from mesa.space import MultiGrid
from agents import GreenRobot, YellowRobot, RedRobot
from objects import Waste, Radioactivity, WasteDisposalZone
import random
from mesa.datacollection import DataCollector


class RobotMission(Model):
    def __init__(self,
                 width=13,
                 height=11,
                 n_green=2,
                 n_yellow=2,
                 n_red=2,
                 n_wastes=10,
                 strategy=3
                   ):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.running = True
        self.time_step = 0

        self.n_green=n_green
        self.n_yellow=n_yellow
        self.n_red=n_red
        self.n_wastes=n_wastes
        self.strategy=strategy
        self.green_wastes_remaining=0
        self.yellow_wastes_remaining=0
        self.red_wastes_remaining=0
        self.latent_green=0
        self.latent_yellow=0
        
        self.ZONE_WIDTH = self.grid.width // 3  
        self.ZONE_GREEN = (0, self.ZONE_WIDTH - 1)  
        self.ZONE_YELLOW = (self.ZONE_WIDTH, 2 * self.ZONE_WIDTH - 1)  
        self.ZONE_RED = (2 * self.ZONE_WIDTH, self.grid.width - 1)  

        self.fused_wastes_count = 0  # Initialize a counter for fused wastes
        self.total_collected_wastes = 0  # Initialize a counter for total collected wastes
        self.red_wastes_returned = 0  # Initialize a counter for red wastes remaining

        self.datacollector = DataCollector(
            model_reporters={
            "FusedWastes": lambda m: m.fused_wastes_count,  # Report the number of fused wastes
            "CollectedWastes": lambda m: m.total_collected_wastes, # Report the cumulative number of wastes collected by each robot
            "RedWastesDeposited": lambda m: m.red_wastes_returned,
            "GreenWastesRemaining": lambda m: m.green_wastes_remaining,
            "YellowWastesRemaining": lambda m: m.yellow_wastes_remaining,
            "RedWastesRemaining": lambda m: m.red_wastes_remaining,  # Report the number of red wastes deposited
            "GreenLatentWastes" : lambda m: m.latent_green,
            "YellowLatentWastes" : lambda m: m.latent_yellow
            },
            # agent_reporters={
            # "CollectedWastes": lambda a: a.total_collected_wastes if isinstance(a, (GreenRobot, YellowRobot, RedRobot)) else 0,  # Report the cumulative number of wastes collected by each robot
            # },
        )
        self.datacollector.collect(self)

        # Création des zones de radioactivité
        self.setup_radioactivity_zones()
        
        # Création des robots
        self.green_agents = GreenRobot.create_agents(model=self, n=n_green)
        self.yellow_agents = YellowRobot.create_agents(model=self, n=n_yellow)
        self.red_agents = RedRobot.create_agents(model=self, n=n_red)
        # self.green_robot = GreenRobot(self)
        # self.yellow_robot = YellowRobot(self)
        # self.red_robot = RedRobot(self)
        
        # Placement des robots dans leurs zones respectives
        self.setup_robots()
        
        # Ajout d'un déchet initial dans la zone verte
        # self.setup_initial_waste()

        # Ajout de plusieurs déchets
        self.setup_wastes()
        
        # Création de la zone de dépôt final (dernière colonne)
        self.setup_disposal_zone()

    def setup_radioactivity_zones(self):
        """Configure les zones de radioactivité."""
        # Zone verte
        for x in range(self.ZONE_GREEN[0], self.ZONE_GREEN[1]+1):
            for y in range(self.grid.height):
                radioactivity = Radioactivity(self, zone=1)
                self.grid.place_agent(radioactivity, (x, y))
        
        # Zone jaune
        for x in range(self.ZONE_YELLOW[0], self.ZONE_YELLOW[1]+1):
            for y in range(self.grid.height):
                radioactivity = Radioactivity(self, zone=2)
                self.grid.place_agent(radioactivity, (x, y))
        
        # Zone rouge
        for x in range(self.ZONE_RED[0], self.ZONE_RED[1]+1):
            for y in range(self.grid.height):
                radioactivity = Radioactivity(self, zone=3)
                self.grid.place_agent(radioactivity, (x, y))

    def setup_robots(self):
        """Place les robots dans leurs zones respectives."""
        # Robot vert dans la zone verte
        for i, agent in enumerate(self.green_agents):
            agent.ID = (i+1)*100/self.n_green
            green_pos = (random.randint(self.ZONE_GREEN[0], self.ZONE_GREEN[1]), random.randint(0, self.grid.height - 1))
            self.grid.place_agent(agent, green_pos)
            # Mise à jour initiale de son knowledge
            agent.knowledge.update(self.get_percepts(agent))
            agent.visited.add(agent.pos) 

        
        # Robot jaune dans la zone verte ou jaune
        for i, agent in enumerate(self.yellow_agents):
            agent.ID = (i+1)*100/self.n_yellow
            yellow_pos = (random.randint(self.ZONE_GREEN[0], self.ZONE_YELLOW[1]), random.randint(0, self.grid.height - 1))
            self.grid.place_agent(agent, yellow_pos)
            # Mise à jour initiale de son knowledge
            agent.knowledge.update(self.get_percepts(agent))
            agent.visited.add(agent.pos) 

        
        # Robot rouge dans la zone verte, jaune ou rouge
        for i, agent in enumerate(self.red_agents):
            agent.ID = (i+1)*100/self.n_red
            red_pos = (random.randint(self.ZONE_GREEN[0], self.ZONE_RED[1]), random.randint(0, self.grid.height - 1))
            self.grid.place_agent(agent, red_pos)
            # Mise à jour initiale de son knowledge
            agent.knowledge.update(self.get_percepts(agent))
            agent.visited.add(agent.pos) 


    def setup_initial_waste(self):
        """Place un déchet initial dans la zone verte."""
        waste_pos = (random.randint(self.ZONE_GREEN[0], self.ZONE_GREEN[1]), random.randint(0, self.grid.height - 1))
        waste = Waste(self, waste_type="green")
        self.grid.place_agent(waste, waste_pos)

    def setup_wastes(self):
        """Place aléatoirement plusieurs déchets de plusieurs types"""
        for _ in range(self.n_wastes):
            waste_color = random.randint(0,2)
            if waste_color==0:
                waste_pos = (random.randint(self.ZONE_GREEN[0], self.ZONE_GREEN[1]), random.randint(0, self.grid.height - 1))
                waste = Waste(self, waste_type="green")
                self.grid.place_agent(waste, waste_pos)
                self.green_wastes_remaining+=1
            if waste_color==1:
                waste_pos = (random.randint(self.ZONE_GREEN[0], self.ZONE_YELLOW[1]), random.randint(0, self.grid.height - 1))
                waste = Waste(self, waste_type="yellow")
                self.grid.place_agent(waste, waste_pos)
                self.yellow_wastes_remaining+=1
            if waste_color==2:
                waste_pos = (random.randint(self.ZONE_GREEN[0], self.ZONE_RED[1]-1), random.randint(0, self.grid.height - 1))
                waste = Waste(self, waste_type="red")
                self.grid.place_agent(waste, waste_pos)
                self.red_wastes_remaining+=1

    def setup_disposal_zone(self):
        """Configure la zone de dépôt final."""
        for y in range(self.grid.height):
            disposal = WasteDisposalZone(self)
            self.grid.place_agent(disposal, (self.grid.width - 1, y))

    def get_percepts(self, agent):
        """Retourne les informations sur l'environnement autour de l'agent."""
        # Obtenir les cellules voisines et leur contenu
        neighbors = self.grid.get_neighborhood(agent.pos, moore=False, include_center=True) # retourne les 5 cases (ou moins si bord de map) sous forme d'une liste de tuples (x,y)
        neighbors = [pos for pos in neighbors if pos != agent.pos]  # Enlever la case correspondant à la position de l'agent

        percepts = {}
        
        for pos in neighbors:
            cell_content = self.grid.get_cell_list_contents([pos]) #retourne une liste d'objets présents dans la case

            if cell_content and any(isinstance(obj, Radioactivity) and obj.zone in agent.allowed_zones for obj in cell_content): #la où l'agent peut aller (sa zone)
                percepts[pos] = cell_content

        return percepts #c'est donc un dico de 4 cases avec pour chaque case une liste d'objets présents dans la case

    def do(self, agent, action):
        """Exécute une action et retourne les nouvelles perceptions."""
        print(f"{agent.robot_type} robot at {agent.pos} doing: {action}")

        # Différentes actions possibles fonction de la stratégie    
        if action == "search_waste":
            self.searching_waste(agent)
        
        elif action == "move_left":
            print(f"{agent.robot_type} robot moving left")
            self.move_to_target(agent, (agent.pos[0] - 1, agent.pos[1]))
        
        elif action == "move_right":
            print(f"{agent.robot_type} robot moving right")
            self.move_to_target(agent, (agent.pos[0] + 1, agent.pos[1]))

        elif action == "move_up":
            print(f"{agent.robot_type} robot moving up")
            self.move_to_target(agent, (agent.pos[0], agent.pos[1] + 1))
        
        elif action == "move_down":
            self.move_to_target(agent, (agent.pos[0], agent.pos[1] - 1))
                
        elif action == "drop_waste":
            x, y = agent.pos
            waste = agent.inventory[0]
            self.grid.place_agent(waste, (x, y)) if agent.robot_type != "red" else None

            if waste.waste_type == "green":
                self.green_wastes_remaining += 1
                self.latent_green -= 1
            elif waste.waste_type == "yellow":
                self.yellow_wastes_remaining += 1
                self.latent_yellow -= 1
            elif waste.waste_type == "red":
                self.red_wastes_remaining += 1
                #pas de latent red
                
            agent.inventory = []
            agent.weight_inventory = 0
            agent.just_dropped = True #Flag pour empêcher de ramasser un déchet juste après avoir déposé
            print(f"{agent.robot_type} robot dropped waste")
            #data collector red si depot final
            self.red_wastes_returned += 1 if agent.robot_type == "red" else 0
            
        elif action == "deliberate_1_go_to_drop":
            # L'agent se déplace vers la colonne de dépôt
            target_column = self.ZONE_WIDTH - 1 if agent.robot_type == "green" else 2 * self.ZONE_WIDTH - 1 if agent.robot_type == "yellow" else self.grid.width - 1
            self.move_towards_column(agent, target_column)
        
        
        # Collecte de déchet si agent sur case avec déchet et place dans l'inventaire
        if agent.weight_inventory < 2 and not agent.just_dropped:
            # Vérifier si l'agent est sur une cellule avec un déchet
            cell_contents = self.grid.get_cell_list_contents([agent.pos])
            for obj in cell_contents:
                if isinstance(obj, Waste) and obj.waste_type == agent.robot_type:
                    # Collecter le déchet
                    agent.inventory.append(obj)
                    agent.weight_inventory += 1 if agent.robot_type != "red" else 2
                    agent.got_waste = True
                    self.grid.remove_agent(obj)
                    print(f"{agent.robot_type} robot collected a {obj.waste_type} waste")

                    #data collector
                    self.total_collected_wastes += 1
                    if agent.robot_type=='green':
                        self.green_wastes_remaining-=1
                        self.latent_green+=1
                    if agent.robot_type=='yellow':
                        self.yellow_wastes_remaining-=1
                        self.latent_yellow+=1
                    if agent.robot_type=='red':
                        self.red_wastes_remaining-=1

                    break


        # Fusionner 2 items identiques (sauf si agent rouge)
        if len(agent.inventory)==2 and agent.robot_type != "red":
            agent.inventory=[]
            agent.weight_inventory=0
            if agent.robot_type == "green":
                waste = Waste(self, waste_type="yellow")
                agent.inventory=[waste]
                agent.weight_inventory += 2
                self.yellow_wastes_remaining+=1
                self.latent_green-=2
                self.latent_yellow+=1
                print("fusion yellow")
            elif agent.robot_type == "yellow":
                waste = Waste(self, waste_type="red")
                agent.inventory=[waste]
                agent.weight_inventory += 2
                self.red_wastes_remaining+=1
                self.latent_yellow-=2
                print("fusion red")
            
            #data collector
            self.fused_wastes_count += 1


        agent.got_waste=False
        agent.just_dropped = False  # Reset pour le prochain tour

        # Retourner les nouvelles perceptions
        return self.get_percepts(agent)
    

    def move_to_target(self, agent, target_pos):
        """Deplace l'agent vers une position cible."""
        # Vérifier si la position cible est dans les zones autorisées du robot
        if self.is_position_allowed(agent, target_pos):
            self.grid.move_agent(agent, target_pos)
            print(f"{agent.robot_type} robot moved to {target_pos}")
        else:
            print(f"{agent.robot_type} robot cannot move from {agent.pos}")


    def checkwaste(self, agent):
        """Vérifie si il y a un déchet ramassable à proximité de l'agent."""
        # Obtenir toutes les cellules voisines
        neighbors = self.grid.get_neighborhood(agent.pos, moore=False, include_center=False)
        neighbors = [pos for pos in neighbors if pos != agent.pos]  # Enlever la case correspondant à la position de l'agent

        for pos in neighbors:
            cell_content = self.grid.get_cell_list_contents([pos]) #retourne une liste d'objets présents dans la case

            # Mouvement vers obj le plus proche
            if self.is_position_allowed(agent, pos) and cell_content and any(isinstance(obj, Waste) and obj.waste_type == agent.robot_type for obj in cell_content):
                return True, pos
            
        return False, None  # Aucun déchet trouvé à proximité


    def searching_waste(self, agent):
        """Déplace l'agent de manière aléatoire dans sa zone autorisée sauf si il voit un waste il le ramasse."""
        possible_moves = []
        
        # Obtenir toutes les cellules voisines
        neighbors = self.grid.get_neighborhood(agent.pos, moore=False, include_center=False)
        neighbors = [pos for pos in neighbors if pos != agent.pos]  # Enlever la case correspondant à la position de l'agent

        for pos in neighbors:
            if self.is_position_allowed(agent, pos):
                possible_moves.append(pos)

        #Mouvement aléatoire si aucun déchet trouvé
        if possible_moves:
            new_position = random.choice(possible_moves)
            self.grid.move_agent(agent, new_position)
    


    def move_towards_column(self, agent, target_column):
        """Déplace l'agent vers une colonne cible en allant simplement à droite."""
        current_x, current_y = agent.pos
        
        # Vérifier si le mouvement à droite est autorisé
        new_position = (current_x + 1, current_y)
        if self.is_position_allowed(agent, new_position):
            self.grid.move_agent(agent, new_position)
            print(f"{agent.robot_type} robot moved right towards column {target_column}, now at {new_position}")
        else:
            print(f"{agent.robot_type} robot cannot move right from {agent.pos}")
    
    def is_position_allowed(self, agent, position):
        """Vérifie si la position est autorisée pour le robot."""
        x, y = position
        
        # Définir les zones autorisées en fonction du type de robot
        if agent.robot_type == "green":
            # Robot vert: uniquement zone verte (colonnes 0-2)
            return self.ZONE_GREEN[0] <= x <= self.ZONE_GREEN[1]
        elif agent.robot_type == "yellow":
            # Robot jaune: zone jaune (colonnes 3-5) + dernière colonne verte (colonne 2)
            return self.ZONE_GREEN[0] <= x <= self.ZONE_YELLOW[1]
        elif agent.robot_type == "red":
            # Robot rouge: zone rouge (colonnes 6-8) + dernière colonne jaune (colonne 5)
            return self.ZONE_GREEN[0] <= x <= self.ZONE_RED[1]

    
    def deliberate_1_checkdrop(self, agent):
        """Vérifie si un robot est sur la dernière colonne de sa zone."""
        if agent.robot_type == "green":
            return agent.pos[0] == self.ZONE_GREEN[1]
        elif agent.robot_type == "yellow":
            return agent.pos[0] == self.ZONE_YELLOW[1] 
        elif agent.robot_type == "red":
            return agent.pos[0] == self.ZONE_RED[1] 
    

    def deliberate_3_checkdrop(self, agent):
        """Vérifie si un robot est sur la case du haut de la dernière colonne de sa zone."""
        if agent.robot_type == "green":
            return agent.pos[0] == self.ZONE_GREEN[1] and agent.pos[1] == self.grid.height - 1
        elif agent.robot_type == "yellow":
            return agent.pos[0] == self.ZONE_YELLOW[1] and agent.pos[1] == self.grid.height - 1
        elif agent.robot_type == "red":
            return agent.pos[0] == self.ZONE_RED[1]
        

    def step(self):
        """Avance la simulation d'un pas."""
        self.time_step += 1
        #print("================================", self.strategy, "================================")
        # Ne faire avancer que les robots, pas les objets Radioactivity
        self.datacollector.collect(self)
        for agent in list(self.agents):
            if isinstance(agent, (GreenRobot, YellowRobot, RedRobot)):
                print(type(agent))
                agent.step_agent()