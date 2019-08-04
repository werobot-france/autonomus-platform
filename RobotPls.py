from time import sleep
from math import *


class Robot:
	x = 0
	y = 0
	R = [x, y]
	T = [0, 0]
	tp = [T]
	path = []
	rp = [R]
	precision = 16

	obstacles = [
		[
			[0, 0],
			[0, 150]
		],
		[
			[0, 0],
			[150, 0]
		],
		[
			[150, 0],
			[150, 150]
		],
		[
			[150, 150],
			[0, 150]
		],
		[
			[0, 40],
			[110, 40]
		],
		[
			[70, 40],
			[70, 20]
		],
		[
			[110, 40],
			[110, 50]
		],
		[
			[150, 100],
			[110, 100]
		],
		[
			[110, 70],
			[110, 100]
		],
		[
			[110, 70],
			[70, 70]
		],
		[
			[40, 90],
			[90, 90]
		],
		[
			[70, 100],
			[70, 130]
		],
		[
			[90, 50],
			[90, 70]
		]
	]


	murs = obstacles  # modifiés pour prendre en compte l'épaisseur


	def getP(self, p, i):
		pr = self.precision

		if p[2] == 1:
			a = [p[0], p[1]-pr, 1]
		elif p[2] == 2:
			a = [p[0]-pr, p[1], 2]
		elif p[2] == 3:
			a = [p[0], p[1]+pr, 3]
		elif p[2] == 4:
			a = [p[0]+pr, p[1], 4]

		if i == 'r':
			for r in self.rp:
				if [r[0], r[1]] == [a[0], a[1]]:
					return r

		if i == 't':
			for t in self.tp:
				if [t[0], t[1]] == [a[0], a[1]]:
					return t


	def simplified(self, pr, pt):
		r, t = [pr], [pt]

		while self.R not in r:
			print("R", r)
			r += [self.getP(r[-1], 'r')]

		while self.T not in [[self.getP(t[-1], 't')[0], self.getP(t[-1], 't')[1]]]:
			print("T", t)
			t += [self.getP(t[-1], 't')]

		r.reverse()
		fpath = r + t + [self.T]

		for f in fpath:
			can = True
			for p in fpath:
				if not self.intersectWall(p, f) and can and fpath[0] != f:
					fpath.remove(fpath[fpath.index(p)-1])
				else:
					can = False

		print('')
		print(
			'_________________________________________[PATH]_________________________________________')
		print(fpath)
		self.path = [self.R] + fpath + [self.T]
		return(fpath)



	def getPath(self, rX, rY, tX, tY, threehold=20, endOrientation=None):
		self.x = rX
		self.y = rY
		self.R = [self.x, self.y]
		self.T = [tX, tY]
		self.tp = [self.T]
		self.rp = [self.R]

		gone = False

		while not gone:
			for pt in self.tp:
				for pr in self.rp:
					if not self.intersectWall(pt, pr):
						self.tp.reverse()
						self.path = self.rp
						self.path += self.tp
						return self.simplified(pr, pt)
			print('....')
			self.expandPaths()


	def expandPaths(self):
		pr = self.precision
		nrp, ntp = [], []
		nrp += self.rp
		ntp += self.tp
		for p in self.tp:
			up = [p[0], p[1]+pr, 1]
			ri = [p[0]+pr, p[1], 2]
			bo = [p[0], p[1]-pr, 3]
			le = [p[0]-pr, p[1], 4]
			if not self.intersectWall(up, p) and up not in self.tp and [up[0], up[1], 3] not in self.tp and [up[0], up[1], 4] not in self.tp and [up[0], up[1], 2] not in self.tp:
				can = True
				for a in ntp:
					if a == up:
						can = False
				if can:
					ntp += [up]
			if not self.intersectWall(ri, p) and ri not in self.tp and [ri[0], ri[1], 3] not in self.tp and [ri[0], ri[1], 4] not in self.tp and [ri[0], ri[1], 1] not in self.tp:
				can = True
				for a in ntp:
					if a == ri:
						can = False
				if can:
					ntp += [ri]
			if not self.intersectWall(bo, p) and bo not in self.tp and [bo[0], bo[1], 1] not in self.tp and [bo[0], bo[1], 4] not in self.tp and [bo[0], bo[1], 2] not in self.tp:
				can = True
				for a in ntp:
					if a == bo:
						can = False
				if can:
					ntp += [bo]
			if not self.intersectWall(le, p) and le not in self.tp and [le[0], le[1], 3] not in self.tp and [le[0], le[1], 1] not in self.tp and [le[0], le[1], 2] not in self.tp:
				can = True
				for a in ntp:
					if a == le:
						can = False
				if can:
					ntp += [le]

		for p in self.rp:
			up = [p[0], p[1]+pr, 1]
			ri = [p[0]+pr, p[1], 2]
			bo = [p[0], p[1]-pr, 3]
			le = [p[0]-pr, p[1], 4]
			if not self.intersectWall(up, p) and up not in self.rp and [up[0], up[1], 3] not in self.rp and [up[0], up[1], 4] not in self.rp and [up[0], up[1], 2] not in self.rp:
				can = True
				for a in nrp:
					if a == up:
						can = False
				if can:
					nrp += [up]
			if not self.intersectWall(ri, p) and ri not in self.rp and [ri[0], ri[1], 3] not in self.rp and [ri[0], ri[1], 4] not in self.rp and [ri[0], ri[1], 1] not in self.rp:
				can = True
				for a in nrp:
					if a == ri:
						can = False
				if can:
					nrp += [ri]
			if not self.intersectWall(bo, p) and bo not in self.rp and [bo[0], bo[1], 1] not in self.rp and [bo[0], bo[1], 4] not in self.rp and [bo[0], bo[1], 2] not in self.rp:
				can = True
				for a in nrp:
					if a == bo:
						can = False
				if can:
					nrp += [bo]
			if not self.intersectWall(le, p) and le not in self.rp and [le[0], le[1], 3] not in self.rp and [le[0], le[1], 1] not in self.rp and [le[0], le[1], 2] not in self.rp:
				can = True
				for a in nrp:
					if a == le:
						can = False
				if can:
					nrp += [le]
		self.tp, self.rp = ntp, nrp


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

