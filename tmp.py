
from gpiozero import DigitalInputDevice

from threading import Thread
from time import sleep

from math import *

from adafruit_crickit import crickit

import sys
import os
def toDeg(x):
    return x * 180/pi

def toRad(x):
    return x / 180/pi

def toFixed(input, n):
    input = str(input).split('.')
    while len(input[1]) != n:
        if len(input[1]) < n:
            input[1] += "0"
        else:
            input[1] = input[1][:-1]
    return input[0] + '.' + input[1]


class TicksWatcher:
    ticks = (0, 0)

    # GPIO pin BCM 23 & 24 Both pulled up
    # gauche=14,15

    # droit=17,27

    phaseA = DigitalInputDevice(14, True)
    phaseB = DigitalInputDevice(15, True)

    phaseC = DigitalInputDevice(17, True)
    phaseD = DigitalInputDevice(27, True)

    counts = 0
    countsP = 0
    state = (0, 0)
    oldState = (0, 0)
    stateP = (0, 0)
    oldStateP = (0, 0)

    thread = None

    def readTicks(self):
        while True:
            fetchedState = (self.phaseA.value, self.phaseB.value)
            fetchedStateP = (self.phaseC.value, self.phaseD.value)
            if fetchedState != self.state:
                self.state = fetchedState

                if (self.state[0], self.oldState[1]) == (1, 0) or (self.state[0], self.oldState[1]) == (0, 1):
                    self.counts += 1

                elif (self.state[0], self.oldState[1]) == (1, 1) or (self.state[0], self.oldState[1]) == (0, 0):
                    self.counts -= 1

                self.oldState = self.state

            if fetchedStateP != self.stateP:
                self.stateP = fetchedStateP

                if (self.stateP[0], self.oldStateP[1]) == (1, 0) or (self.stateP[0], self.oldStateP[1]) == (0, 1):
                    self.countsP += 1

                elif (self.stateP[0], self.oldStateP[1]) == (1, 1) or (self.stateP[0], self.oldStateP[1]) == (0, 0):
                    self.countsP -= 1

                self.oldStateP = self.stateP

    def start(self):
        self.thread = Thread(target=self.readTicks)
        self.thread.start()

    def getValues(self):
        # gauche, droite
        return (self.counts, self.countsP)


class PositionWatcher:
    oldTicks = (0, 0)
    perimeter = 205
    axialDistance = 233.5
    theta = pi / 2
    x = 0
    y = 0
    tickWatcher = TicksWatcher()

    def watchPosition(self):
        while True:
            newTicks = self.tickWatcher.getValues()
            deltaTicks = (newTicks[0] - self.oldTicks[0],
                          newTicks[1] - self.oldTicks[1])
            self.oldTicks = newTicks
            leftDistance = deltaTicks[0] / 2400 * self.perimeter
            rightDistance = deltaTicks[1] / 2400 * self.perimeter
            t1 = (leftDistance + rightDistance) / 2
            alpha = (rightDistance - leftDistance) / self.axialDistance
            self.theta = self.theta + alpha
            self.x = self.x + t1 * cos(self.theta)
            self.y = self.y + t1 * sin(self.theta)
            # print((x - 95 * cos(theta), y - 95 * sin(theta)), theta * 180/pi)
            sleep(0.01)

    def start(self):
        self.tickWatcher.start()
        self.thread = Thread(target=self.watchPosition)
        self.thread.start()

    def getPos(self):
        return (self.x, self.y)

    def getOrientation(self):
        return (self.theta)


positionWatcher = PositionWatcher()
positionWatcher.start()

leftMotor = crickit.dc_motor_1
rightMotor = crickit.dc_motor_2

seuil = 30
pwmMin = 0.35

def pwm(targetTheta, theta, speed):
    global pwmMin
    return (1/speed - pwmMin) / (2*pi) * (targetTheta - theta) + 1

# def goTo(targetX, targetY):
#     x = positionWatcher.getPos()[0]
#     y = positionWatcher.getPos()[1]
#     theta = positionWatcher.getOrientation()
#     targetDistance = sqrt((targetX - x) ** 2 + (targetY - y) ** 2)
#     targetTheta = atan2((targetY - y), (targetX - x))
#     leftSpeed = rightSpeed = 0
#     while targetDistance > seuil:
#         print(targetDistance, targetTheta - theta, leftSpeed, rightSpeed)
#         speed = ((1 + pwmMin) / 2)
#         leftSpeed = speed * pwm(targetTheta, theta, speed)
#         rightSpeed = speed * -pwm(targetTheta, theta, speed)       
#         leftMotor.throttle = -leftSpeed
#         rightMotor.throttle = -rightSpeed
        
#         x = positionWatcher.getPos()[0]
#         y = positionWatcher.getPos()[1]
#         theta = positionWatcher.getOrientation()
#         targetDistance = sqrt((targetX - x) ** 2 + (targetY - y) ** 2)
#         targetTheta = atan2((targetY - y), (targetX - x))
#     leftMotor.throttle = 0
#     rightMotor.throttle = 0

# def goToOrientation(targetOrientation):
#     running = True
#     seuilOrientation = pi/12
#     cruiseSpeedOrientation = 0.5
#     while running:
#         theta = positionWatcher.getOrientation()
#         print(theta / pi/180)
#         deltaTheta = targetOrientation - theta
        
#         leftPwm = -((deltaTheta / abs(deltaTheta)) * cruiseSpeedOrientation)
#         rightPwm = -((deltaTheta / abs(deltaTheta)) * cruiseSpeedOrientation)
#         leftMotor.throttle = leftPwm
#         rightMotor.throttle = rightPwm

#         if deltaTheta < seuilOrientation: 
#             running = False
    
#     leftMotor.throttle = 0
#     rightMotor.throttle = 0
    
def goToOrientation(targetTheta):
    seuilOrientation = pi/10
    running = True
    while running:
        theta = positionWatcher.getOrientation()
        deltaTheta = targetTheta - theta
        
        if abs(deltaTheta) > pi:
            # autre sens
            var = deltaTheta / abs(deltaTheta)
            deltaTheta = (2*pi - abs(deltaTheta)) * -var    
            
        if abs(deltaTheta) > seuilOrientation:
            leftPwm = 0.5 * deltaTheta/abs(deltaTheta) +(0.2/pi/(deltaTheta))
            rightPwm = 0.5 * deltaTheta/abs(deltaTheta) +(0.2/pi/(deltaTheta))
            leftMotor.throttle = leftPwm
            rightMotor.throttle = rightPwm
        else:
            running = False
            
    leftMotor.throttle = 0
    rightMotor.throttle = 0

def goTo(targetX, targetY, seuil = 30, endOrientation = None):
    cruiseSpeed = 0.6
    
    # orienter le robot dans la bonne position    
    x = positionWatcher.getPos()[0]
    y = positionWatcher.getPos()[1]
    
    goToOrientation(atan2((targetY - y), (targetX - x)))
    print('orientation fin')
    running = True
    
    while running:        
        x = positionWatcher.getPos()[0]
        y = positionWatcher.getPos()[1]
        theta = positionWatcher.getOrientation()
        targetDistance = sqrt((targetX - x) ** 2 + (targetY - y) ** 2)
        targetTheta = atan2((targetY - y), (targetX - x))
        deltaTheta = targetTheta - theta
        print(toDeg(deltaTheta))
        
        if abs(deltaTheta) > pi:
            deltaTheta += 2*pi
        
        if abs(deltaTheta) < pi/2:
            leftPwm =-(cruiseSpeed - (1-cruiseSpeed)*(deltaTheta/(pi / 2)))
            rightPwm =(cruiseSpeed + (1-cruiseSpeed)*(deltaTheta/(pi / 2)))
            leftMotor.throttle = leftPwm
            rightMotor.throttle = rightPwm
        else:
            goToOrientation(atan2((targetY - y), (targetX - x)))
                
        if targetDistance < seuil:
            running = False

    leftMotor.throttle = 0
    rightMotor.throttle = 0
    
    if (endOrientation != None):
        goToOrientation(toRad(endOrientation))
    
def main():
    goTo(1000, 0, 50)
    # goTo(-400, 0, 50)
    # goTo(-400, 500, 50)
    # goTo(400, 500, 50)
    # goTo(400, 1000, 50)
    # goTo(-200, 1000, 50)
    # goTo(-200, 1900, 50)
    # goTo(-200, 2000, 50)
    # goTo(30, 2000, 50, -90)
    # print("WOW")
    # goTo(-200, 2000, 50, -90)
    # goTo(-300, 1900, 50)
    # print("#-5")
    # goTo(-300, 1000, 50)
    # print("#-4")
    # goTo(400, 1000, 50)
    # print("#-3")
    # goTo(400, 500, 50)
    # print("#-2")
    # goTo(-400, 500, 50)
    # print("#-1")
    # goTo(-400, 0, 50)
    # print("#-0")
    # goTo(0, 0, 50, 90)
    # goToOrientation(pi/2)
    # print("LELEELLELELEL")
    
    #goTo(0, 400, 70)
    # goTo(0, 700, 40)
    # goTo(-500, 700, 40)
    # goTo(600, 800, 50)
    #print(positionWatcher.getOrientation() / pi/180)
    
try:
    main()
except KeyboardInterrupt:
    print('Interrupted')    
    leftMotor.throttle = 0
    rightMotor.throttle = 0
    goTo(0, 0, 70)
    goToOrientation(pi/2)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
    

