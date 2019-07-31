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

	def set_axes(self, axes):
		self.text.set_axes(axes)
		lines.Line2D.set_axes(self, axes)

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
	tp = [[T]]
	path = []
	rp = [[R]]
	precision = 140

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
		],
		[
			[300, 900],
			[300, 700]
		],
		[
			[300, 700],
			[100, 700]
		],
		[
			[100, 700],
			[100, 300]
		],
		[
			[100, 300],
			[0, 300]
		],
		[
			[0, 300],
			[0, 600]
		],
		[
			[0, 600],
			[-100, 600]
		],
		[
			[-100, 600],
			[-100, 500]
		],
		[
			[-100, 500],
			[-700, 500]
		],
		[
			[-200, 500],
			[-200, 900]
		],
		[
			[-200, 900],
			[0, 900]
		],
		[
			[-700, 1300],
			[700, 1300]
		],
		[
			[700, 1300],
			[700, -500]
		],
		[
			[-700, -500],
			[700, -500]
		],
		[
			[-700, -500],
			[-700, 1300]
		]
	]
	murs = obstacles  # modifiés pour prendre en compte l'épaisseur


def simplified():
	simple = False
	fpath = Robot.path
	while not simple:
		can = True
		for p in fpath:
			if len(fpath) > 1:
				if p != fpath[-1] and p != fpath[-2] and p != fpath[-3]:
					if not intersectWall(p, fpath[fpath.index(p)+2]):
						fpath.remove(fpath[fpath.index(p)+1])
						can = False
		simple = can
	Robot.path = fpath
	print('PATH', fpath)
	display('Sismologie')
	return(fpath)


def display(title):
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

	plt.plot([Robot.R[0], Robot.T[0]], [Robot.R[1], Robot.T[1]], 'ro')
	plt.axis([-710, 710, -510, 1310])
	plt.annotate('Endroit où les bg vont', xy=Robot.T)
	plt.annotate('Gros BG', xy=Robot.R)
	fig.suptitle(title, fontsize=16, color=(1, 0, 0, 1))
	plt.show()


def getPath(rX, rY, tX, tY, threehold=20, endOrientation=None):
	Robot.x = rX
	Robot.y = rY
	Robot.R = [Robot.x, Robot.y]
	Robot.T = [tX, tY]
	Robot.tp = [[Robot.T]]
	Robot.rp = [[Robot.R]]

	display("pitit aperçu")

	gone = False

	while not gone:
		for pt in Robot.tp:
			for pr in Robot.rp:
				if not intersectWall(pt[-1], pr[-1]):
					pt.reverse()
					Robot.path = pr
					Robot.path += pt
					a = 0
					can = True
					for p in Robot.path:
						if len(p) > 2:
							if (p[a] != p[-1] and p[a] != p[-2]):
								if intersectWall(p[a], p[a+1]):
									can = False
							a += 1
					if can:
						return simplified()
		expandPaths()


def expandPaths():
	ntp = []
	nrp = []
	pr = Robot.precision
	for p in Robot.tp:
		up = [p[-1][0], (p[-1][1])+pr]
		ri = [(p[-1][0])+pr, p[-1][1]]
		bo = [p[-1][0], (p[-1][1])-pr]
		le = [(p[-1][0])-pr, p[-1][1]]
		if not intersectWall(up, p[-1]):
			np = []
			for i in p:
				np.append(i)
			np.append(up)
			ntp += [np]
		if not intersectWall(ri, p[-1]):
			np = []
			for i in p:
				np.append(i)
			np.append(ri)
			ntp += [np]
		if not intersectWall(bo, p[-1]):
			np = []
			for i in p:
				np.append(i)
			np.append(bo)
			ntp += [np]
		if not intersectWall(le, p[-1]):
			np = []
			for i in p:
				np.append(i)
			np.append(le)
			ntp += [np]

		print('NTP', ntp)
	for p in Robot.rp:
		up = [p[-1][0], (p[-1][1])+pr]
		ri = [(p[-1][0])+pr, p[-1][1]]
		bo = [p[-1][0], (p[-1][1])-pr]
		le = [(p[-1][0])-pr, p[-1][1]]
		if not intersectWall(up, p[-1]):
			np = []
			for i in p:
				np.append(i)
			np.append(up)
			nrp += [np]
		if not intersectWall(ri, p[-1]):
			np = []
			for i in p:
				np.append(i)
			np.append(ri)
			nrp += [np]
		if not intersectWall(bo, p[-1]):
			np = []
			for i in p:
				np.append(i)
			np.append(bo)
			nrp += [np]
		if not intersectWall(le, p[-1]):
			np = []
			for i in p:
				np.append(i)
			np.append(le)
			nrp += [np]

		print('NRP', nrp)
	Robot.rp, Robot.tp = nrp, ntp


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


getPath(-500, 0, -100, 800)  # startingrobotX, startingrobotY, targetX, tegetY
