from time import sleep
from math import pi, atan2, sqrt
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines


class MyLine(lines.Line2D):

	def __init__(self, *args, **kwargs):
		# we'll update the position when the line data is set
		self.text = mtext.Text(0, 0, '')
		lines.Line2D.__init__(self, *args, **kwargs)

		# we can't access the label attr until *after* the line is
		# initiated
		self.text.set_text(self.get_label())

	def set_figure(self, figure):
		self.text.set_figure(figure)
		lines.Line2D.set_figure(self, figure)

	def set_transform(self, transform):
		# 2 pixel offset
		texttrans = transform + mtransforms.Affine2D().translate(2, 2)
		self.text.set_transform(texttrans)
		lines.Line2D.set_transform(self, transform)

	def set_data(self, x, y):
		if len(x):
			self.text.set_position((x[-1], y[-1]))

		lines.Line2D.set_data(self, x, y)

	def draw(self, renderer):
		# draw my label at the end of the line with 2 pixel offset
		lines.Line2D.draw(self, renderer)
		self.text.draw(renderer)


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


#	obstacles = [
#		[
#			[0, 0],
#			[0, 150]
#		],
#		[
#			[0, 0],
#			[150, 0]
#		],
#		[
#			[150, 0],
#			[150, 150]
#		],
#		[
#			[150, 150],
#			[0, 150]
#		],
#		[
#			[0, 40],
#			[110, 40]
#		],
#		[
#			[70, 40],
#			[70, 20]
#		],
#		[
#			[110, 40],
#			[110, 50]
#		],
#		[
#			[150, 100],
#			[110, 100]
#		],
#		[
#			[110, 70],
#			[110, 100]
#		],
#		[
#			[110, 70],
#			[70, 70]
#		],
#		[
#			[40, 90],
#			[90, 90]
#		],
#		[
#			[70, 100],
#			[70, 130]
#		],
#		[
#			[90, 50],
#			[90, 70]
#		]
#	]
	murs = obstacles  # modifiés pour prendre en compte l'épaisseur


def getP(p, i):
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


def simplified(pr, pt):
	r, t = [pr], [pt]

	while Robot.R not in r:
		print("R", r)
		r += [getP(r[-1], 'r')]

	while Robot.T not in [[getP(t[-1], 't')[0], getP(t[-1], 't')[1]]]:
		print("T", t)
		t += [getP(t[-1], 't')]

	r.reverse()
	fpath = r + t + [Robot.T]

	for f in fpath:
		can = True
		for p in fpath:
			if not intersectWall(p, f) and can and fpath[0] != f:
				fpath.remove(fpath[fpath.index(p)-1])
			else:
				can = False

	print('')
	print(
		'_________________________________________[PATH]_________________________________________')
	print(fpath)
	Robot.path = [Robot.R] + fpath + [Robot.T]
	display('Sismologie')
	return(fpath)


def display(title, stuck=False):
	fig, ax = plt.subplots()
	for o in Robot.obstacles:
		b = [[o[0][0], o[1][0]], [o[0][1], o[1][1]]]
		ax.add_line(MyLine(b[0], b[1]))

	for p in range(len(Robot.path)):
		if (Robot.path[p] != Robot.path[-1]):
			o = [Robot.path[p], Robot.path[p+1]]
		b = [[o[0][0], o[1][0]], [o[0][1], o[1][1]]]
		L = MyLine(b[0], b[1])
		L.set_color((1, 0, 0, 1))
		ax.add_line(L)

	if stuck:
		for p in Robot.rp:
			plt.plot([p[0]], [p[1]], 'bo')
		for p in Robot.tp:
			plt.plot([p[0]], [p[1]], 'ro')

	plt.plot([Robot.R[0]], [Robot.R[1]], 'bs')
	plt.plot([Robot.T[0]], [Robot.T[1]], 'rs')
	plt.axis([-5, 155, -5, 155])
	plt.annotate('T', xy=Robot.T)
	plt.annotate('expert', xy=Robot.R)
	fig.suptitle(title, fontsize=16, color=(1, 0, 0, 1))
	plt.show()


def displayP(title, R, T, p):
	fig, ax = plt.subplots()
	for o in Robot.obstacles:
		b = [[o[0][0], o[1][0]], [o[0][1], o[1][1]]]
		ax.add_line(MyLine(b[0], b[1]))

	for i in range(len(p)):
		if (p[i] != p[-1]):
			o = [p[i], p[i+1]]
		b = [[o[0][0], o[1][0]], [o[0][1], o[1][1]]]
		L = MyLine(b[0], b[1])
		L.set_color((1, 0, 0, 1))
		ax.add_line(L)

	plt.plot([R[0]], [R[1]], 'bs')
	plt.plot([T[0]], [T[1]], 'rs')
	plt.axis([-5, 155, -5, 155])
	plt.annotate('T', xy=T)
	plt.annotate('expert', xy=R)
	fig.suptitle(title, fontsize=16, color=(1, 0, 0, 1))
	plt.show()


def getPath(rX, rY, tX, tY, threehold=20, endOrientation=None):
	Robot.x = rX
	Robot.y = rY
	Robot.R = [Robot.x, Robot.y]
	Robot.T = [tX, tY]
	Robot.tp = [Robot.T]
	Robot.rp = [Robot.R]
	#display("pitit aperçu")

	gone = False

	while not gone:
		for pt in Robot.tp:
			for pr in Robot.rp:
				if not intersectWall(pt, pr):
					Robot.tp.reverse()
					Robot.path = Robot.rp
					Robot.path += Robot.tp
					return simplified(pr, pt)
		print('....')
		expandPaths()
		Robot.times += 1
		if Robot.times == Robot.step:
			display('g du mal...', True)
			Robot.times = 0


def expandPaths():
	pr = Robot.precision
	nrp, ntp = [], []
	nrp += Robot.rp
	ntp += Robot.tp
	for p in Robot.tp:
		up = [p[0], p[1]+pr, 1]
		ri = [p[0]+pr, p[1], 2]
		bo = [p[0], p[1]-pr, 3]
		le = [p[0]-pr, p[1], 4]
		if not intersectWall(up, p) and up not in Robot.tp and [up[0], up[1], 3] not in Robot.tp and [up[0], up[1], 4] not in Robot.tp and [up[0], up[1], 2] not in Robot.tp:
			can = True
			for a in ntp:
				if a == up:
					can = False
			if can:
				ntp += [up]
		if not intersectWall(ri, p) and ri not in Robot.tp and [ri[0], ri[1], 3] not in Robot.tp and [ri[0], ri[1], 4] not in Robot.tp and [ri[0], ri[1], 1] not in Robot.tp:
			can = True
			for a in ntp:
				if a == ri:
					can = False
			if can:
				ntp += [ri]
		if not intersectWall(bo, p) and bo not in Robot.tp and [bo[0], bo[1], 1] not in Robot.tp and [bo[0], bo[1], 4] not in Robot.tp and [bo[0], bo[1], 2] not in Robot.tp:
			can = True
			for a in ntp:
				if a == bo:
					can = False
			if can:
				ntp += [bo]
		if not intersectWall(le, p) and le not in Robot.tp and [le[0], le[1], 3] not in Robot.tp and [le[0], le[1], 1] not in Robot.tp and [le[0], le[1], 2] not in Robot.tp:
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
		if not intersectWall(up, p) and up not in Robot.rp and [up[0], up[1], 3] not in Robot.rp and [up[0], up[1], 4] not in Robot.rp and [up[0], up[1], 2] not in Robot.rp:
			can = True
			for a in nrp:
				if a == up:
					can = False
			if can:
				nrp += [up]
		if not intersectWall(ri, p) and ri not in Robot.rp and [ri[0], ri[1], 3] not in Robot.rp and [ri[0], ri[1], 4] not in Robot.rp and [ri[0], ri[1], 1] not in Robot.rp:
			can = True
			for a in nrp:
				if a == ri:
					can = False
			if can:
				nrp += [ri]
		if not intersectWall(bo, p) and bo not in Robot.rp and [bo[0], bo[1], 1] not in Robot.rp and [bo[0], bo[1], 4] not in Robot.rp and [bo[0], bo[1], 2] not in Robot.rp:
			can = True
			for a in nrp:
				if a == bo:
					can = False
			if can:
				nrp += [bo]
		if not intersectWall(le, p) and le not in Robot.rp and [le[0], le[1], 3] not in Robot.rp and [le[0], le[1], 1] not in Robot.rp and [le[0], le[1], 2] not in Robot.rp:
			can = True
			for a in nrp:
				if a == le:
					can = False
			if can:
				nrp += [le]
	Robot.tp, Robot.rp = ntp, nrp


def ccw(A, B, C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Retourne True si ça se croise


def intersect(A, B, C, D):
	return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def intersectWall(A, B):
	for mur in Robot.murs:
		if intersect(A, B, mur[0], mur[1]):
			return True
	return False


title = "lel"
p = []
R = [0, 0]
T = [0, 0]
if p == []:
	getPath(20, 10, 80, 140)  # startingrobotX, startingrobotY, targetX, tegetY
else:
	displayP(title, R, T, p)
