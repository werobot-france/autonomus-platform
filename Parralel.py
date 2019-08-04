from time import sleep
from math import *
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


def getP(L):
	d = distance()

	print('cos', cos(acos(B[0]-A[0]/d)))
	p12 = [L[1][0]+E*(1+cos(abs(acos(B[0]-A[0]/d)))), L[1][1]+E*(cos(abs(acos(B[0]-A[0]/d))))]
	p11 = [L[0][0]+E*(1+cos(abs(acos(B[0]-A[0]/d)))), L[0][1]+E*(cos(abs(acos(B[0]-A[0]/d))))]

	p13 = [L[1][0]-E*(1+cos(abs(acos(B[0]-A[0]/d)))), L[1][1]-E*(cos(abs(acos(B[0]-A[0]/d))))]
	p14 = [L[0][0]-E*(1+cos(abs(acos(B[0]-A[0]/d)))), L[0][1]-E*(cos(abs(acos(B[0]-A[0]/d))))]


	print(distance(p12, p13))

	return [[p11, p12], [p13, p14]]

B = [0,0]
A = [5,5]
E = 2


def distance(A=A, B=B):
	return sqrt(abs((B[0]- A[0])**2+(B[1]-A[1])**2))

fig, ax = plt.subplots()
plt.plot([A[0], B[0]], [A[1], B[1]], 'bo')

ax.add_line(MyLine([A[0], B[0]], [A[1], B[1]]))

plt.axis([-10, 10, -10, 10])

for p in getP([A, B]):
	print(p)
	plt.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], 'ro')
	ax.add_line(MyLine([p[0][0], p[1][0]], [p[0][1], p[1][1]]))
plt.show()


