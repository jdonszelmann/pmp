import uuid

class Batch:
	def __init__(self,window):
		self.batch = {}
		self.window = window

	def add(self,obj):
		identifier = uuid.uuid4()
		self.batch[identifier] = obj
		return identifier

	def remove(self,identifier):
		self.batch.pop(identifier,None)

	def draw(self):
		for key,item in self.batch.items():
			if hasattr(item,"visible"):
				if item.visible:
					item.draw()
			else:
				item.draw()

	def update(self):
		try:
			for key,item in self.batch.items():
				try:
					item.update(self.window)
				except Exception as e:
					if "Label" not in repr(e):
						print(e,"on line 28 of custombatch")
						raise
		except Exception as e:
			if "dictionary" not in repr(e):
				print(e,"on line 31 of custombatch")
				raise


