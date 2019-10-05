class Queue:

	def __init__(self, rawData):
		self._rawData = rawData
		self.state = rawData["state"]
		self.id = rawData["id"]
		self.percentComplete = rawData["percentdone"][:-1]
		self.slot = rawData["slot"]
	
	def __str__(self):
		return "Queue {id} is {state}, at {percent}%".format(id=self.id, state=self.state, percent=self.percentComplete)
	
	def __unicode__(self):
		return self.__str__()
	