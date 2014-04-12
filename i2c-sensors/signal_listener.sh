#!/bin/bash
export PYTHONPATH=`pwd`
export COPTER_CONTROL_FILE=/home/pi/Desktop/projects/copter/copter_control.csv
python ./bitify/python/copter/CopterSignalsListener.py 8888
