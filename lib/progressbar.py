from pyglet.gl import *


class progressbar:
	def __init__(self,batch,x,y,length,color=(0,0,0,1),callback=lambda:None):
		self.y = y
		self.x = x
		self.length = length
		self.color = color

		self.progress = 0
		self.thumbx = self.x
		self.thumby = self.y

		self.callback = callback

		self.clicked = False
		self.hover = False

		self.status = "normal"

		batch.add(self)

	def update(self,window):
		self.thumbx = (self.progress * self.length) + self.x

		oldstatus = self.status

		from . import mouseX,mouseY,mousePressed, currentfile
		if self.thumbx-3 < mouseX < self.thumbx + 8 + 3 and self.thumby - 3 < mouseY < self.thumby + 16 + 3:
			self.hover = True
		else:
			self.hover = False

		if self.hover and mousePressed == 1 and not self.clicked:
			self.clicked = True
		elif not(self.hover and mousePressed == 1) and self.clicked:
			self.clicked = False
		
		if not self.clicked and mousePressed != 1:
			self.status = "normal"

		if self.clicked and currentfile:
			self.status = "dragging"

		if self.status == "dragging":
			oldthumbx = self.thumbx
			oldprogress = self.progress
			pixafterstart = mouseX-self.x
			self.progress = pixafterstart/self.length
			self.thumbx = (self.progress * self.length) + self.x
			if self.thumbx != oldthumbx:
				self.callback(self,self.status)


		if self.thumbx > self.length + self.x:
			self.thumbx = self.length + self.x

		if self.thumbx < self.x:
			self.thumbx = self.x

		if self.y - 6 < mouseY < self.y + 6 and not self.hover and self.x < mouseX < self.x + self.length:
			if mousePressed == 1 and currentfile:
				pixafterstart = mouseX-self.x
				self.progress = pixafterstart/self.length
				self.callback(self,"jump")


		if self.status != oldstatus and oldstatus == "dragging":
			self.callback(self,"stopping")

	def draw(self):
		glLoadIdentity()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		glEnable(GL_LINE_SMOOTH);
		glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
		
		glBegin(GL_LINES)
		glColor4f(*self.color)
		glVertex2f(self.x, self.y)
		glVertex2f(self.x+self.length, self.y)
		glEnd()

		if self.hover:
			size = 9
		else:
			size = 8

		glLoadIdentity()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		glEnable(GL_LINE_SMOOTH);
		glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
		glBegin(GL_QUADS)
		glColor4f(*self.color)
		glVertex2f(self.thumbx, self.thumby+size)
		glVertex2f(self.thumbx+size, self.thumby+size)
		glVertex2f(self.thumbx+size, self.thumby-size)
		glVertex2f(self.thumbx, self.thumby-size)
		glEnd()