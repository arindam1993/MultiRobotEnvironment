'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Arindam Bose (arindam.1993@gmail.com), Tucker Balch (trbalch@gmail.com)
'''

from Agent import Agent
from Ball import Ball
from Obstacle import Obstacle
from LinearAlegebraUtils import *
import numpy as np
from Action import Stun, Kick
import random
from NavUtils import getObstacleAvoidance, findNearestUnstunned, getTeamAvoidance
class PredatorBrain(object):
    '''
    classdocs
    '''


    def __init__(self):      
        pass
    
    def takeStep(self, myTeam=[], enemyTeam=[], balls=[], obstacles=[]):
        actions = []
        deltaPos = np.array([1, 0, 0])
        nearestUnstunnedAgent = findNearestUnstunned(enemyTeam)
        stunMovement = array([0, 0, 0])
        if nearestUnstunnedAgent.isStunned:
            stunMovement  = array([0, 0, 0])
        else:
            stunMovement = nearestUnstunnedAgent.position

        avoidObstacleMovement = getObstacleAvoidance(obstacles)
        avoidTeamMovement = getTeamAvoidance(myTeam)

        movement = normalize(1.5*stunMovement + 0.5*avoidObstacleMovement + 0.5*avoidTeamMovement)
        deltaRot = getYPRFromVector(movement)
        if distBetween(np.array([0, 0, 0]), nearestUnstunnedAgent.position) < nearestUnstunnedAgent.stunRange:
            actions.append(Stun(nearestUnstunnedAgent, 5))
 #           print "dist " + str(distBetween(np.array([0, 0, 0]), nearestUnstunnedAgent.position)) + " stunrange" + str(nearestUnstunnedAgent.stunRange)
            for teammate in myTeam:
                if((teammate.position==np.array([0.0, 0.0, 0.0])).all()):
 #                   print "Predator stunning itself"
                    actions.append(Stun(teammate, 1.25))

        return deltaPos, deltaRot, actions





        
