import pyglet
pyglet.options['debug_gl'] = False
sounds = []

class sound:
	def __init__(self,filename=None):
		self.filename = filename
		self.song = None
		try:
			self.sound = pyglet.media.load(self.filename.encode("utf-8"))
		except Exception as e:
			print(e,"on line 12 of playsound")
			self.sound = None

	def load(self,filename):
		self.filename = filename
		try:
			self.sound = pyglet.media.load(self.filename.encode("utf-8"))
		except Exception as e:
			print(e,"on line 20 of playsound")
			self.sound = None

	def play(self):
		if self.filename == None:
			print("could not play sound. file not loaded")
			return
		if not self.sound:
			try:
				self.sound = pyglet.media.load(self.filename.encode("utf-8"))
			except Exception as e:
				print(e,"on line 31 of playsound") 
				self.sound = None
			if not self.sound:
				print("could not play sound. file not loaded")
				return
		if self.song:
			self.song.play()
		else:		
			self.song = self.sound.play()

	@property
	def playing(self):
		return self.song.playing if self.song else None

	def pause(self):
		if self.song: self.song.pause()

	@property
	def duration(self):
		if self.sound:
			return self.sound.duration

	@property
	def time(self):
		if self.song:
			return self.song.time

	def stop(self):
		if self.song:
			if self.song: self.song.pause()
			self.song.next_source()
			self.sound = None
			self.song = None

	def goto(self,time):
		if self.sound:
			try:
				self.sound.seek(time)
			except OSError:
				pass





