# !/usr/bin/python

__author__ = 'ivanbahdanau'
import csv
import os



def read_file_data():
    global copter_is_on, copter_torque, is_kill, control_force, z_axe_control
    copterControlFile = os.environ.get('COPTER_CONTROL_FILE')
    with open(copterControlFile, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            copter_is_on = row[0] == 'True'
            copter_torque = int(row[1])
            is_kill = row[2] == 'True'
            control_force = row[3]
            z_axe_control = row[4]
    return (copter_is_on, copter_torque, is_kill, int(control_force), float(z_axe_control))


def write_file_data(copter_is_on, copter_torque, is_kill, control_force,z_axe_control):
    with open(os.environ.get('COPTER_CONTROL_FILE'), 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([str(copter_is_on), str(copter_torque), str(is_kill), str(control_force),str(z_axe_control)])

