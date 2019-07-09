from Robot import Robot
from sys import exit
from os import _exit

robot = Robot()

# def main():
#     robot.goTo(0, 1000, 50)
#     print('end of goto')
#     robot.goTo(0, 0, 50)
#     print('stopped')
#     robot.stopThreads()

def main():
    robot.logState()
    
try:
    main()
except KeyboardInterrupt:
    print('Interrupted')
    robot.stopMotors()
    try:
        exit(0)
    except SystemExit:
        _exit(0)