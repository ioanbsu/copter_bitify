import os
import time
import math
import sys

import smbus
from bitify.python.sensors import imu
from bitify.python.utils.i2cutils import i2c_raspberry_pi_bus_number


Q1_MOTOR_ADDRESS = 4
Q2_MOTOR_ADDRESS = 3
Q3_MOTOR_ADDRESS = 1
Q4_MOTOR_ADDRESS = 0

MOTOR_STOPPED = 450

ALPHA_CONSTANT = 4

G_MATRIX = [0.5, 0.5, 0.2]

averagePeriod = 20
flySeconds = 1
init_torque = 200
if len(sys.argv) == 3:
    flySeconds = int(sys.argv[1])
    init_torque = int(sys.argv[2])

print "Running time:{0}; torque: {1}".format(flySeconds, init_torque)

bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu_controller = imu.IMU(bus, 0x69, 0x53, 0x1e, "IMU")
imu_controller.set_compass_offsets(72, 72, -30)


def sin(angle):
    return math.sin(angle)


def cos(yRotation):
    return math.cos(yRotation)


def calculateTorques(pitch, roll, yaw, ang_vel_x, ang_vel_y, ang_vel_z):
    xTorque = -1 * G_MATRIX[0] * ang_vel_x - ALPHA_CONSTANT * (
        sin(roll / 2) * cos(pitch / 2) * cos(yaw / 2) -
        cos(roll / 2) * sin(pitch / 2) * sin(yaw / 2))
    yTorque = -1 * G_MATRIX[0] * ang_vel_y - ALPHA_CONSTANT * (
        cos(roll / 2) * sin(pitch / 2) * cos(yaw / 2) +
        sin(roll / 2) * cos(pitch / 2) * sin(yaw / 2))
    zTorque = -1 * G_MATRIX[0] * ang_vel_z - ALPHA_CONSTANT * (
        cos(roll / 2) * cos(pitch / 2) * sin(yaw / 2) -
        sin(roll / 2) * sin(pitch / 2) * cos(yaw / 2))
    return [xTorque, yTorque, zTorque]


def calculateMotorSpeeds(torques, T):
    a1, a2, a3 = 62695.9247649, 227272.72727272727, 8620.690
    t1, t2, t3 = torques[0], torques[1], torques[2]
    constantDesiredTorque = T * a3
    w1 = max(t2 * a1 + t3 * a2 + constantDesiredTorque, 0)
    w2 = max(t1 * a1 - t3 * a2 + constantDesiredTorque, 0)
    w3 = max(- t2 * a1 + t3 * a2 + constantDesiredTorque, 0)
    w4 = max(- t1 * a1 - t3 * a2 + constantDesiredTorque, 0)

    # print " {0},{1},{2},{3}".format(math.sqrt(w1), math.sqrt(w2), math.sqrt(w3), math.sqrt(w4))
    return [math.sqrt(w1), math.sqrt(w2), math.sqrt(w3), math.sqrt(w4)]


def runMotors(q1, q3, q2, q4):
    os.system(
        "echo {0}={1} > /dev/servoblaster;"
        "echo {2}={3} > /dev/servoblaster;"
        "echo {4}={5} > /dev/servoblaster;"
        "echo {6}={7} > /dev/servoblaster;".format(int(Q1_MOTOR_ADDRESS), int(q1),
                                                   int(Q2_MOTOR_ADDRESS), int(q2),
                                                   int(Q3_MOTOR_ADDRESS), int(q3),
                                                   int(Q4_MOTOR_ADDRESS), int(q4)))


millis = int(round(time.time() * 1000))

while millis + flySeconds * 1000 > int(round(time.time() * 1000)):
    (pitch, roll, yaw, ang_vel_x, ang_vel_y, ang_vel_z) = imu_controller.read_pitch_roll_yaw_with_speeds()
    yaw -= math.pi
    torques = calculateTorques(pitch, roll, yaw, ang_vel_x, ang_vel_y, ang_vel_z)
    motorSpeeds = calculateMotorSpeeds(torques, init_torque)
    adjusted = 2350
    q1 = MOTOR_STOPPED + int(motorSpeeds[0] - adjusted) / 5
    q2 = MOTOR_STOPPED + int(motorSpeeds[1] - adjusted) / 5
    q3 = MOTOR_STOPPED + int(motorSpeeds[2] - adjusted) / 5
    q4 = MOTOR_STOPPED + int(motorSpeeds[3] - adjusted) / 5
    print "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}".format(q1, q3, q2, q4,
                                                                          torques[0], torques[1], torques[2],
                                                                          pitch, roll, yaw,
                                                                          ang_vel_x, ang_vel_y, ang_vel_z)
    runMotors(q1, q3, q2, q4)
else:
    runMotors(MOTOR_STOPPED, MOTOR_STOPPED, MOTOR_STOPPED, MOTOR_STOPPED)