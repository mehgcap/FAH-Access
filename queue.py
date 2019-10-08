class Queue:

	def __init__(self, rawData):
		self._rawData = rawData
		self.state = rawData["state"]
		self.estimatedTimeLeft = rawData["eta"]
		self.ppd = rawData["ppd"]
		self.id = int(rawData["id"])
		#we use the ["-1] to trim the percent sign this field includes
		self.percentComplete = rawData["percentdone"][:-1]
		self.slot = rawData["slot"]
	
	def __str__(self):
		return "Queue {id} is {state}, at {percent}% (about {time} left), with {ppd} points per day".format(
			id=self.id,
			state=self.state,
			percent=self.percentComplete,
			time=self.estimatedTimeLeft,
			ppd=self.ppd
		)
	
	def __unicode__(self):
		return self.__str__()
	