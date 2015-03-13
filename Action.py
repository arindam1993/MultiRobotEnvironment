'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Arindam Bose (arindam.1993@gmail.com), Tucker Balch (trbalch@gmail.com)
'''


class Stun(object):
    '''
    classdocs
    '''


    def __init__(self, agent, duration):
        '''
        Constructor
        '''
        self.agentToStun = agent
        self.agentUID = agent.uid
        self.duration = duration
        
        
class Kick(object):
    
    def __init__(self, ball, direction, intensity):
        self.ball = ball
        self.ballUID = ball.getUID()
        self.direction = direction
        self.intensity = intensity
        