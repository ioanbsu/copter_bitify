__author__ = 'ivanbahdanau'

import math
ALPHA_CONSTANT = 10

G_MATRIX = [0.5, 0.5, 0.2]

MOTOR_STOPPED = 450


def sin(angle):
    return math.sin(angle)


def cos(yRotation):
    return math.cos(yRotation)


def calculateTorques(roll, pitch, yaw, ang_vel_x, ang_vel_y, ang_vel_z):
    rollTorque = -1 * G_MATRIX[0] * ang_vel_x - ALPHA_CONSTANT * (
        sin(roll / 2) * cos(pitch / 2) * cos(yaw / 2) -
        cos(roll / 2) * sin(pitch / 2) * sin(yaw / 2))
    pitchTorque = -1 * G_MATRIX[1] * ang_vel_y - ALPHA_CONSTANT * (
        cos(roll / 2) * sin(pitch / 2) * cos(yaw / 2) +
        sin(roll / 2) * cos(pitch / 2) * sin(yaw / 2))
    yawTorque = -1 * G_MATRIX[2] * ang_vel_z - ALPHA_CONSTANT * (
        cos(roll / 2) * cos(pitch / 2) * sin(yaw / 2) -
        sin(roll / 2) * sin(pitch / 2) * cos(yaw / 2))
    return (rollTorque, pitchTorque, yawTorque)


def calculateMotorSpeeds(rollTorque, pitchTorque, yawTorque, T):
    a1, a2, a3 = 62695.9247649, 10000, 8620.690
    t1, t2, t3 = rollTorque, pitchTorque, yawTorque
    constantDesiredTorque = T * a3
    w1 = max(t2 * a1 + t3 * a2 + constantDesiredTorque, 0)
    w2 = max(t1 * a1 - t3 * a2 + constantDesiredTorque, 0)
    w3 = max(- t2 * a1 + t3 * a2 + constantDesiredTorque, 0)
    w4 = max(- t1 * a1 - t3 * a2 + constantDesiredTorque, 0)

    # print " {0},{1},{2},{3}".format(math.sqrt(w1), math.sqrt(w2), math.sqrt(w3), math.sqrt(w4))
    return [math.sqrt(w1), math.sqrt(w2), math.sqrt(w3), math.sqrt(w4)]


(rollTorque, pitchTorque, yawTorque) = calculateTorques(0.001805784, 0.187500545, -0.135503703, 0.026355179,
                                                        -0.006467172, 0.031989961)
print (rollTorque, pitchTorque, yawTorque)
motorSpeeds = calculateMotorSpeeds(rollTorque, pitchTorque, yawTorque, 1135)
adjusted = 2350
q1 = MOTOR_STOPPED + int(motorSpeeds[0] - adjusted) / 5
q2 = MOTOR_STOPPED + int(motorSpeeds[1] - adjusted) / 5
q3 = MOTOR_STOPPED + int(motorSpeeds[2] - adjusted) / 5
q4 = MOTOR_STOPPED + int(motorSpeeds[3] - adjusted) / 5
print (q1, q2, q3, q4)
