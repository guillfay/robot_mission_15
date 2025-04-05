# Number of the group 15
# Date of creation 11/03/2025 
# Names of the members of the group : Erwan DAVID, Guillaume FAYNOT

from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from model import RobotMission
from agents import GreenRobot, YellowRobot, RedRobot
from objects import Waste, Radioactivity, WasteDisposalZone



def agent_portrayal(agent):
    if isinstance(agent, GreenRobot):
        return {"color": "#00cb4d", "size": 150, "text": "G", "zorder": 1}
    elif isinstance(agent, YellowRobot):
        return {"color": "#FCDC12", "size": 150, "text": "Y", "zorder": 1}
    elif isinstance(agent, RedRobot):
        return {"color": "#c80202", "size": 150, "text": "R", "zorder": 1}
    elif isinstance(agent, Waste):
        if agent.waste_type == "green":
            return {"color": "#4dcb7d", "size": 150, "text": "W", "marker": "^"}
        elif agent.waste_type == "yellow":
            return {"color": "#FFE645", "size": 150, "text": "W", "marker": "^"}
        elif agent.waste_type == "red":
            return {"color": "#c54d4d", "size": 150, "text": "W", "marker": "^"}
    elif isinstance(agent, Radioactivity):
        if agent.zone == 3:
            return {"color": "#FFEBEE", "size": 700, "text": "", "marker": "s", "zorder": 0} # rouge
        elif agent.zone == 2:
            return {"color": "#FFFFF0", "size": 700, "text": "", "marker": "s", "zorder": 0} # jaune
        elif agent.zone == 1:
            return {"color": "#E8F8E8", "size": 700, "text": "", "marker": "s", "zorder": 0} # vert
        
        
    elif isinstance(agent, WasteDisposalZone):
        return {"color": "#ffffff", "size": 700, "text": "DISPOSAL", "marker": "s", "zorder": 0}

# Paramètres du modèle
model_params = {
    "width":{
        "type": "SliderInt",
        "value": 13,
        "label": "Grid width",
        "min": 5,
        "max": 50,
        "step": 1},

    "height": {
        "type": "SliderInt",
        "value": 11,
        "label": "Grid height",
        "min": 3,
        "max": 50,
        "step": 1},
    
    "n_green": {
        "type": "SliderInt",
        "value": 2,
        "label": "Green agents",
        "min": 0,
        "max": 10,
        "step": 1},

    "n_yellow": {
        "type": "SliderInt",
        "value": 2,
        "label": "Yellow agents",
        "min": 0,
        "max": 10,
        "step": 1},
    
    "n_red": {
        "type": "SliderInt",
        "value": 2,
        "label": "Red agents",
        "min": 0,
        "max": 10,
        "step": 1},

    "n_wastes": {
        "type": "SliderInt",
        "value": 10,
        "label": "Wastes",
        "min": 0,
        "max": 30,
        "step": 1},
    
    "strategy": {
        "type": "SliderInt",
        "value": 3,
        "label": "Strategy",
        "min": 1,
        "max": 3,
        "step": 1},
    
}

# Création du modèle et de la visualisation
robot_model = RobotMission()
SpaceGraph = make_space_component(agent_portrayal)
WastesRemaining = make_plot_component({"GreenWastesRemaining" : "g",  "GreenLatentWastes": "mediumseagreen", "YellowWastesRemaining" : "gold", "YellowLatentWastes" : "yellow", "RedWastesRemaining" : 'r'})
FusedWastes = make_plot_component("FusedWastes")
CollectedWastes = make_plot_component("CollectedWastes")
RedWastesDeposited = make_plot_component("RedWastesDeposited")

page = SolaraViz(
    robot_model,
    components=[SpaceGraph, WastesRemaining, FusedWastes, CollectedWastes, RedWastesDeposited],
    model_params=model_params,
    name="Robot Mission",
)

page

# Ligne de commande pour run le serveur : 
"""

python -m solara run server.py

"""
