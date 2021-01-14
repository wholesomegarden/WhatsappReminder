# DanilatorService.py
from User import User
from Reminder import Reminder
from Conv import Conv
# from app import Service
# from ctparse import ctparemidrse
# from datetime import datetime
from bs4 import BeautifulSoup
import requests

from dateparser.search import search_dates

import time
import datetime
import re

from threading import Thread

known = {"Morning":"at 08:00", "evening":"at 18:00", "in in":"in","at at":"at", "בבוקר":"08:00"}
days = "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(",")

# class DanilatorService(Service):
class DanilatorService():
	users = {}
	upcoming = {}
	init = False
	serviceName= "Danilator"
	groupName = "💚 Danilator 💚"


	def getDB():
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("USERS")
		print(DanilatorService.users)

		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("JSON")
		jsonUsers = User.usersToJSONusers(DanilatorService.users)
		print(jsonUsers)

		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("recovered USERS")
		print(User.jsonUsersToUsers(jsonUsers))

		return {"users":jsonUsers,"upcoming":DanilatorService.upcoming}
		# return {"users":DanilatorService.users,"upcoming":DanilatorService.upcoming}


	def setDB(db):
		DanilatorService.upcoming = db["upcoming"]
		DanilatorService.users = User.jsonUsersToUsers(db["users"])

	def backup():
		DanilatorService.backupDelegate(db = DanilatorService.getDB(),service = DanilatorService.serviceName)

	def loadDB():
		res = DanilatorService.backupDelegate(db = None,service = DanilatorService.serviceName)
		if res is not None:
			resave = False
			if "upcoming" not in res:
				res["upcoming"] = {}
				resave = True
			if "users" not in res:
				res["users"] = {}
				resave = True
			DanilatorService.setDB(res)
			if resave:
				DanilatorService.backup()


	def asyncRoll():
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("YOY YOYOYOY YOY OY OY ")
		print("DANILATOR")
		t = Thread(target = DanilatorService.rollUpcoming,args = [None,])
		t.start()

	def rollUpcoming(data):
		"!!!!!!!!!!!!!!!!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@"
		while(True):
			for key in list(DanilatorService.upcoming.keys()):
				t = DanilatorService.upcoming[key]
				if time.time()-t > 0:
					userID,remID = key.split("_")
					DanilatorService.send(userID, remID)
			time.sleep(1)


	# shared = None
	#
	# def __init__(self):
	#     shared = sel
	#     pass #load from back

	def go(sendDelegate = None, backupDelegate = None):
		## LOAD FROM DAL

		DanilatorService.users = {}
		DanilatorService.upcoming = {}
		DanilatorService.init = True
		DanilatorService.asyncRoll()
		DanilatorService.sendDelegate = sendDelegate
		DanilatorService.backupDelegate = backupDelegate
		DanilatorService.loadDB()


	def process(userID, message):

		print(DanilatorService.init,"!!!!!!!!!!!!")
		if not DanilatorService.init:
			DanilatorService.go()

		dbChanged = False

		userID = str(userID)

		# dbChanged = False
		if userID not in DanilatorService.users:
			user = User(userID)
			DanilatorService.users[userID] = user

			user.conv.manager("WELCOME "+userID)
			DanilatorService.actuallySend(userID, "*Welcome to Danilator 💚 Service*\nYou can now send a name of a song to get it's lyrics translations :)")
			dbChanged = True

		user = DanilatorService.users[userID]
		#
		# for a in range(10):
		# 	DanilatorService.actuallySend(userID, str(a))
		target = message
		urlChecks = ["http","youtu","spotify.com"]
		url = False
		for check in urlChecks:
			if check.lower() in target.lower():
				url = True
		if url:
			target = str(re.search("(?P<url>https?://[^\s]+)", target).group("url"))
		DanilatorService.actuallySend(userID, "Checking Lyrics for:\n*"+target+"*\n"+"Please wait a bit")

		# import requests
		# from bs4 import BeautifulSoupYO
		# example = "We are the champions"
		# song = example.replace(" ","+")

		target = target.replace(" ","+")
		lyricsLink = "http://danilator.wholesome.garden/lyrics/"+target
		print (lyricsLink)
		page = requests.get(lyricsLink)
		# if str(page.status_code) == "200":
		soup = BeautifulSoup(page.content, 'html.parser')
		# print(soup.prettify())
		# print(soup.body[""])

		# txt = str(str(P).split('))

		title = soup.findAll("h3")[0].text.replace("                   ","").replace("                ","").replace("\n","")
		while title[-1:] is " ":
			title = title[:-1]

		P = soup.find_all('p')
		lyrics = []
		for pp in P:
			lyrics.append(pp.text.replace("\n","").replace("                ","").replace("              ",""))

		for l in lyrics:
			print("LLL:",l)

		firstLang = lyrics[0::4][:-1]
		secondLang = lyrics[1::4][:-1]

		cleanLyrics = "💚 *Danilator* 💚\n"
		cleanLyrics += "*"+title+"*"+"\n\n"

		for i in range(len(firstLang)):
			cleanLyrics += firstLang[i] +"\n"+ secondLang[i]+"\n\n"
		cleanLyrics+="Made with 💚\n"
		cleanLyrics+="from "+lyricsLink

		DanilatorService.actuallySend(userID, cleanLyrics)
		# if False:
		# 	DanilatorService.actuallySend(userID, "Could not fetch lyrics %0AE: "+e)


		#
		# for l in lyrics:
		# 	print(":::"+l+"::::")
		#
		# Made with 💚
		#
		# lyrics
		#
		#
		#
		#
		#
		# user.conv.human(message)
		# timestr = ""
		#
		# if not user.conv.ongoing:
		# # check for commands
		# 	print("AAAAAAAAAAAAAAAAAA")
		# 	m, t, timestr = DanilatorService.parseMsg(message)
		# 	if t is None:
		# 		user.conv.manager("When to remind you?")
		# 		DanilatorService.actuallySend(userID, "When shall I remind you ?")
		# 		user.conv.ongoing = True
		# 	else:
		# 		DanilatorService.convFinished(user, set = True)
		#
		# 	rem = DanilatorService.newReminder(userID, m, t)
		#
		#
		#
		# else:
		# 		print("BBBBBBBBBBBBBBBBBBBBB")
		# 		user.conv.tries += 1
		# 		m, t, timestr = DanilatorService.parseMsg(message)
		# 		## GET LAST REMINDER
		#
		# 		if t is None:
		# 			user.conv.manager("Sorry I didnt understand when  "+ str(user.conv.tries))
		# 			DanilatorService.actuallySend(userID, "Sorry I didn't unserstand when...")
		#
		# 		else:
		# 			rem = user.lastRem
		# 			rem.sendTime = t
		#
		# 			DanilatorService.convFinished(user, set = True)
		#
		# if DanilatorService.convFinished(user):
		# 	rem = user.lastRem
		#
		# 	if rem.sendTime is not None:
		# 		user.conv.manager(" ".join(["THANK YOU! WILL REMIND YOU TO ",rem.message, "at",time.ctime(rem.sendTime)," (",timestr,")"]))
		# 		DanilatorService.actuallySend(userID, " ".join(["THANK YOU! WILL REMIND YOU TO ",rem.message, "at",time.ctime(rem.sendTime)," (",timestr,")"]))
		#
		# 		combID = userID+"_"+rem.id
		# 		DanilatorService.upcoming[combID] = rem.sendTime
		# 		dbChanged = True
		# 	else:
		# 		print("XXXXXXXXXXXXXXXXXXXXXXXX", "unhandled")
		#
		# 	DanilatorService.convFinished(user, set = None)
		# 	user.conv.ongoing = False
		# else:
		# 	print("***continue conv!!!!!!!!!!!!!!!!!!")
		#
		if dbChanged:
			DanilatorService.backup()


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
		if userID in DanilatorService.users:
			user = DanilatorService.users[userID]
			if remID in user.reminders["unsent"]:
				rem = user.reminders["unsent"][remID]
				print("!!!!!!!",rem)
				if DanilatorService.actuallySend(userID,rem.message):
					if user.markSent(remID):
						if combID in DanilatorService.upcoming:
							DanilatorService.upcoming.pop(combID)
							DanilatorService.backup()
						else:
							print("EEEEEEEEE", "wasn't in upcoming")

					else:
						print("EEEEEEEEE", "could not mark!")

				else:
					print("EEEEEEEEE", "could not send!")



	def actuallySend(userID, message):
		print("TRY SENDING ON WHATSAPP! TO:", userID, "MESSAGE:", message)
		return DanilatorService.sendDelegate(userID,message)

		# return False #for errors

	def getRE(key):
		return re.compile(re.escape(key.lower()), re.IGNORECASE)


	def formatKnown(txt):
		for key in known:
			keyRE = DanilatorService.getRE(key)
			changed = keyRE.sub(known[key],txt)
			if txt != changed:
				print("-------CHANGED",txt,"TO",changed)
				txt = changed
		return txt

	def parseMsg(txt, tries = 0):
		print("============================")
		print(txt)
		formatted = DanilatorService.formatKnown(txt)
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
					new = DanilatorService.changeDay(formatted)
				else:
					new = formatted.replace(timestr,"in "+timestr)
				return DanilatorService.parseMsg(new, tries+1 )
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
			keyRE = DanilatorService.getRE(key)
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

		user = DanilatorService.users[userID]
		if user is None:
			print("user not found")
			return None

		user.remCount += 1
		remID = str(user.remCount)
		rem = Reminder(remID, userID, message, when)
		user.reminders["unsent"][remID] = rem
		user.lastRem = rem

		return rem
