#!/usr/bin/env python

import web  # web.py
import smbus

import bitify.python.sensors.imu as imu
from bitify.python.utils.i2cutils import i2c_raspberry_pi_bus_number

urls = (
    '/', 'index'
)

bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu_controller = imu.IMU(bus, 0x69, 0x53, 0x1e, "IMU")
imu_controller.set_compass_offsets(72, 72, -30)

app = web.application(urls, globals())

class index:
    def GET(self):
        (pitch, roll, yaw, ang_vel_x, ang_vel_y, ang_vel_z) = imu_controller.read_pitch_roll_yaw_with_speeds()
        result = "%.2f %.2f %.2f %.2f %.2f %.2f" % (pitch, roll, yaw,ang_vel_x, ang_vel_y, ang_vel_z)
        return result

if __name__ == "__main__":
    app.run()
