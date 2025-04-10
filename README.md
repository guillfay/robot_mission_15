# Multi-Agents Systems
## Self-organization of robots in a hostile environment
*# robot_mission_15*

The goal of this project is to create differents agents in an environment that are able to clear 3 areas of various radioactivity levels filled with nuclear watses.

*Group 15*
- Erwan DAVID
- Guillaume FAYNOT

## Requirements

Install the requirements in the file [`requirements.txt`]('./requirements.txt')

## Run the simulation environment

`python -m solara run server.py`

## Table of contents

1. [Introduction](#introduction)
2. [Agents](#agents)
3. [Model](#model)
4. [Objects](#enviornment-objects)
5. [Server](#server)
6. [Strategies](#strategies)

### 1. Introduction

Through this project, we model the mission of robots that have to collect dangerous waste, transform it and then transport it to a secure area. The robots navigate in an environment broken down into several zones where the level of radioactivity varies from low radioactive to highly radioactive. Robots only have access to specific areas matching their radioactivity levels. 
- **Green Zone** : low radioactivity zone
- **Yellow Zone** : medium radioactivity zone
- **Red Zone** : high radioactivity zone
The goal of this project is to create a cleanup multi-agents model with the most efficient strategy to clear all the radioactive wastes in all 3 zones.

### 2. Agents

As it was explained previously, there are 3 types of robots :
- **Green Robot** can carry 2 green wastes at a time. Once it has picked up 2 green wastes, it merges them into 1 yellow waste and puts it in the green deposit zone. It can only move into the green zone.
- **Yellow Robot** can carry 2 yellow wastes at a time. Once has picked up 2 yellow wastes, it merges them into 1 red waste and puts it in the yellow deposit zone. It can only move into the green and yellow zones.
- **Red Robot** can carry only 1 red waste at a time and and aims to put it in the red deposit zone. It can move into all zones.

As a first approach, the agents only have a few features and caracteristics : they move randomly into their allocated areas, skipping the cells they have already visited and choosing in priority the cells that contain a wast of their type. They can pick up to two wastes, merge them, and move towards their allocated deposit zone

```mermaid
classDiagram
    class RobotAgent {
        +dict knowledge
        +list inventory
        +int weight_inventory
        +bool got_waste
        +str robot_type
        +list allowed_zones
        +set visited
        +bool go_fuze
        +bool just_dropped
        +int ID
        +step_agent()
        +deliberate_1(knowledge)
        +deliberate_2(knowledge)
        +deliberate_3(knowledge)
        +move_towards(target_pos)
    }
    
    class GreenRobot {
        +deliberate_1(knowledge)
        +deliberate_2(knowledge)
        +deliberate_3(knowledge)
    }
    
    class YellowRobot {
        +deliberate_1(knowledge)
        +deliberate_2(knowledge)
    }

    class RedRobot {
        +deliberate_1(knowledge)
        +deliberate_2(knowledge)
    }
    
    RobotAgent <|-- GreenRobot
    RobotAgent <|-- YellowRobot
    RobotAgent <|-- RedRobot
```

**Attributes** like `knowledge`, `inventory`, `weight_inventory`, `visited`, and `allowed_zones` allow each robot to track its environment, carried waste, and movement restrictions.

**Methods** such as `step_agent` control the robot's behavior at each simulation step, deciding on actions based on a strategy (`deliberate_1`, `deliberate_2`, `deliberate_3`). Movement is managed with `move_towards`, and robots decide to pick up or drop waste according to their perceptions and inventory status.

The three `deliberate` methods represent different exploration strategies and will be detailed further on: random exploration (`deliberate_1`), targeted exploration of unvisited cells (`deliberate_2`), and a systematic "one-by-one" exploration (`deliberate_3`).


### 3. Model

The model is mainly repsonsible for the environment behavior, initialization of the agents and  running of the simulation.

The model is described by :
- `width`, `height` :  width and height of the grid
- `n_green`, `n_yellow`, `n_red` : number of robots of each type
- `n_wastes` : number of wastes

A grid is created with the proper dimensions and divided in 3 radioactive zones. All the robots and wastes are setup accordingly. We use a `DataCollector` to collect the data that is being used in further analysis of the simulation.

At each step, the robot agents perform differents tasks : 
- get the neighbor cells contents
- decide to move on a neighbor cell or collect a waste if possible
- merge wastes if 2 wastes are picked up, then move towards the deposit zone until it's reached.

Agents aren't allowed to communicate yet and only percieve their surrounding environment. The strategy here is to execute random moves, avoiding a cell that was just previously occupied by another robot or previously occupied by the robot itself.



### 4. Environment Objects

The environment objects are represented as agents to meet the Mesa library constraints. These agents do not have a proper behavior whatsoever, but it allows the environment to identify particular characteristics.

- **Waste** : this agent represents a waste to collect. Its main attribute is its type (green, yellow or red)

- **Radioactivity** : this agent represents the radioactivity of a zone. Its attributes are its zone ID (1 -> green, 2 -> yellow, etc) and its radioactivity level (green -> [0, 0.33], yellow -> [0.33, 0.66], red -> [0.66, 1]).

- **WasteDisposalZone** : this agent represents the waste disposal zone at the end of each zone


### 5. Server

By running server.py, a visulization window opens, allowing to see the simulation on a grid and a few plots : 

- RemainingWastes : counts the remaining wastes for each type.
- FusedWastes : counts all the wastes that have been merged, independently on the type.
- CollectedWastes : counts all the wastes that have been collected, independently on the type.
- RedWastesDeposit : counts all the red wastes that have been deposited.

### 6. Strategies

For this first iteration, we implemented 3 differents strategies, which can be changed using the corresponding cursor on the server web page.

- Strategie 1 : agents move totally randomly in their allowed area and try to get a waste. When exactly two wastes are collected, they move towards the deposit zone on the far right and drop a merge waste of another color

- Strategy 2 : agents move randomly in their allowed area, directy going to a corresponding waste in their neighborhood (if its inventory isn't full) or avoiding the areas it has already visited, and try to get a waste. When exactly two wastes are collected, they move towards the deposit zone on the far right and drop a merge waste of another color

- Strategy 3 : agents move randomly in their allowed area, directy going to a corresponding waste in their neighborhood (if its inventory isn't full) or avoiding the areas it has already visited, and try to get a waste. To avoid any latent waste (for example, an agent that has picked up a waste but can't find another one to merge), each agent goes to an intermediate desposit zone (1 cell) and drops the single waste he has. If a waste is already in the deposit zone, he picks up two wastes and merges them. The he goes to the deposit zone of the next color. Note : to optimize displacement of the agents, deposit zone for agents green and yellow are the same.

#### Performance

Ou objective is to build agents that can collect the most wastes as possible in the minimum amount of time.

Here are a performance plot for each strategy, with the same parameters (2 agents of each type and 15 random wastes).

**Strategy 1**

![Strategy 1 Performance](./strat1.png)

**Strategy 2**

![Strategy 2 Performance](./strat2.png)

**Strategy 3**

![Strategy 3 Performance](./strat3.png)

**Comparison Table**

The table below compares the number of wastes collected for each strategy after 280 steps:

| Strategy   | Total Wastes Collected |
|------------|------------------------|
| Strategy 1 | 33                     |
| Strategy 2 | 42                     |
| Strategy 3 | 61                     |

Strategy 3 seems to outperform the other two. We still need to run multiple simulations to verify this assumption.