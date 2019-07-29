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
	precision = 300
	path = []
	R = []
	T = []
	tp = [[T]]
	rp = [[R]]

	obstacles = [
		[
			[-300, 300],
			[300, 300]
		]
	]

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
					gone = True
					for mur in self.murs:
						print('mur', mur)
						print('pt', pt)
						print('pr', pr)
						if gone:
							if self.intersect(pt[-1], pr[-1], mur[0], mur[1]):
								gone = False
								print('CAAAAAAN_____________________________________________________________________________________')
							else:
								print('CANANANANANNANANANANANAANANNANANNANANNANANNANANNANANANANANNA')
			if gone:
				pt.reverse()
				self.path = pr
				self.path += pt
				return self.simplified(self.path)
			self.expandPaths()

	def expandPaths(self):
		ntp = []
		nrp = []
		for p in self.tp:
			print('p', p)
			for mur in self.murs:
				if (not self.intersect(p[-1], [p[-1][0], p[-1][1]+self.precision], mur[0], mur[1])):
					np = []
					for i in p:
						np.append(i)
					np.append([p[-1][0], p[-1][1]+self.precision])
					ntp.append(np)
				if (not self.intersect(p[-1], [p[-1][0]+self.precision, p[-1][1]], mur[0], mur[1])):
					np = []
					for i in p:
						np.append(i)
					np.append([p[-1][0]+self.precision, p[-1][1]])
					ntp.append(np)
				if (not self.intersect(p[-1], [p[-1][0], p[-1][1]-self.precision], mur[0], mur[1])):
					np = []
					for i in p:
						np.append(i)
					np.append([p[-1][0], p[-1][1]-self.precision])
					ntp.append(np)
				if (not self.intersect(p[-1], [p[-1][0]-self.precision, p[-1][1]], mur[0], mur[1])):
					np = []
					for i in p:
						np.append(i)
					np.append([p[-1][0]-self.precision, p[-1][1]])
					ntp.append(np)
		for p in self.rp:
			for mur in self.murs:
				if (not self.intersect(p[-1], [p[-1][0], p[-1][1]+self.precision], mur[0], mur[1])):
					np = []
					for i in p:
						np.append(i)
					np.append([p[-1][0], p[-1][1]+self.precision])
					nrp.append(np)
				if (not self.intersect(p[-1], [p[-1][0]+self.precision, p[-1][1]], mur[0], mur[1])):
					np = []
					for i in p:
						np.append(i)
					np.append([p[-1][0]+self.precision, p[-1][1]])
					nrp.append(np)
				if (not self.intersect(p[-1], [p[-1][0], p[-1][1]-self.precision], mur[0], mur[1])):
					np = []
					for i in p:
						np.append(i)
					np.append([p[-1][0], p[-1][1]-self.precision])
					nrp.append(np)
				if (not self.intersect(p[-1], [p[-1][0]-self.precision, p[-1][1]], mur[0], mur[1])):
					np = []
					for i in p:
						np.append(i)
					np.append([p[-1][0]-self.precision, p[-1][1]])
					nrp.append(np)
		self.rp, self.tp = nrp, ntp

	def ccw(self, A, B, C):
		return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

	# Return true si ça se croise
	def intersect(self, A, B, C, D):
		return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

	def stopMotors(self):
		self.leftMotor.throttle = self.rightMotor.throttle = 0

	def stopThreads(self):
		self.positionWatcher.stop()

	def logState(self):
		while True:
			self.fetch()
			print(self.x, self.y, self.theta * 180/pi)
			sleep(0.1)
