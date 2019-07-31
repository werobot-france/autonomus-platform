from PositionWatcher import PositionWatcher
from adafruit_crickit import crickit
from math import pi, atan2, sqrt
from time import sleep
import matplotlib.pyplot as plt

class Robot:
	leftMotor = crickit.dc_motor_1
	rightMotor = crickit.dc_motor_2
	positionWatcher = None
	x = 0
	y = 0
	theta = 0
	precision = 350
	path = []
	R = []
	T = []
	tp = [[T]]
	rp = [[R]]

	obstacles = [
		[
			[-200, 100],
			[200, 100]
		],
		[
			[-200, 100],
			[-200, -200]
		],
		[
			[200, 100],
			[200, -200]
		]
	]
		
	fig, ax = plt.subplots()
	for o in obstacles:
		b = [[o[0][0], o[1][0], [o[0][0], o[1][0]]
		print(o)
		ax.add_line(MyLine(o[0], o[1]))

plt.show()

	murs = obstacles  # modifiés pour prendre en compte l'épaisseur

	def __init__(self):
		self.positionWatcher = PositionWatcher()
		self.positionWatcher.start()

	def fetch(self):
		self.x = self.positionWatcher.getPos()[0]
		self.y = self.positionWatcher.getPos()[1]
		self.theta = self.positionWatcher.getOrientation()

	def goToOrientation(self, targetTheta):
		seuilOrientation = pi/10
		running = True
		while running:
			self.fetch()
			deltaTheta = targetTheta - self.theta

			if abs(deltaTheta) > pi:
				deltaTheta = (2*pi - abs(deltaTheta)) * - deltaTheta / abs(deltaTheta)

			if abs(deltaTheta) > seuilOrientation:
				self.leftMotor.throttle = self.rightMotor.throttle = 0.5 * \
					deltaTheta/abs(deltaTheta) + (0.2/pi/(deltaTheta))
			else:
				running = False

		self.stopMotors()

	def goTo(self, targetX, targetY, threehold=20, endOrientation=None):
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
				pwm = (1-cruiseSpeed)*(deltaTheta/(pi / 2))
				self.leftMotor.throttle = -(cruiseSpeed - pwm)
				self.rightMotor.throttle = cruiseSpeed + pwm
			else:
				self.goToOrientation(targetTheta)

			if targetDistance < threehold:
				running = False

		self.stopMotors()

		if (endOrientation != None):
			self.goToOrientation(endOrientation)

	def simplified(self, path):
		return(path)

	def getPath(self, tX, tY, threehold=20, endOrientation=None):
		x = self.positionWatcher.getPos()[0]
		y = self.positionWatcher.getPos()[1]
		self.R = [x, y]
		self.T = [tX, tY]
		self.tp = [[self.T]]
		self.rp = [[self.R]]

		gone = False

		while not gone:
			for pt in self.tp:
				for pr in self.rp:
					print('TP', self.tp)
					print('RP', self.rp)
					if not self.intersectWall(pt[-1], pr[-1]):
						pt.reverse()
						self.path = pr
						self.path += pt
						return self.simplified(self.path)
			self.expandPaths()

	def expandPaths(self):
		ntp = []
		nrp = []
		pr = self.precision
		for p in self.tp:
			up = [p[-1][0], (p[-1][1])+pr]
			ri = [(p[-1][0])+pr, p[-1][1]]
			bo = [p[-1][0], (p[-1][1])-pr]
			le = [(p[-1][0])-pr, p[-1][1]]
			if not self.intersectWall(up, p[-1]):
				np = []
				for i in p:
					np.append(i)
				np.append(up)
				ntp += [np]
			if not self.intersectWall(ri, p[-1]):
				np = []
				for i in p:
					np.append(i)
				np.append(ri)
				ntp += [np]
			if not self.intersectWall(bo, p[-1]):
				np = []
				for i in p:
					np.append(i)
				np.append(bo)
				ntp += [np]
			if not self.intersectWall(le, p[-1]):
				np = []
				for i in p:
					np.append(i)
				np.append(le)
				ntp += [np]

			print('NTP', ntp)
		for p in self.rp:
			up = [p[-1][0], (p[-1][1])+pr]
			ri = [(p[-1][0])+pr, p[-1][1]]
			bo = [p[-1][0], (p[-1][1])-pr]
			le = [(p[-1][0])-pr, p[-1][1]]
			if not self.intersectWall(up, p[-1]):
				np = []
				for i in p:
					np.append(i)
				np.append(up)
				nrp += [np]
			if not self.intersectWall(ri, p[-1]):
				np = []
				for i in p:
					np.append(i)
				np.append(ri)
				nrp += [np]
			if not self.intersectWall(bo, p[-1]):
				np = []
				for i in p:
					np.append(i)
				np.append(bo)
				nrp += [np]
			if not self.intersectWall(le, p[-1]):
				np = []
				for i in p:
					np.append(i)
				np.append(le)
				nrp += [np]
			
			print('NRP', nrp)
		self.rp, self.tp = nrp, ntp
			

	def ccw(self, A, B, C):
		return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

	# Retourne True si ça se croise
	def intersect(self, A, B, C, D):
		return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

	def intersectWall(self, A, B):
		for mur in self.murs:
			if self.intersect(A, B, mur[0], mur[1]):
				return True
		return False

	def stopMotors(self):
		self.leftMotor.throttle = self.rightMotor.throttle = 0

	def stopThreads(self):
		self.positionWatcher.stop()

	def logState(self):
		while True:
			self.fetch()
			print(self.x, self.y, self.theta * 180/pi)
			sleep(0.1)
