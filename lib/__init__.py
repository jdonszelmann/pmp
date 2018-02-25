import tkinter, pyglet, sys, time as pytime, threading, datetime
from . import playsound, button, custombatch, progressbar, filelist, videoviewer
from pyglet.gl import *
from math import pi,sin,cos,tan

currentsong = None
currentfile = None

def setfile(filename):
	global currentfile, currentsong
	if "playpause" in globals():
		try:
			playpause.active = True
		except:
			pass

	currentfile = filename
	if currentsong:
		currentsong.stop()
		currentsong = None
		
	if not currentsong:
		currentsong = playsound.sound(currentfile)
	currentsong.play()

class scroller:
	def __init__(self):
		self.objects = []

	def register(self,obj):
		self.objects.append(obj)

	def update(self,val):
		for i in self.objects:
			i.scroll(val)

scroll = scroller()


def waiter():
	pytime.sleep(0.5)
	if currentsong:
		currentsong.play()


def waitforplay():
	a = threading.Thread(target=waiter)
	a.start()

def glCircle(x, y, radius,color):
	iterations = int(2*radius*pi)
	s = sin(2*pi / iterations)
	c = cos(2*pi / iterations)

	dx, dy = radius, 0
	
	glBegin(GL_TRIANGLE_FAN)
	glColor4f(*color)
	glVertex2f(x, y)
	for i in range(iterations+1):
		glVertex2f(x+dx, y+dy)
		dx, dy = (dx*c - dy*s), (dy*c + dx*s)
	glEnd()


pyglet.options['debug_gl'] = False

mouseX=mouseY=0
mousePressed = -1

def start():
	window = pyglet.window.Window(640, 480, resizable=False, vsync=True, caption="Python Media Player")
	icon1 = pyglet.image.load('lib/icon.png')
	window.set_icon(icon1)
	batch = custombatch.Batch(window)
	glClearColor(1,1,1,1)

	class circle:
		def shape(self,button):
			glCircle(button.x,button.y,max(button.width,button.height),button.color)
			button.label.draw()
		
		def inside(self,button,x,y):
			return ((button.x-x)**2+(button.y-y)**2)**0.5 <= max(button.width,button.height)

	class stopbutton(circle):
		def shape(self,button):
			glCircle(button.x,button.y,max(button.width,button.height),button.color)
			glLoadIdentity()
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
			glEnable(GL_LINE_SMOOTH);
			glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
			glBegin(GL_QUADS)
			glColor4f(0,0,0,1)
			glVertex2f(button.x-10, button.y+10)
			glVertex2f(button.x-10, button.y-10)
			glVertex2f(button.x+10, button.y-10)
			glVertex2f(button.x+10, button.y+10)
			glEnd()

	class playbutton(circle):
		def shape(self,button):
			if not hasattr(button,"active"):
				button.active = False

			glCircle(button.x,button.y,max(button.width,button.height),button.color)
			if not button.active:
				glLoadIdentity()
				glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
				glEnable(GL_LINE_SMOOTH);
				glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
				glBegin(GL_TRIANGLES)
				glColor4f(0,0,0,1)
				glVertex2f(button.x-8, button.y+10)
				glVertex2f(button.x-8, button.y-10)
				glVertex2f(button.x+10, button.y)
				glEnd()
			else:
				glLoadIdentity()
				glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
				glEnable(GL_LINE_SMOOTH);
				glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
				glBegin(GL_QUADS)
				glColor4f(0,0,0,1)
				glVertex2f(button.x-8, button.y-10)
				glVertex2f(button.x-8, button.y+10)
				glVertex2f(button.x-4, button.y+10)
				glVertex2f(button.x-4, button.y-10)
				glVertex2f(button.x+8, button.y-10)
				glVertex2f(button.x+8, button.y+10)
				glVertex2f(button.x+4, button.y+10)
				glVertex2f(button.x+4, button.y-10)				
				glEnd()			

	def moveprogress(bar,status):
		global currentsong
		if status == "dragging":
			if currentsong:
				currentsong.pause()
				timelabel.text = "{}".format(str(datetime.timedelta(seconds=round(currentsong.duration*bar.progress,0))))
		if status == "stopping":
			if currentsong:
				currentsong.goto(currentsong.duration*bar.progress)
				waitforplay()
		if status == "jump":
			if not currentsong:
				currentsong = playsound.sound(currentfile)
			currentsong.goto(currentsong.duration*bar.progress)
			waitforplay()

	global playpause
	playpause = button.Button(batch,width=25,x=window.width/2 - 50,y=50,color=(1,1,1,1),shape=playbutton())
	stopsong = button.Button(batch,width=25,x=window.width/2 + 50,y=50,color=(1,1,1,1),shape=stopbutton())
	progress = progressbar.progressbar(batch,length=window.width-20,x=10,y=90, callback=moveprogress)
	timelabel = pyglet.text.Label(text="-:--:--",x=5,y=60,font_name="Arial",font_size=12,color=(0,0,0,255))
	totaltimelabel = pyglet.text.Label(text="-:--:--",x=window.width-5,anchor_x="right",y=60,font_name="Arial",font_size=12,color=(0,0,0,255))
	file_explorer = filelist.filelist(batch,20,150,window.width-40,window.height-150)
	video_viewer = videoviewer.videoviewer(batch,20,150,window.width-40,window.height-150)
	currently_playing = pyglet.text.Label(text=str(currentfile),x=2,y=2,font_name="Arial",bold=True,font_size=8,color=(0,0,0,255))
	switch_video = button.Button(batch,text="fileview",x=window.width-70,width=50,y=120,font="Arial",size=8,color=(1,1,1,1))
	batch.add(currently_playing)
	batch.add(timelabel)
	batch.add(totaltimelabel)
	video_viewer.set_invisible()

	@switch_video.onclick
	def onunclick(b):
		if not hasattr(b,"active"):
			b.active = False
		b.active = not b.active
		if b.active:
			b.text = "videoview"
			video_viewer.set_visible()
			file_explorer.set_invisible()
		else:
			b.text = "fileview"
			file_explorer.set_visible()
			video_viewer.set_invisible()

	@switch_video.onhover
	def onhover(b):
		b.color = (0.6,0.6,0.6,0.5)
	
	@switch_video.onunhover
	def onunhover(b):
		b.color = (1,1,1,1)

	@playpause.onclick
	def onclick(b):
		if currentfile != None:
			global currentsong
			if not currentsong:
				currentsong = playsound.sound(currentfile)
				progress.progress = 0
			if not hasattr(b,"active"):
				b.active = False
			b.active = not b.active

			if b.active:
				currentsong.play()
			else:
				currentsong.pause()
	
	@stopsong.onclick
	def onclick(b):
		global currentsong, currentfile
		if currentsong:
			currentsong.stop()
			playpause.active = False
			currentsong = None
			progress.progress = 0
			currentfile = None


	@stopsong.onhover
	def onhover(b):
		b.color = (0.6,0.6,0.6,0.5)
	
	@stopsong.onunhover
	def onunhover(b):
		b.color = (1,1,1,1)

	@playpause.onhover
	def onhover(b):
		b.color = (0.6,0.6,0.6,0.5)
	
	@playpause.onunhover
	def onunhover(b):
		b.color = (1,1,1,1)

	def update(dt):
		global currentfile, currentsong
		currently_playing.text = str(currentfile)

		if currentsong:
			if not progress.status == "dragging" and currentsong.playing:
				progress.progress = currentsong.time / currentsong.duration
				try:
					timelabel.text = "{}".format(str(datetime.timedelta(seconds=round(currentsong.time,0))))
					totaltimelabel.text = "{}".format(str(datetime.timedelta(seconds=round(currentsong.duration-currentsong.time,0))))
				except:
					timelabel.text = "-:--:--"
					totaltimelabel.text = "-:--:--"	
			else:
				pass
			try:
				if round(currentsong.duration,1) == round(currentsong.time,1) and currentsong.duration != None:
					currentsong.stop()
					progress.progress = 0
					currentfile = file_explorer.get_next_executable(currentfile)
					if currentfile == None:
						currentsong = None
						pass
					else:
						playpause.active = True
						currentsong = playsound.sound(currentfile)
						currentsong.play()
			except:
				currentsong = None
				currentfile = None
		else:
			timelabel.text = "-:--:--"
			totaltimelabel.text = "-:--:--"
		batch.update()

	@window.event
	def on_mouse_motion(x, y, dx, dy):
		global mouseY, mouseX
		mouseX = x
		mouseY = y
	
	@window.event
	def on_mouse_drag(x, y, dx, dy,buttons,modifiers):
		global mouseY, mouseX
		mouseX = x
		mouseY = y

	@window.event
	def on_mouse_scroll(x, y, scroll_x, scroll_y):
		scroll.update(scroll_y)

	@window.event
	def on_mouse_press(x, y, buttons, modifiers):
		global mousePressed
		mousePressed = buttons

	@window.event
	def on_mouse_release(x, y, button, modifiers):
		global mousePressed
		mousePressed = -1

	@window.event
	def on_draw():
		glClear(GL_COLOR_BUFFER_BIT)
		glEnable(GL_BLEND);
		batch.draw()

	@window.event
	def on_close():
		window.close()
		sys.exit()

	@window.event
	def on_resize(width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(gl.GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, width, 0, height, -1, 1)
		glMatrixMode(gl.GL_MODELVIEW)

	event_loop = pyglet.app.EventLoop()
	pyglet.clock.schedule_interval(update, 1/120.0)
	event_loop.run()