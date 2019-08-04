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

	times = 0
	step = 10
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

class PathGetter:
	def getP(self, p, i):
		pr = Robot.precision

		if p[2] == 1:
			a = [p[0], p[1]-pr, 1]
		elif p[2] == 2:
			a = [p[0]-pr, p[1], 2]
		elif p[2] == 3:
			a = [p[0], p[1]+pr, 3]
		elif p[2] == 4:
			a = [p[0]+pr, p[1], 4]

		if i == 'r':
			for r in Robot.rp:
				if [r[0], r[1]] == [a[0], a[1]]:
					return r

		if i == 't':
			for t in Robot.tp:
				if [t[0], t[1]] == [a[0], a[1]]:
					return t


	def simplified(self, pr, pt):
		r, t = [pr], [pt]

		while Robot.R not in r:
			print("R", r)
			r += [self.getP(r[-1], 'r')]

		while Robot.T not in [[self.getP(t[-1], 't')[0], self.getP(t[-1], 't')[1]]]:
			print("T", t)
			t += [self.getP(t[-1], 't')]

		r.reverse()
		fpath = r + t + [Robot.T]

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
		Robot.path = [Robot.R] + fpath + [Robot.T]
		return(fpath)

	def getPath(self, rX, rY, tX, tY, threehold=20, endOrientation=None):
		Robot.x = rX
		Robot.y = rY
		Robot.R = [Robot.x, Robot.y]
		Robot.T = [tX, tY]
		Robot.tp = [Robot.T]
		Robot.rp = [Robot.R]
		#self.display("pitit aperçu")

		gone = False

		while not gone:
			for pt in Robot.tp:
				for pr in Robot.rp:
					if not PathGetter.intersectWall(0, pt, pr):
						Robot.tp.reverse()
						Robot.path = Robot.rp
						Robot.path += Robot.tp
						return PathGetter.simplified(0, pr, pt)
			print('....')
			self.expandPaths()


	def expandPaths(self):
		pr = Robot.precision
		nrp, ntp = [], []
		nrp += Robot.rp
		ntp += Robot.tp
		for p in Robot.tp:
			up = [p[0], p[1]+pr, 1]
			ri = [p[0]+pr, p[1], 2]
			bo = [p[0], p[1]-pr, 3]
			le = [p[0]-pr, p[1], 4]
			if not self.intersectWall(up, p) and up not in Robot.tp and [up[0], up[1], 3] not in Robot.tp and [up[0], up[1], 4] not in Robot.tp and [up[0], up[1], 2] not in Robot.tp:
				can = True
				for a in ntp:
					if a == up:
						can = False
				if can:
					ntp += [up]
			if not self.intersectWall(ri, p) and ri not in Robot.tp and [ri[0], ri[1], 3] not in Robot.tp and [ri[0], ri[1], 4] not in Robot.tp and [ri[0], ri[1], 1] not in Robot.tp:
				can = True
				for a in ntp:
					if a == ri:
						can = False
				if can:
					ntp += [ri]
			if not self.intersectWall(bo, p) and bo not in Robot.tp and [bo[0], bo[1], 1] not in Robot.tp and [bo[0], bo[1], 4] not in Robot.tp and [bo[0], bo[1], 2] not in Robot.tp:
				can = True
				for a in ntp:
					if a == bo:
						can = False
				if can:
					ntp += [bo]
			if not self.intersectWall(le, p) and le not in Robot.tp and [le[0], le[1], 3] not in Robot.tp and [le[0], le[1], 1] not in Robot.tp and [le[0], le[1], 2] not in Robot.tp:
				can = True
				for a in ntp:
					if a == le:
						can = False
				if can:
					ntp += [le]

		for p in Robot.rp:
			up = [p[0], p[1]+pr, 1]
			ri = [p[0]+pr, p[1], 2]
			bo = [p[0], p[1]-pr, 3]
			le = [p[0]-pr, p[1], 4]
			if not self.intersectWall(up, p) and up not in Robot.rp and [up[0], up[1], 3] not in Robot.rp and [up[0], up[1], 4] not in Robot.rp and [up[0], up[1], 2] not in Robot.rp:
				can = True
				for a in nrp:
					if a == up:
						can = False
				if can:
					nrp += [up]
			if not self.intersectWall(ri, p) and ri not in Robot.rp and [ri[0], ri[1], 3] not in Robot.rp and [ri[0], ri[1], 4] not in Robot.rp and [ri[0], ri[1], 1] not in Robot.rp:
				can = True
				for a in nrp:
					if a == ri:
						can = False
				if can:
					nrp += [ri]
			if not self.intersectWall(bo, p) and bo not in Robot.rp and [bo[0], bo[1], 1] not in Robot.rp and [bo[0], bo[1], 4] not in Robot.rp and [bo[0], bo[1], 2] not in Robot.rp:
				can = True
				for a in nrp:
					if a == bo:
						can = False
				if can:
					nrp += [bo]
			if not self.intersectWall(le, p) and le not in Robot.rp and [le[0], le[1], 3] not in Robot.rp and [le[0], le[1], 1] not in Robot.rp and [le[0], le[1], 2] not in Robot.rp:
				can = True
				for a in nrp:
					if a == le:
						can = False
				if can:
					nrp += [le]
		Robot.tp, Robot.rp = ntp, nrp


	def ccw(self, A, B, C):
		return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

	# Retourne True si ça se croise


	def intersect(self, A, B, C, D):
		return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)


	def intersectWall(self, A, B):
		for mur in Robot.murs:
			if self.intersect(A, B, mur[0], mur[1]):
				return True
		return False
