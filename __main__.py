from Robot import Robot
from sys import exit
from os import _exit
from math import pi

robot = Robot()

def main():
    robot.goTo(0, 500, 20)

try:
    main()
except KeyboardInterrupt:
    robot.stopMotors()
    try:
        exit(0)
    except SystemExit:
        _exit(0)


[
[1.5623140860223153e-05, 0.04270833047578166], 
[120.00001562314085, 0.04270833047578166], 
[240.00001562314085, 0.04270833047578166], 
[240, 500], 
[120, 500],
[1.5623140860223153e-05, 0.04270833047578166], 
[-119.99998437685915, 0.04270833047578166], 
[-239.99998437685915, 0.04270833047578166], 
[-240, 500], 
[-120, 500], 
[0, 500]
]
