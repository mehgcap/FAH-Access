from fah_session import FAHSession
from menu import MenuItem
from queue import Queue
from slot import Slot
from itertools import count

host = "localhost"
port = 36330
session = FAHSession(host, port)

def showSummary():
	queues = {}
	slots = {}
	
	#get the slot info
	slotsData = session.getSlotInfo()
	#add all the slots to our dictionary
	for slotData in slotsData:
		slot = Slot(slotData)
		slots[slot.id] = slot
	
	#now the queue info
	queuesData = session.getQueueInfo()
	for queueData in queuesData:
		queue = Queue(queueData)
		queues[queue.id] = queue
		#add this queue to it's parent slot's list of queues
		slotID = queue.slot
		slots[slotID].queues.append(queue)
	
	#get basic details
	teamInfo = eval(session.getPreparedResponse("options user team"), {}, {})
	
	print("User {user} is folding for team {team}".format(user=teamInfo["user"], team=teamInfo["team"]))
	for slot in slots.values():
		print(slot.__str__())
	for queue in queues.values():
		print(queue.__str__())

def close():
	global session
	session.close()
	exit()

def enterCommand():
	global session
	cmd = input("Enter a command to be sent directly to FAH:\n")
	result = session.getPreparedResponse(cmd)
	print(result)

counter = lambda c=count(): next(c) + 1
menuItems = [
	MenuItem(counter(), "Show summary", showSummary),
	MenuItem(counter(), "Enter Command", enterCommand),
	MenuItem(counter(), "Exit", close),
]

menuChoice = -1
validChoices = [item.number for item in menuItems]
while menuChoice not in validChoices:
	[print("{num}. {text}".format(num=item.number, text=item.text)) for item in menuItems]
	try:
		menuChoice = int(input("Choice: "))
	except ValueError:
		print("Invalid entry. Numbers only.")
		continue
	
	if menuChoice in validChoices:
		menuItems[menuChoice-1].run()
		menuChoice = -1
	else:
		print("{choice} is not a valid selection.".format(choice=menuChoice))

session.close()
