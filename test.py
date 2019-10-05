from queue import Queue
from slot import Slot
import telnetlib

host = "localhost"
port = 36330
session = telnetlib.Telnet(host, port)
queues = {}
slots = {}

#get the slot info
session.write("slot-info\n".encode("ascii"))
#this line will skip the PyON header
unnecessaryLines = session.read_until(b"\nPyON ")
#read the PyON message
slotLines = session.read_until(b"---\n").decode("ascii").split("\n")
slotLines = "\n".join(slotLines[1:(len(slotLines)-2)])
slotsData = eval(slotLines, {}, {})
for slotData in slotsData:
	slot = Slot(slotData)
	slots[slot.id] = slot

session.write("queue-info\n".encode("ascii"))
#this line will skip the PyON header
unnecessaryLines = session.read_until(b"\nPyON ")
#read the PyON message
queueLines = session.read_until(b"---\n").decode("ascii").split("\n")
queueLines = "\n".join(queueLines[1:(len(queueLines)-2)])
queuesData = eval(queueLines, {}, {})
for queueData in queuesData:
	queue = Queue(queueData)
	queues[queue.id] = queue
	slotID = queue.slot
	slots[slotID].queues.append(queue)

#output the results
for slot in slots.values():
	print(slot.__str__() + "\n")
for queue in queues.values():
	print(queue.__str__() + "\n")

session.close()
