from Robot import Robot
from sys import exit
from os import _exit
from math import pi

robot = Robot()

def main():
    robot.goTo(-400, 0, 50)
    robot.goTo(-400, 500, 50)
    robot.goTo(400, 500, 50)
    robot.goTo(400, 1000, 50)
    robot.goTo(-200, 1000, 50)
    robot.goTo(-200, 1900, 50)
    robot.goTo(-200, 2000, 50)
    robot.goTo(30, 2000, 50, -90)
    print("WOW")
    robot.goTo(-200, 2000, 50, -90)
    robot.goTo(-300, 1900, 50)
    print("#-5")
    robot.goTo(-300, 1000, 50)
    print("#-4")
    robot.goTo(400, 1000, 50)
    print("#-3")
    robot.goTo(400, 500, 50)
    print("#-2")
    robot.goTo(-400, 500, 50)
    print("#-1")
    robot.goTo(-400, 0, 50)
    print("#-0")
    robot.goTo(0, 0, 50, 90)
    robot.goToOrientation(pi/2)
    print("LELEELLELELEL")
    print('stopped')
    robot.stopThreads()

#def main():
    #robot.logState()
    
try:
    main()
except KeyboardInterrupt:
    print('Interrupted')
    robot.stopMotors()
    try:
        exit(0)
    except SystemExit:
        _exit(0)
