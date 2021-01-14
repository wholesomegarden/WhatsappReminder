# ReminderService.py
from User import User
from Reminder import Reminder
from Conv import Conv
# from app import Service
# from ctparse import ctparemidrse
# from datetime import datetime
from dateparser.search import search_dates

import time
import datetime
import re

from threading import Thread

known = {"Morning":"at 08:00", "evening":"at 18:00", "in in":"in","at at":"at", "בבוקר":"08:00"}
days = "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(",")

# class ReminderService(Service):
class ReminderService():
	users = {}
	upcoming = {}
	init = False
	serviceName= "Reminders"
	groupName = "🔔 Reminders 🔔"
	welcome =  "*Welcome to Reminders 🔔 Service*\nYou can now send a message and we will send you a reminder :)\nשלחו הודעה ואנחנו כבר נזכיר לכם :)\n\nFor example:\nThats awesome in 5 seconds\nלהתקשר לברוך מחר בבוקר"


	def getDB():
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("USERS")
		print(ReminderService.users)

		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("JSON")
		jsonUsers = User.usersToJSONusers(ReminderService.users)
		print(jsonUsers)

		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("recovered USERS")
		print(User.jsonUsersToUsers(jsonUsers))

		return {"users":jsonUsers,"upcoming":ReminderService.upcoming}
		# return {"users":ReminderService.users,"upcoming":ReminderService.upcoming}


	def setDB(db):
		ReminderService.upcoming = db["upcoming"]
		ReminderService.users = User.jsonUsersToUsers(db["users"])

	def backup():
		ReminderService.backupDelegate(db = ReminderService.getDB(),service = ReminderService.serviceName)

	def loadDB():
		res = ReminderService.backupDelegate(db = None,service = ReminderService.serviceName)
		if res is not None:
			resave = False
			if "upcoming" not in res:
				res["upcoming"] = {}
				resave = True
			if "users" not in res:
				res["users"] = {}
				resave = True
			ReminderService.setDB(res)
			if resave:
				ReminderService.backup()


	def asyncRoll():
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		t = Thread(target = ReminderService.rollUpcoming,args = [None,])
		t.start()

	def rollUpcoming(data):
		"!!!!!!!!!!!!!!!!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@"
		while(True):
			for key in list(ReminderService.upcoming.keys()):
				t = ReminderService.upcoming[key]
				if time.time()-t > 0:
					userID,remID = key.split("_")
					ReminderService.send(userID, remID)
			time.sleep(1)


	# shared = None
	#
	# def __init__(self):
	#     shared = sel
	#     pass #load from back

	def go(sendDelegate = None, backupDelegate = None):
		## LOAD FROM DAL

		ReminderService.users = {}
		ReminderService.upcoming = {}
		ReminderService.init = True
		ReminderService.asyncRoll()
		ReminderService.sendDelegate = sendDelegate
		ReminderService.backupDelegate = backupDelegate
		ReminderService.loadDB()


	def process(userID, message):
		print(ReminderService.init,"!!!!!!!!!!!!")
		if not ReminderService.init:
			ReminderService.go()

		dbChanged = False

		userID = str(userID)
		if userID not in ReminderService.users:

			user = User(userID)
			ReminderService.users[userID] = user

			user.conv.manager("WELCOME "+userID)
			ReminderService.actuallySend(userID, "WELCOME "+userID)
			dbChanged = True

		user = ReminderService.users[userID]
		user.conv.human(message)
		timestr = ""

		if not user.conv.ongoing:
		# check for commands
			print("AAAAAAAAAAAAAAAAAA")
			m, t, timestr = ReminderService.parseMsg(message)
			if t is None:
				user.conv.manager("When to remind you?")
				ReminderService.actuallySend(userID, "When shall I remind you ?")
				user.conv.ongoing = True
			else:
				ReminderService.convFinished(user, set = True)

			rem = ReminderService.newReminder(userID, m, t)



		else:
				print("BBBBBBBBBBBBBBBBBBBBB")
				user.conv.tries += 1
				m, t, timestr = ReminderService.parseMsg(message)
				## GET LAST REMINDER

				if t is None:
					user.conv.manager("Sorry I didnt understand when  "+ str(user.conv.tries))
					ReminderService.actuallySend(userID, "Sorry I didn't unserstand when...")

				else:
					rem = user.lastRem
					rem.sendTime = t

					ReminderService.convFinished(user, set = True)

		if ReminderService.convFinished(user):
			rem = user.lastRem

			if rem.sendTime is not None:
				user.conv.manager(" ".join(["THANK YOU! WILL REMIND YOU TO ",rem.message, "at",time.ctime(rem.sendTime)," (",timestr,")"]))
				ReminderService.actuallySend(userID, " ".join(["THANK YOU! WILL REMIND YOU TO ",rem.message, "at",time.ctime(rem.sendTime)," (",timestr,")"]))

				combID = userID+"_"+rem.id
				ReminderService.upcoming[combID] = rem.sendTime
				dbChanged = True
			else:
				print("XXXXXXXXXXXXXXXXXXXXXXXX", "unhandled")

			ReminderService.convFinished(user, set = None)
			user.conv.ongoing = False
		else:
			print("***continue conv!!!!!!!!!!!!!!!!!!")

		if dbChanged:
			ReminderService.backup()


	def convFinished(user, set = -1):
		if set is -1:
			convFin = True
			for key in user.conv.fin:
				if user.conv.fin[key] is None:
					convFin = False
			return convFin
		else:
			for key in user.conv.fin:
				user.conv.fin[key] = set

	def send(userID, remID):
		userID, remID = str(userID), str(remID)
		combID = userID+"_"+remID
		if userID in ReminderService.users:
			user = ReminderService.users[userID]
			if remID in user.reminders["unsent"]:
				rem = user.reminders["unsent"][remID]
				print("!!!!!!!",rem)
				if ReminderService.actuallySend(userID,rem.message):
					if user.markSent(remID):
						if combID in ReminderService.upcoming:
							ReminderService.upcoming.pop(combID)
							ReminderService.backup()
						else:
							print("EEEEEEEEE", "wasn't in upcoming")

					else:
						print("EEEEEEEEE", "could not mark!")

				else:
					print("EEEEEEEEE", "could not send!")



	def actuallySend(userID, message):
		print("TRY SENDING ON WHATSAPP! TO:", userID, "MESSAGE:", message)
		return ReminderService.sendDelegate(userID,message)

		# return False #for errors

	def getRE(key):
		return re.compile(re.escape(key.lower()), re.IGNORECASE)


	def formatKnown(txt):
		for key in known:
			keyRE = ReminderService.getRE(key)
			changed = keyRE.sub(known[key],txt)
			if txt != changed:
				print("-------CHANGED",txt,"TO",changed)
				txt = changed
		return txt

	def parseMsg(txt, tries = 0):
		print("============================")
		print(txt)
		formatted = ReminderService.formatKnown(txt)
		timestr = ""
		res = search_dates(formatted, add_detected_language=True)
		when = None
		if res is None:
			return txt, when, timestr
		if True:#try:
			# print("######################",formatted)
			# print(res)
			date = res[0][1].timestamp()
			timestr = res[0][0]
			lang = res[0][2]
			## remove timestr from reminder

			diff = time.time()-date
			# print("DIFF",diff, time.ctime(date))
			if diff > 0 and tries < 3:
				print("RETRY ")
				if tries == 0:
					new = ReminderService.changeDay(formatted)
				else:
					new = formatted.replace(timestr,"in "+timestr)
				return ReminderService.parseMsg(new, tries+1 )
			else:
				when = date
		# if True:#except:
		#     print("EEEEEEEEEEEEEEEEEEEEEE res:",res)
		#     return txt, None, ""

		if timestr is not "":
			formatted = txt.replace(timestr,"")
		return formatted, when, timestr

	def changeDay(txt):
		# print("CCCCCCCCCCCCC C C C C C C, ",txt,"\n")
		temp = txt + ""
		today = datetime.date.today().strftime("%A")
		currday = days.index(today)
		dates = []
		for d in range(7):
			c = (d+currday+1)%7
			dates.append(days[c])
		print("DATES::::::::::::::::::")
		print(dates)

		kc = 0
		for key in dates:
			kc+=1
			realday = "in "+str(kc)+" day"
			if c>1:
				realday+="s"
			print("DDDDDD ",realday)
			keyRE = ReminderService.getRE(key)
			changed = keyRE.sub(realday,txt)
			print("TTTTTTTT",changed)
			print
			txt = changed
		if temp != txt:
			print("CHANGED FROM -",temp," TO -",txt)
		else:
			print("NOT CHANGED DAY")
		return txt

	def newReminder(userID, message, when = None):

		user = ReminderService.users[userID]
		if user is None:
			print("user not found")
			return None

		user.remCount += 1
		remID = str(user.remCount)
		rem = Reminder(remID, userID, message, when)
		user.reminders["unsent"][remID] = rem
		user.lastRem = rem

		return rem
