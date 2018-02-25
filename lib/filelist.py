import os,re, sys
from pyglet.gl import *
from . import button, isvalidpath

executablefiles = ["wma","mp3","mp4","wmv"]

class filelist:
	def __init__(self,batch,x,y,width,height):
		from . import scroll
		scroll.register(self)
		try:
			if sys.platform == 'win32':
				self.currentdir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Music') 
			else:
				self.currentdir = os.path.join(os.path.join(os.path.expanduser('~')), 'Music') 
		except:
			if sys.platform == 'win32':
				self.currentdir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
			else:
				self.currentdir = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 			

		self.batch = batch

		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.visible = True

		self.scrollvalue = 0

		def onclickfunc(b):
			nonlocal self
			self.scrollvalue = 0

			driveletter = re.compile(r"\w:(?!\\)")
			try:
				old = self.currentdir
				if sys.platform == 'win32':

					self.currentdir = re.sub(r"\\+",r"\\",self.currentdir).rsplit("\\",1)[0]
				else:
					self.currentdir = re.sub(r"/+",r"/",self.currentdir).rsplit("/",1)[0]
				if driveletter.match(self.currentdir):
					self.currentdir = self.currentdir + "\\"
				try:
					self.update_filelist()
				except:
					self.currentdir = old
			except Exception as e:
				print(e,"on line 50 of filelist")

		def onclickfuncup(b):
			nonlocal self
			self.scrollvalue -= 1
			if self.scrollvalue > len(os.listdir(self.currentdir)) - self.height//30:
				self.scrollvalue = len(os.listdir(self.currentdir)) - self.height//30
			if self.scrollvalue < 0:
				self.scrollvalue = 0
			self.update_filelist()

		def onclickfuncdown(b):
			nonlocal self
			self.scrollvalue += 1
			if self.scrollvalue > len(os.listdir(self.currentdir)) - self.height//30:
				self.scrollvalue = len(os.listdir(self.currentdir))	 - self.height//30	
			if self.scrollvalue < 0:
				self.scrollvalue = 0
		
			# if self.scrollvalue > :		
			self.update_filelist()

		def onhoverfunc(b):
			b.color = (0.6,0.6,0.6,0.7)

		def onunhoverfunc(b):
			b.color = (0.7,0.7,0.7,0.5) 

		self.b = button.Button(self.batch,x=self.x,y=self.y-20,height=20,width=50,onclick=onclickfunc,onhover=onhoverfunc,onunhover=onunhoverfunc, text="back",color=(0.7,0.7,0.7,0.5))
		self.scrollup = button.Button(self.batch,x=self.x + self.width - 20,y=self.y+self.height//2,height=self.height//2,width=20,onclick=onclickfuncup,onhover=onhoverfunc,onunhover=onunhoverfunc, text="^",color=(0.7,0.7,0.7,0.5), textanchor="top")
		self.scrolldown = button.Button(self.batch,x=self.x + self.width - 20,y=self.y,height=self.height//2,width=20,onclick=onclickfuncdown,onhover=onhoverfunc,onunhover=onunhoverfunc, text="v",color=(0.7,0.7,0.7,0.5))
		self.label = pyglet.text.Label(text=self.currentdir,bold=True,font_name='Arial',font_size=10,x=self.x+70,y=self.y-20,color=(0,0,0,255),width=self.width-70)
		self.batchlabelid = self.batch.add(self.label)
		self.batch.add(self)
		self.buttons = []
		self.update_filelist()
	
	def set_visible(self):
		for i in self.buttons:
			i.visible = True
		self.scrollup.visible = True
		self.scrolldown.visible = True
		self.b.visible = True
		self.visible = True
		self.label = pyglet.text.Label(text=self.currentdir,bold=True,font_name='Arial',font_size=10,x=self.x+70,y=self.y-20,color=(0,0,0,255),width=self.width-70)
		self.batchlabelid = self.batch.add(self.label)

	def set_invisible(self):
		for i in self.buttons:
			i.visible = False
		self.scrollup.visible = False
		self.scrolldown.visible = False
		self.b.visible = False
		self.visible = False
		del self.label
		self.batch.remove(self.batchlabelid)

	def get_next_executable(self,filename):
		if sys.platform == 'win32':
			currentdir = re.sub(r"\\+",r"\\",filename).rsplit("\\",1)[0]
			f = filename.split("\\")[-1]
		else:
			currentdir = re.sub(r"/+",r"/",filename).rsplit("/",1)[0]
			f = filename.split("/")[-1]
		canchoose = False
		for i in os.listdir(currentdir):
			if i == f:
				canchoose = True
				continue
			if canchoose and i.split(".")[-1] in executablefiles:
				return os.path.join(currentdir, i)

		return None		

	def update_filelist(self):
		self.label.text = self.currentdir
		def hoverfunc(b):
			b.color = (0.6,0.6,0.6,0.7)

		def unhoverfunc(b):
			b.color = (0.7,0.7,0.7,0.5) 

		def clickfunc(b):
			
			# try:
			if sys.platform == 'win32':
				if os.path.isdir(re.sub(r"\\+",r"\\",self.currentdir) + "\\" + b.value):
					self.currentdir = re.sub(r"\\+",r"\\",self.currentdir + "\\" + b.value)
					self.scrollvalue = 0
					self.update_filelist()
				else:
					for i in executablefiles:
						from . import setfile
						if (re.sub(r"\\+",r"\\",self.currentdir) + "\\" + b.value).endswith(i):
							setfile(re.sub(r"\\+",r"\\",self.currentdir) + "\\" + b.value)
							break

			else:
				if os.path.isdir(re.sub(r"/+",r"/",self.currentdir) + "/" + b.value):
					self.currentdir = re.sub(r"/+",r"/",self.currentdir + "/" + b.value)
					self.scrollvalue = 0
					self.update_filelist()
				else:
					for i in executablefiles:
						if (re.sub(r"\\+",r"\\",self.currentdir) + "\\" + b.value).endswith(i):
							currentfile = re.sub(r"\\+",r"\\",self.currentdir) + "\\" + b.value
							break	

			# except Exception as e:
			# 	print(e,"on line 142 of filelist")

		for i in self.buttons:
			i.batch.remove(i.batchid)
		self.buttons = []
		current = 30
		for i in os.listdir(self.currentdir)[self.scrollvalue:]:
			if current - 30 >= self.height:
				break
			b = button.Button(self.batch,text=str(i),x=self.x,y=self.y + self.height - current,width=self.width-20,height=30,color=(0.7,0.7,0.7,0.5), onhover = hoverfunc, onunhover = unhoverfunc,onrelease=clickfunc)
			b.value = i
			self.buttons.append(b)
			current += 30

	def scroll(self,val):
		self.scrollvalue -= int(val)
		if self.scrollvalue > len(os.listdir(self.currentdir)) - self.height//30:
			self.scrollvalue = len(os.listdir(self.currentdir))	 - self.height//30	
		if self.scrollvalue < 0:
			self.scrollvalue = 0
		self.update_filelist()

	def update(self,window):
		pass

	def draw(self):
		if self.visible:
			glLoadIdentity()
			glBegin(GL_LINES)
			glColor4f(0,0,0,1)
			glVertex2f(self.x,self.y)
			glVertex2f(self.x+ self.width,self.y)
			glVertex2f(self.x + self.width, self.y)
			glVertex2f(self.x + self.width, self.y + self.height)
			glVertex2f(self.x + self.width, self.y + self.height)
			glVertex2f(self.x, self.y + self.height)
			glVertex2f(self.x, self.y + self.height)
			glVertex2f(self.x,self.y)
			glEnd()