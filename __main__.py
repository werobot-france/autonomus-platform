from RobotPls import Robot
from sys import exit
from os import _exit
from math import pi

robot = Robot()

def main():
    robot.getPath(20, 10, 80, 140)  # startingrobotX, startingrobotY, targetX, tegetY

try:
    main()
except KeyboardInterrupt:
    robot.stopMotors()
    try:
        exit(0)
    except SystemExit:
        _exit(0)
