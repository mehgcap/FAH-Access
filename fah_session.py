import telnetlib

class FAHSession:

	def __init__(self, host="localhost", port=36330, timeout=7):
		self._session = telnetlib.Telnet(host, port, timeout)
		self.timeout = timeout
	
	def getPreparedResponse(self, command, timeout=None):
		if timeout is None:
			timeout = self.timeout
		#sends the command to the Telnet session, reads the response, and strips all the extra data so the resulting PyON can be evaluated
		self._session.write("{cmd}\n".format(cmd=command).encode("ascii"))
		#this line will skip the PyON header
		unnecessaryLines = self._session.read_until(b"\nPyON ", timeout)
		if unnecessaryLines is None or unnecessaryLines == "" or "PyON" not in unnecessaryLines.decode("ascii"):
			raise Exception("invalid response received for command")
		#read the PyON message
		lines = self._session.read_until(b"---\n", timeout).decode("ascii")
		#we want to strip the first and last couple lines, so make an array by splitting on the return character
		lineArray = lines.split("\n")
		#strip the first line, and the last two lines, and join the whole thing with new lines so it can be evaluated
		lines = "\n".join(lineArray[1:(len(lineArray)-2)])
		return lines
	
	def getSlotInfo(self):
		slotLines = self.getPreparedResponse("slot-info")
		return eval(slotLines, {}, {})
	
	def getQueueInfo(self):
		queueLines = self.getPreparedResponse("queue-info")
		return eval(queueLines, {}, {})
	
	def close(self):
		self._session.close()
	