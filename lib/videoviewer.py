import pyglet
from pyglet.gl import *


class videoviewer:
	def __init__(self,batch,x,y,width,height):
		self.batch = batch
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.visible = True
		self.currentlyplaying = None

		self.batch.add(self)

	def set_visible(self):
		self.visible = True

	def set_invisible(self):
		self.visible = False

	def update(self,window):
		from . import currentsong
		self.currentlyplaying = currentsong

	def draw(self):
		if self.currentlyplaying != None:
			if self.currentlyplaying.song:
				t = self.currentlyplaying.song.get_texture()
				if t and self.currentlyplaying.song.source and self.currentlyplaying.song.source.video_format:
					glLoadIdentity()
	
					t = self.currentlyplaying.song.get_texture()
					gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
					t.width = self.width
					t.height = self.height
					t.blit(self.x,self.y)
				else:
					l = pyglet.text.Label(text="no video source available",color=(0,0,0,255),x=self.width//2,y=self.height//2,anchor_x="center")
					l.draw()
			else:
				l = pyglet.text.Label(text="no video source available",color=(0,0,0,255),x=self.width//2,y=self.height//2,anchor_x="center")
				l.draw()
		else:
			l = pyglet.text.Label(text="no video source available",color=(0,0,0,255),x=self.width//2,y=self.height//2,anchor_x="center")
			l.draw()