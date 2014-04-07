__author__ = 'ivanbahdanau'

import math


def rotate_around_z(angle, x, y):
    radiansAroundZ = math.radians(angle)
    newX = (math.cos(radiansAroundZ) * x - math.sin(radiansAroundZ) * y)
    newY = math.sin(radiansAroundZ) * x + math.cos(radiansAroundZ) * y
    return (newX, newY)

def rotate_around_roll(angle_radians, pitch, yaw):
    newPitch = (math.cos(angle_radians) * pitch - math.sin(angle_radians) * yaw)
    newYaw = math.sin(angle_radians) * pitch + math.cos(angle_radians) * yaw
    return (newPitch, newYaw)