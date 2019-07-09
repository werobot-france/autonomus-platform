from PositionWatcher import PositionWatcher
from adafruit_crickit import crickit
from math import pi, atan2, sqrt
from time import sleep

class Robot:
    leftMotor = crickit.dc_motor_1
    rightMotor = crickit.dc_motor_2
    positionWatcher = None
    x = 0
    y = 0
    theta = 0
    
    def __init__(self):
        self.positionWatcher = PositionWatcher()
        self.positionWatcher.start()
        
    def fetch(self):
        self.x = self.positionWatcher.getPos()[0]
        self.y = self.positionWatcher.getPos()[1]
        self.theta = self.positionWatcher.getOrientation()
    
    def goToOrientation(self, targetTheta):
        print('Go to Orientation!')
        seuilOrientation = pi/10
        running = True
        while running:
            self.fetch()
            deltaTheta = targetTheta - self.theta
            
            if abs(deltaTheta) > pi:
                deltaTheta = (2*pi - abs(deltaTheta)) * - deltaTheta / abs(deltaTheta)
                
            if abs(deltaTheta) > seuilOrientation:
                self.leftMotor.throttle = self.rightMotor.throttle = 0.5 * deltaTheta/abs(deltaTheta) +(0.2/pi/(deltaTheta))
            else:
                running = False
                
        self.stopMotors()
        
    def goTo(self, targetX, targetY, threehold = 20, endOrientation = None):
        print('go to launch')
        cruiseSpeed = 0.6
        
        x = self.positionWatcher.getPos()[0]
        y = self.positionWatcher.getPos()[1]
        
        self.goToOrientation(atan2((targetY - y), (targetX - x)))
        
        running = True
        
        while running:
            self.fetch()
            targetDistance = sqrt((targetX - self.x) ** 2 + (targetY - self.y) ** 2)
            targetTheta = atan2((targetY - self.y), (targetX - self.x))
            deltaTheta = targetTheta - self.theta
            
            if abs(deltaTheta) > pi:
                deltaTheta += 2*pi
            
            if abs(deltaTheta) < pi/2:
                pwm = (cruiseSpeed + (1-cruiseSpeed)*(deltaTheta/(pi / 2)))
                self.leftMotor.throttle = -pwm
                self.rightMotor.throttle = pwm
            else:
                self.goToOrientation(targetTheta)
                    
            if targetDistance < threehold:
                running = False

        self.stopMotors()
        
        if (endOrientation != None):
            print('endorientation')
            self.goToOrientation(endOrientation)
            
    def stopMotors(self):
        self.leftMotor.throttle = self.rightMotor.throttle = 0
                        
    def stopThreads(self):
        self.positionWatcher.stop()
        
    def logState(self):
        while True:
            self.fetch()
            print(self.x, self.y, self.theta * 180/pi)
            sleep(0.1)
        
