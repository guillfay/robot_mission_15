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


