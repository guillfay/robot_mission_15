# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa.visualization import SolaraViz, make_space_component
from model import RobotMission
from agents import GreenRobot, YellowRobot, RedRobot
from objects import Waste, Radioactivity, WasteDisposalZone

def agent_portrayal(agent):
    if isinstance(agent, GreenRobot):
        return {"color": "#00FF00", "size": 150, "text": "G", "zorder": 1}
    elif isinstance(agent, YellowRobot):
        return {"color": "#FFFF00", "size": 150, "text": "Y", "zorder": 1}
    elif isinstance(agent, RedRobot):
        return {"color": "#FF0000", "size": 150, "text": "R", "zorder": 1}
    elif isinstance(agent, Waste):
        if agent.waste_type == "green":
            return {"color": "#90EE90", "size": 150, "text": "W", "marker": "s"}
        elif agent.waste_type == "yellow":
            return {"color": "#FFFF99", "size": 150, "text": "W", "marker": "s"}
        elif agent.waste_type == "red":
            return {"color": "#FFA07A", "size": 150, "text": "W", "marker": "s"}
    elif isinstance(agent, Radioactivity):
        if agent.zone == 3:
            return {"color": "#FFEBEE", "size": 300, "text": "", "marker": "s", "zorder": 0}
        elif agent.zone == 2:
            return {"color": "#FFFFF0", "size": 300, "text": "", "marker": "s", "zorder": 0}
        elif agent.zone == 1:
            return {"color": "#E8F8E8", "size": 300, "text": "", "marker": "s", "zorder": 0}
        
        
    elif isinstance(agent, WasteDisposalZone):
        return {"color": "#ffffff", "size": 300, "text": "DISPOSAL", "marker": "s", "zorder": 0}

# Paramètres du modèle
model_params = {
    "width":{
        "type": "SliderInt",
        "value": 9,
        "label": "Grid width",
        "min": 3,
        "max": 50,
        "step": 1},

    "height": {
        "type": "SliderInt",
        "value": 3,
        "label": "Grid height",
        "min": 1,
        "max": 50,
        "step": 1}
}

# Création du modèle et de la visualisation
robot_model = RobotMission()
SpaceGraph = make_space_component(agent_portrayal)

page = SolaraViz(
    robot_model,
    components=[SpaceGraph],
    model_params=model_params,
    name="Robot Mission",
)

page

# Ligne de commande pour run le serveur : 
"""

python3 -m solara run server.py

"""
