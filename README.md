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

### 4. Environment Objects

### 5. Server

### 6. Strategies


