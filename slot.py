class Slot:

	def __init__(self, rawData):
		self._rawData = rawData
		self.id = int(rawData["id"])
		self.description = rawData["description"]
		self.idle = rawData["idle"]
		self.queues = []
	
	def __str__(self):
		state = "active"
		if self.idle:
			state = "inactive"
		return "slot {id} is {state}, and has {queues} queues. Description: {desc}".format(id=self.id, state=state, queues=len(self.queues), desc=self.description)
	
	def __unicode__(self):
		return self.__str__()
	