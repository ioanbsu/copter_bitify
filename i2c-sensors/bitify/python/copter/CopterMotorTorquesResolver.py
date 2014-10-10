__author__ = 'ivanbahdanau'

import math

G_MATRIX = [0.5, 0.5, 0.2]

MOTOR_STOPPED = 450

def sin(angle):
    return math.sin(angle)


def cos(angle):
    return math.cos(angle)


class CopterMotorTorquesResolver(object):
    def calculateTorques(self,roll, pitch, yaw, roll_vel, pitch_vel, yaw_vel,control_force):
        tempTorque = roll
        # roll = pitch +0.04
        # pitch = tempTorque - 0.03

        rollTorque = -1 * G_MATRIX[0] * roll_vel - control_force * (
            sin(roll / 2) * cos(pitch / 2) * cos(yaw / 2) -
            cos(roll / 2) * sin(pitch / 2) * sin(yaw / 2))
        pitchTorque = -1 * G_MATRIX[1] * pitch_vel - control_force * (
            cos(roll / 2) * sin(pitch / 2) * cos(yaw / 2) +
            sin(roll / 2) * cos(pitch / 2) * sin(yaw / 2))
        yawTorque = -1 * G_MATRIX[2] * yaw_vel - control_force * (
            cos(roll / 2) * cos(pitch / 2) * sin(yaw / 2) -
            sin(roll / 2) * sin(pitch / 2) * cos(yaw / 2))
        return (rollTorque, pitchTorque, yawTorque)


    def calculateMotorSpeeds(self,rollTorque, pitchTorque, yawTorque, T,z_axe_control):
        a1, a2, a3 = 62695.9247649, z_axe_control, 8620.690
        t1, t2, t3 = rollTorque, pitchTorque, yawTorque
        constantDesiredTorque = T * a3
        w1 = max(t2 * a1 + t3 * a2 + constantDesiredTorque, 0)
        w2 = max(t1 * a1 - t3 * a2 + constantDesiredTorque, 0)
        w3 = max(- t2 * a1 + t3 * a2 + constantDesiredTorque, 0)
        w4 = max(- t1 * a1 - t3 * a2 + constantDesiredTorque, 0)

        # print " {0},{1},{2},{3}".format(math.sqrt(w1), math.sqrt(w2), math.sqrt(w3), math.sqrt(w4))
        return [math.sqrt(w1), math.sqrt(w2), math.sqrt(w3), math.sqrt(w4)]

    def calculate_motor_adjusted_speeds(self, motorSpeeds):
        adjusted = 2350
        q1 = MOTOR_STOPPED + int(motorSpeeds[0] - adjusted) / 5
        q2 = MOTOR_STOPPED + int(motorSpeeds[1] - adjusted) / 5
        q3 = MOTOR_STOPPED + int(motorSpeeds[2] - adjusted) / 5
        q4 = MOTOR_STOPPED + int(motorSpeeds[3] - adjusted) / 5
        return (q1, q2, q3, q4)
