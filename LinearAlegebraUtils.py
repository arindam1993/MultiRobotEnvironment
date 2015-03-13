'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Arindam Bose (arindam.1993@gmail.com), Tucker Balch (trbalch@gmail.com)
'''


from numpy import *
import numpy as np

from math import sin, cos, radians
def rotMatrixFromYPR(rotation):
    a = radians(rotation[0])
    b = radians(rotation[1])
    c = radians(rotation[2])

    co = [cos(a),cos(b),cos(c)]
    si = [sin(a),sin(b),sin(c)]    

    rotMat = array([
                    [co[0]*co[1], si[0]*co[1], -si[1]],
                    [co[0]*si[1]*si[2] - si[0]*co[2], si[0]*si[1]*si[2] + co[0]*co[2], co[1]*si[2]],
                    [co[0]*si[1]*co[2] + si[0]*si[2], si[0]*si[1]*co[2] - co[0]*si[2], co[1]*co[2]]])
    return rotMat

def getYPRFromVector(vector):
    mag = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] )
    yaw = math.degrees(math.atan2(vector[1],vector[0]))
    pitch = -math.degrees(math.atan2(vector[2], mag))
    roll = 0
    return array([yaw, pitch, roll])

def distBetween(p1, p2):
    distVec = p2 - p1
    return np.linalg.norm(distVec)

def normalize(vector):
    mag = np.linalg.norm(vector)
    return vector/mag

def clampRotation(rotation, maxRot):
    if rotation[0] > 0:
        if rotation[0] > maxRot[0]:
            rotation[0] = maxRot[0]
    elif rotation[0] < 0:
        if -1 * rotation[0] > maxRot[0]:
            rotation[0] = -1 * maxRot[0]
    if rotation[1] > 0:
        if rotation[1] > maxRot[1]:
            rotation[1] = maxRot[1]
    elif rotation[1] < 0:
        if -1 * rotation[1] > maxRot[1]:
            rotation[1] = -1 * maxRot[1]
    if rotation[2] > 0:
        if rotation[2] > maxRot[2]:
            rotation[2] = maxRot[2]
    elif rotation[2] < 0:
        if -1 * rotation[2] > maxRot[2]:
            rotation[2] = -1 * maxRot[2]
    return rotation

def reflectVector(vector, normal):
    return -2 * dot(vector, normal) * normal + vector
        
        
incident = array([0, 0 , 1])
print reflectVector(incident, array([0, 0, -1]))
