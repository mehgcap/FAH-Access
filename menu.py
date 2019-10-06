class MenuItem(object):

	def __init__(self, number, text, function):
		self.number = number
		self.text = text
		self.function = function
	
	def run(self, *args, **kwargs):
		self.function(*args, **kwargs)
	