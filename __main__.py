from Robot import Robot
from sys import exit
from os import _exit
from math import pi

robot = Robot()

def main():
    print('PATH', robot.getPath(-100, 800, 20))

try:
    main()
except KeyboardInterrupt:
    robot.stopMotors()
    try:
        exit(0)
    except SystemExit:
        _exit(0)
