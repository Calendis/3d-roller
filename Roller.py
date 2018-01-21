class Roller():
	"""These objects will scan the adjacent pixels for height and move there"""
	def __init__(self, x, y):
		super(Roller, self).__init__()
		self.x = x
		self.y = y
		self.radius = 2

	def update(self):
		pass

	def get_x(self, offset=0):
		return self.x+offset

	def get_y(self, offset=0):
		return self.y+offset

	def get_pos(self):
		return((self.get_x(), self.get_y()))

	def set_x(self, new_x):
		self.x = new_x

	def set_y(self, new_y):
		self.y = new_y

	def offset_pos(self, offpos):
		self.set_x(self.x+offpos[0])
		self.set_y(self.y+offpos[1])
		