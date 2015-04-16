'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Arindam Bose (arindam.1993@gmail.com), Tucker Balch (trbalch@gmail.com)
'''


import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from World import *
from Agent import Agent, RestrictedAgent
from Obstacle import *
from pylab import *
from Ball import Ball
from LinearAlegebraUtils import distBetween
from PreyBrain import PreyBrain
from PredatorBrain import PredatorBrain
from Team import Team
from SimTime import SimTime
from StatsTracker import StatsTracker
import random



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

    def setup(self):    
        #setup directory to save the images
        try:
            os.mkdir(self.imageDirName)
        except:
            print self.imageDirName + " subdirectory already exists. OK."

  
         #define teams which the agents can be a part of
        predator = Team("Predator", '#ff99ff')
        prey = Team("Prey", '#ffcc99')
        #Defining a couple of agents 

        #predator and prey counts
        predatorCount = 5
        preyCount = 10
        displacement = array([0, 20, 0])

        #initial seed positions
        predatorPos = array([20, 0, 0])
        preyPos = array([0, 0, 0])

        #set seed for randomly placing predators
        random.seed(20)

        #initialize predators
        for i in range(0, predatorCount):
            brain = PredatorBrain()
            x = random.random() * 30
            y = random.random() * 30
            z = random.random() * 30
            newDisplacement = array([x, y, z])
            agent = Agent(predator, predatorPos, array([0, 0, 0]), brain, 5, 5, 5)
            self.world.addAgent(agent)
            predatorPos+=newDisplacement

        #initialize prey
        for i in range(0, preyCount):
            brain = PreyBrain()
            agent = RestrictedAgent(prey, preyPos, array([0, 0, 0]), brain, 2, 200, 2, 2)
            self.world.addAgent(agent)
            preyPos+=displacement

#         
        #define a bunch of obstacles
        ob1Pos = array([-50,-50,-50])
        ob1 = Obstacle(ob1Pos, 30)
         
        ob2Pos = array([80,-50,-50])
        ob2 = Obstacle(ob2Pos, 20)

        originRef = Obstacle(array([0.1, 0.1, 0.1]), 10)
         
        #add obstacles to the world
        self.world.addObstacle(ob1)
        self.world.addObstacle(originRef)
        
        
#called at a fixed 30fps always
    def fixedLoop(self):
        for agent in self.world.agents:
            agent.moveAgent(self.world)

        for ball in self.world.balls:  
            if len(self.ballWPs) > 0:  
                ball.moveBall(self.ballWPs[self.currWP], 1)
                if distBetween(ball.position, self.ballWPs[self.currWP]) < 0.5:
                    self.currWP = (self.currWP + 1)%len(self.ballWPs)
                    # if len(self.ballWPs) > 0:
                    #     self.ballWPs.remove(self.ballWPs[0])

    
#Called at specifed fps
    def loop(self, ax):       
        self.world.draw(ax)
       
                
    def run(self):
        #Run setup once
        self.setup()
        
        #Setup loop
        timeStep = 1/double(30)
        frameProb = double(self.fps) / 30
        currTime = double(0)
        SimTime.fixedDeltaTime = timeStep
        SimTime.deltaTime = double(1/ self.fps)
        drawIndex = 0
        physicsIndex = 0
        while(currTime < self.simTime):
            self.fixedLoop()
            SimTime.time = currTime
            currProb = double(drawIndex)/double(physicsIndex+1)
            if currProb < frameProb:
                self.drawFrame(drawIndex)  
                drawIndex+=1
            physicsIndex+=1
            currTime+=double(timeStep)

     
        print "Physics ran for "+str(physicsIndex)+" steps"
        print "Drawing ran for "+str(drawIndex)+" steps"
        print "Agents were stunned for"+str(StatsTracker.stunTimeDict)
            
    def drawFrame(self, loopIndex):
        fig = plt.figure(figsize=(16,12))
        ax = fig.add_subplot(111, projection='3d') 
        ax.view_init(elev = 30)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")    
        fname = self.imageDirName + '/' + str(int(100000000+loopIndex)) + '.png' # name the file 
        self.loop(ax)
        plt.gca().set_ylim(ax.get_ylim()[::-1])
        savefig(fname, format='png', bbox_inches='tight')
        print 'Written Frame No.'+ str(loopIndex)+' to '+ fname
        plt.close()


#Simulation runs here
#set the size of the world
world = World(150, 150)
#specify which world to simulate, total simulation time, and frammerate for video
sim = Simulator(world, 120, 30, "images")
#run the simulation
sim.run()

'''
To create a video using the image sequence, execute the following command in command line.
>ffmpeg -framerate 30 -i "1%08d.png" -r 30 outPut.mp4
                    ^                    ^
                Framerate mtached with simulator
Make sure to set your current working directory to /images and have ffmpeg in your path.
'''

    
