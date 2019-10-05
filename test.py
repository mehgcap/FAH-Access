from queue import Queue
from slot import Slot
import telnetlib

host = "localhost"
port = 36330
session = telnetlib.Telnet(host, port)
queues = {}
slots = {}

def getPreparedResponse(session, command):
	#sends the command to the Telnet session, reads the response, and strips all the extra data so the resulting PyON can be evaluated
	session.write("{cmd}\n".format(cmd=command).encode("ascii"))
	#this line will skip the PyON header
	unnecessaryLines = session.read_until(b"\nPyON ")
	#read the PyON message
	lines = session.read_until(b"---\n").decode("ascii")
	#we want to strip the first and last couple lines, so make an array by splitting on the return character
	lineArray = lines.split("\n")
	#strip the first line, and the last two lines, and join the whole thing with new lines so it can be evaluated
	lines = "\n".join(lineArray[1:(len(lineArray)-2)])
	return lines

#get the slot info
slotLines = getPreparedResponse(session, "slot-info")
slotsData = eval(slotLines, {}, {})
#add all the slots to our dictionary
for slotData in slotsData:
	slot = Slot(slotData)
	slots[slot.id] = slot

queueLines = getPreparedResponse(session, "queue-info")
queuesData = eval(queueLines, {}, {})
for queueData in queuesData:
	queue = Queue(queueData)
	queues[queue.id] = queue
	slotID = queue.slot
	slots[slotID].queues.append(queue)

#get basic details
optionsData = getPreparedResponse(session, "options user team")
print(optionsData)

#output the results
for slot in slots.values():
	print(slot.__str__() + "\n")
for queue in queues.values():
	print(queue.__str__() + "\n")

session.close()
