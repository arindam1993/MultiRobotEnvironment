'''
Created on Jan 16, 2015

@author: Arindam
'''

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from numpy import *
from World import *
from Agent import Agent
from Obstacle import *
from pylab import *
from Ball import Ball
from LinearAlegebraUtils import distBetween
from RunAtBallBrain import RunAtBallBrain
from Team import Team
from matplotlib import animation


#Called once for initialization
'''
Usage guidelines:
1. Define globals required for the simulation in the __init__ constructor, here we define a bunch of waypoints for the ball
2. Initialize the globals in the setup() method. 
'''

class Simulator(object):
    def __init__(self, world, simTime, fps, imageDirName):
        self.world = world
        self.simTime = simTime
        self.fps = fps
        self.imageDirName = imageDirName
        self.currWP = 0
        self.ballWPs = [array([50.0, -100.0, 0.0]), array([0.0, 100.0, -70.0]), array([50.0, 20.0, 100.0]),array([-30.0, 50.0, -100.0]), array([80.0, -50.0, 50.0]), array([80.0, -50.0, -50.0]), array([-65.0, 20.0, 50.0]), array([-50.0, 20.0, -60.0])]
        self.fig = plt.figure(figsize=(16,12))


    def setup(self):
        #define teams which the agents can be a part of
        teamA = Team("A", '#ff99ff')
        teamB = Team("B", '#ffcc99')
        #Defining a couple of agents 
        ag1Pos = array([80, 50, -20])
        ag1Rot = array([30, 0, 0])
        ag1Brain = RunAtBallBrain()
        agent1 = Agent(teamA, ag1Pos, ag1Rot, ag1Brain, 5, 5)
         
         
        ag2Pos = array([-80, 0, 0])
        ag2Rot = array([0, 0, 0])
        ag2Brain = RunAtBallBrain()
        agent2 = Agent(teamA, ag2Pos, ag2Rot, ag2Brain, 5, 5)
         
        ag3Pos = array([70, 30, 50])
        ag3Rot = array([0, 0, 0])
        ag3Brain = RunAtBallBrain()
        agent3 = Agent(teamB, ag3Pos, ag3Rot, ag3Brain, 5, 5)
         
        ag4Pos = array([-80, 20, 60])
        ag4Rot = array([0, 0, 0])
        ag4Brain = RunAtBallBrain()
        agent4 = Agent(teamB, ag4Pos, ag4Rot, ag4Brain, 5, 5)
         
        #Add the agent to the world
        self.world.agents.append(agent1)
        self.world.agents.append(agent2)
        self.world.agents.append(agent3)
        self.world.agents.append(agent4)

        #define a bunch of obstacles
        ob1Pos = array([-50,-50,-50])
        ob1 = Obstacle(ob1Pos, 30)
         
        ob2Pos = array([80,-50,-50])
        ob2 = Obstacle(ob2Pos, 20)
         
        #add obstacles to the world
        self.world.obstacles.append(ob1)
        self.world.obstacles.append(ob2)
        
        #define a ball
        ball = Ball(array([0, 0, 0]))
        
        
        #add the ball to the world
        self.world.balls.append(ball)
        
    # called at a fixed 30fps always
    # physics simulation
    def fixedLoop(self):
        for agent in self.world.agents:
            agent.moveAgent(self.world)
         
        for ball in self.world.balls:  
            if len(self.ballWPs) > 0:  
                ball.moveBall(self.ballWPs[0], 1)
                if distBetween(ball.position, self.ballWPs[0]) < 0.5:
                    if len(self.ballWPs) > 0:
                        self.ballWPs.remove(self.ballWPs[0])

    
    #Called at specifed fps
    def loop(self, ax):       
        self.world.draw(ax)

    # advances simulation 1 tick, returns the current world state plot
    def tick(self):
        self.fixedLoop()

        self.fig.clf()
        ax = self.fig.add_subplot(111, projection='3d')
        ax.view_init(elev = 30)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        return self.loop(ax), plt.gca().set_ylim(ax.get_ylim()[::-1])

def tick(i):
    return sim.tick()

FPS = 30 # hardcoded into simulation assumptions

world = World(100, 100)
sim = Simulator(world, 10, FPS, "images")

# simulator assumes its physics simulation is running at dt = 1/30 s
# would have to recalculate the true animation framerate (to get physically accurate speeds, etc)
# if you change the raw sample rate of the animator function (which accepts arguments in ms)
simlen = 10 # sec
frames = FPS * simlen

ani = animation.FuncAnimation(sim.fig, tick, frames=frames, blit=True, init_func=sim.setup)

ani.save('output.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
