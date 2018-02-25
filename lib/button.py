import pyglet
from pyglet.gl import *

ftoicolor = lambda l: tuple(map(lambda x:x*255,list(l)))


class Button:
	def __init__(self,batch,x=0,y=0,width=50,height=20,visible=True,size=14,shape=None,font='Arial',color=(1,1,1,1),textcolor=(0,0,0,1),text="",onclick=lambda:None,onhover=lambda:None,onunhover=lambda:None,onrelease=lambda:None, textanchor="bottom"):
		self.textanchor = textanchor
		self.label = None		
		self.batch = batch
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.font = font
		self.size = size
		self.textcolor = ftoicolor(textcolor)
		self._onclick = onclick
		self._onrelease = onrelease
		self._onhover = onhover
		self._onunhover = onunhover
		self.color = color
		self.text = text
		self.hover = False
		self.clicked = False
		self.visible = visible
		self.shape = shape


		self.batchid = self.batch.add(self)

	def update(self,window):
		if self.visible:
			from . import mouseX,mouseY,mousePressed
			if not self.shape:
				if self.x < mouseX < self.x + self.width and self.y < mouseY < self.y + self.height and not self.hover:
					self.hover = True
					try:
						self._onhover(self)
					except Exception:
						self._onhover()
				elif self.hover and not (self.x < mouseX < self.x + self.width and self.y < mouseY < self.y + self.height):
					try:
						self._onunhover(self)
					except Exception:
						self._onunhover()
					self.hover = False
			else:
				if self.shape.inside(self,mouseX,mouseY) and not self.hover:
					self.hover = True
					try:
						self._onhover(self)
					except Exception as e1:
						try:
							self._onhover()
						except Exception as e2:
							print(e1, "-->", e2)
				elif self.hover and not (self.shape.inside(self,mouseX,mouseY)):
					try:
						self._onunhover(self)
					except Exception as e1:
						try:
							self._onunhover()
						except Exception as e2:
							print(e1, "-->", e2)
					self.hover = False				
			
			if self.hover and mousePressed == 1 and not self.clicked:
				self.clicked = True
				try:
					self._onclick(self)
				except Exception as e1:
					try:
						self._onclick()
					except Exception as e2:
						print(e1, "-->", e2)
			elif self.clicked and not (self.hover and mousePressed == 1):
				self.clicked = False
				try:
					self._onrelease(self)
				except Exception as e1:
					try:
						self._onrelease()
					except Exception as e2:
						print(e1, "-->", e2)

	@property
	def text():
		return self.label

	@text.setter
	def text(self,text):
		if self.textanchor == "bottom":
			self.label = pyglet.text.Label(text=text,font_name=self.font,font_size=self.size,width=self.width,height=self.height,x=self.x+2,y=self.y+2,color=self.textcolor)
		elif self.textanchor == "top":
			self.label = pyglet.text.Label(text=text,font_name=self.font,font_size=self.size,width=self.width,height=self.height,x=self.x+2,y=self.y+self.height-2,anchor_y = "top",color=self.textcolor)

		changed = False
		while True:
			if self.label.content_width > self.width:
				changed = True
				self.label.text = self.label.text[:-1]
			else:
				if changed:
					self.label.text = self.label.text[:-3] + "..."
				break


	def onhover(self,func):
		self._onhover = func

	def onunhover(self,func):
		self._onunhover = func

	def onclick(self,func):
		self._onclick = func

	def onrelease(self,func):
		self._onrelease = func

	def hide(self):
		self.visible = False

	def show(self):
		self.visible = True

	def draw(self):
		if self.visible:
			if self.shape:
				self.shape.shape(self)
			else:
				glLoadIdentity()
				glBegin(GL_QUADS)
				glColor4f(*self.color)
				glVertex2f(self.x,self.y)
				glVertex2f(self.x + self.width, self.y)
				glVertex2f(self.x + self.width, self.y + self.height)
				glVertex2f(self.x, self.y + self.height)
				glEnd()
				self.label.draw()

