from Robot import *
from sys import exit
from os import _exit
from math import pi

robot = Robot()
path = PathGetter()

def main():
    robot.goToPath(path.getPath(600, 1300))  # startingrobotX, startingrobotY, targetX, tegetY


try:
    main()
except KeyboardInterrupt:
    robot.stopMotors()
    try:
        exit(0)
    except SystemExit:
        _exit(0)
