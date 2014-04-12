import os

import smbus
from CopterMotorTorquesResolver import CopterMotorTorquesResolver, MOTOR_STOPPED
import FileUtils as FileUtils
from bitify.python.sensors import imu
from bitify.python.utils.i2cutils import i2c_raspberry_pi_bus_number


Q1_MOTOR_ADDRESS = 4
Q2_MOTOR_ADDRESS = 3
Q3_MOTOR_ADDRESS = 1
Q4_MOTOR_ADDRESS = 0


def runMotors(q1, q2, q3, q4):
    os.system(
        "echo {0}={1} > /dev/servoblaster;"
        "echo {2}={3} > /dev/servoblaster;"
        "echo {4}={5} > /dev/servoblaster;"
        "echo {6}={7} > /dev/servoblaster;".format(int(Q1_MOTOR_ADDRESS), int(q1),
                                                   int(Q2_MOTOR_ADDRESS), int(q2),
                                                   int(Q3_MOTOR_ADDRESS), int(q3),
                                                   int(Q4_MOTOR_ADDRESS), int(q4)))


bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu_controller = imu.IMU(bus, 0x69, 0x53, 0x1e, "IMU")
imu_controller.set_compass_offsets(72, 72, -30)

motorTorques = CopterMotorTorquesResolver()

while True:
    (copter_is_on, copter_torque, is_kill, control_force,z_axe_control) = FileUtils.read_file_data()
    (pitch, roll, yaw, roll_vel, pitch_vel, yaw_vel) = imu_controller.read_pitch_roll_yaw_with_speeds()
    roll -= 0.049156023
    pitch -= 0.005387534
    (rollTorque, pitchTorque, yawTorque) = motorTorques.calculateTorques(roll, pitch, yaw, roll_vel, pitch_vel,
                                                                         yaw_vel, control_force)
    motorSpeeds = motorTorques.calculateMotorSpeeds(rollTorque, pitchTorque, yawTorque, copter_torque,z_axe_control)
    (q1, q2, q3, q4) = motorTorques.calculate_motor_adjusted_speeds(motorSpeeds);
    # print "{0}    {1}    {2}    {3}  {4} {5} {6} {7} {8} {9}".format(q1, q2, q3, q4, rollTorque, pitchTorque, yawTorque,roll,pitch,yaw)
    if is_kill:
        FileUtils.write_file_data(True, 650, False,30,1000)
        runMotors(MOTOR_STOPPED, MOTOR_STOPPED, MOTOR_STOPPED, MOTOR_STOPPED)
        exit()
    if copter_is_on:
        print "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}".format(q1, q2, q3, q4,
                                                                              rollTorque, pitchTorque, yawTorque,
                                                                              roll, pitch, yaw,
                                                                              roll_vel, pitch_vel, yaw_vel)
        runMotors(q1, q2, q3, q4)
    else:
        runMotors(MOTOR_STOPPED, MOTOR_STOPPED, MOTOR_STOPPED, MOTOR_STOPPED)