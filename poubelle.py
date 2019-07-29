
R = [x, y]
T = [tX, tY]
RT = [x, tY]
TR = [tX, y]

	#si on peut y aller en ligne droite, le faire
	if not self.intersectWall(R, T):
			self.go(tX, tY, threehold, endOrientation)
			gone = True

		if not gone:
			#si on peut en en deux fois, x puis y ou l'inverse
			if (not self.intersectWall(R, RT) and not self.intersectWall(RT, T)):
				self.go(x, tY, threehold, endOrientation)
				self.go(tX, tY, threehold, endOrientation)
				gone = True
			else:
				if (not self.intersectWall(R, TR) and not self.intersectWall(TR, T)):
					self.go(tX, y, threehold, endOrientation)
					self.go(tX, tY, threehold, endOrientation)
					gone = True

					cX, cY = c[3][0], c[3][1]
			# si l'abcisse du coin est comprise entre celles du robot et de target, ajouter un déplacement sur l'ordonnée
			if (cX > tX and cX < x) or (cX > x and cX < tX):
				dY = y + ((abs(cY - y) + margeR) * ((y-cY)/abs(y-cY)))
				for mur in self.murs:
					m1, m2 = mur[0], mur[1]
					if (not self.intersect(R, [x, y+dY], m1, m2)) and (not self.intersect([x, y+dY], [tX, y+dY], m1, m2)) and (not self.intersect([tX, y+dY], T, m1, m2)):
						self.go(x, y+dY, threehold, endOrientation)
						self.go(tX, y+dY, threehold, endOrientation)
						self.go(tX, tY, threehold, endOrientation)
						gone = True
			else:
				# si l'ordonnée du coin est comprise entre celles du robot et de target, ajouter un déplacement sur l'abcisse
				if (cY > tY and cY < y) or (cY > y and cY < tY):
					dX = x + ((abs(cX - x) + margeR) * ((x-cX)/abs(x-cX)))
					for mur in self.murs:
						m1, m2 = mur[0], mur[1]
						if (not self.intersect(R, [x+dX, y], m1, m2)) and (not self.intersect([x+dX, y], [x+dX, tY], m1, m2)) and (not self.intersect([x+dX, tY], T, m1, m2)):
							self.go(x+dX, y, threehold, endOrientation)
							self.go(x+dX, tY, threehold, endOrientation)
							self.go(tX, tY, threehold, endOrientation)
							gone = True

				tp.append([])
				rp.append([])

				for p in tp[-1]:
					if (not self.intersectWall(p, [p[0], p[1]+precision])):
						tp[-1].append([[p[0], p[1]+precision], p])
						tp[0].append([[p[0], p[1]+precision], p])
					if (not self.intersectWall(p, [p[0]+precision, p[1]])):
						tp[-1].append([[p[0]+precision, p[1]], p])
						tp[0].append([[p[0], p[1]+precision], p])
					if (not self.intersectWall(p, [p[0], p[1]-precision])):
						tp[-1].append([[p[0], p[1]-precision], p])
						tp[0].append([[p[0], p[1]+precision], p])
					if (not self.intersectWall(p, [p[0]-precision, p[1]])):
						tp[-1].append([[p[0]-precision, p[1]], p])
						tp[0].append([[p[0], p[1]+precision], p])

				for p in rp[-1]:
					if (not self.intersectWall(p, [p[0], p[1]+precision])):
						rp[-1].append([[p[0], p[1]+precision], p])
						rp[0].append([[p[0], p[1]+precision], p])
					if (not self.intersectWall(p, [p[0]+precision, p[1]])):
						rp[-1].append([[p[0]+precision, p[1]], p])
						rp[0].append([[p[0], p[1]+precision], p])
					if (not self.intersectWall(p, [p[0], p[1]-precision])):
						rp[-1].append([[p[0], p[1]-precision], p])
						rp[0].append([[p[0], p[1]+precision], p])
					if (not self.intersectWall(p, [p[0]-precision, p[1]])):
						rp[-1].append([[p[0]-precision, p[1]], p])
						rp[0].append([[p[0], p[1]+precision], p])

				path = []

				for pt in tp[0]:
					for pr in rp[0]:
						if (self.intersect(pr[0], pr[1], pt[0], pt[1])):
							for p in pr:
								path.append([[p[0][0], p[0][1]], p[1]])



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

	obstacles = [
		 [
			[300, 250], # premier point du mur
			[-200, 250], # deuxieme
			5  # epaisseur
		] 
	] 

	murs = obstacles # modifié pour prendre en compte l'épaisseur 

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
				self.leftMotor.throttle = self.rightMotor.throttle = 0.5 * deltaTheta/abs(deltaTheta) +(0.2/pi/(deltaTheta))
			else:
				running = False
				
		self.stopMotors()
	def go(self, targetX, targetY, threehold = 20, endOrientation = None):
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
	def goTo(self, tX, tY, threehold=20, endOrientation=None):
		x = self.positionWatcher.getPos()[0]
		y = self.positionWatcher.getPos()[1]
		R = [x, y]
		T = [tX, tY]
		gone = False
		
		tp = [[T]]
		rp = [[R]]
		precision = 1000
		path = []
		fpath = []

		while not gone:

			for ltp in tp:
				for lrp in rp:
					#print("lrp", lrp)
					#print("ltp", ltp)
					for mur in self.murs:
						if (not self.intersect(ltp[-1], lrp[-1], mur[0], mur[1])) and (not gone):
							for frp in rp:
								print("frp", frp)
								fpath.append(frp[0])
							for ftp in tp:
								print("ftp", ftp)
								fpath.append(ftp[0])
						print("fpath", fpath)
			if fpath != [] :
				npath = []
				i = 0
				for p in fpath:
					#print("p", p)
					if (p != fpath[-1]):
						for mur in self.murs:
							if not self.intersect(p, fpath[i], mur[0], mur[1]):
								npath.append(p)
					i++
				fpath = npath
				print("fpath", fpath)
				for p in fpath:
					print('go', p)
					self.go(p[0], p[1], threehold, endOrientation)
				gone = True

			if not gone:
				print('tp', tp)
				ntp = []
				nrp = []
				for p in tp:
					#print('p', p)
					for mur in self.murs:
						if (not self.intersect(p[-1], [p[-1][0], p[-1][1]+precision], mur[0], mur[1])):
							np = []
							for i in p:
								np.append(i)
							np.append([p[-1][0], p[-1][1]+precision])
							ntp.append(np)
						if (not self.intersect(p[-1], [p[-1][0]+precision, p[-1][1]], mur[0], mur[1])):
							np = []
							for i in p:
								np.append(i)
							np.append([p[-1][0]+precision, p[-1][1]])
							ntp.append(np)
						if (not self.intersect(p[-1], [p[-1][0], p[-1][1]-precision], mur[0], mur[1])):
							np = []
							for i in p:
								np.append(i)
							np.append([p[-1][0], p[-1][1]-precision])
							ntp.append(np)
						if (not self.intersect(p[-1], [p[-1][0]-precision, p[-1][1]], mur[0], mur[1])):
							np = []
							for i in p:
								np.append(i)
							np.append([p[-1][0]-precision, p[-1][1]])
							ntp.append(np)

				for p in rp:
					for mur in self.murs:
						if (not self.intersect(p[-1], [p[-1][0], p[-1][1]+precision], mur[0], mur[1])):
							np = []
							for i in p:
								np.append(i)
							np.append([p[-1][0], p[-1][1]+precision])
							nrp.append(np)
						if (not self.intersect(p[-1], [p[-1][0]+precision, p[-1][1]], mur[0], mur[1])):
							np = []
							for i in p:
								np.append(i)
							np.append([p[-1][0]+precision, p[-1][1]])
							nrp.append(np)
						if (not self.intersect(p[-1], [p[-1][0], p[-1][1]-precision], mur[0], mur[1])):
							np = []
							for i in p:
								np.append(i)
							np.append([p[-1][0], p[-1][1]-precision])
							nrp.append(np)
						if (not self.intersect(p[-1], [p[-1][0]-precision, p[-1][1]], mur[0], mur[1])):
							np = []
							for i in p:
								np.append(i)
							np.append([p[-1][0]-precision, p[-1][1]])
							nrp.append(np)
				print('nrp', nrp)
				print('ntp', ntp)
				rp, tp = nrp, ntp
						

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

