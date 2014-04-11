__author__ = 'ivanbahdanau'


#!/usr/bin/env python

import sys

import smbus
import bitify.python.sensors.imu as imu
from bitify.python.utils.i2cutils import i2c_raspberry_pi_bus_number


bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu_controller = imu.IMU(bus, 0x69, 0x53, 0x1e, "IMU")
imu_controller.set_compass_offsets(41, 136, 9)


if len(sys.argv) >= 2 and sys.argv[1] == 'stat':
    print "pitch,roll,yaw,axelX,axelY,axelZ"
    for i in range(0, 5000):
        ( pitch, roll, yaw, axel_x, axel_y, axel_z) = imu_controller.read_pitch_roll_yaw_with_speeds()
        result = "%.2f %.2f %.2f %.2f %.2f %.2f" % (roll, pitch, yaw, axel_x, axel_y, axel_z)
        print result
else:
    (pitch, roll, yaw, axel_x, axel_y, axel_z) = imu_controller.read_pitch_roll_yaw_with_speeds()
    print "position:"
    print "   pitch = %.3f" % (pitch)
    print "   roll = %.3f" % (roll)
    print "   yaw = %.3f" % (yaw)
    print "====================================="

    print "angular speeds:"
    print "   x = %.3f" % (axel_x)
    print "   y = %.3f" % (axel_y)
    print "   z = %.3f" % (axel_z)
    print "====================================="

