# Challenge18Service.py
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

known = {"morning":"at 08:00","afternoon":"at 16:00", "evening":"at 18:00", "in in":"in","at at":"at", "בבוקר":"08:00", "בצהריים":"12:00", "בערב":"18:00"}
days = "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(",")

# class Challenge18Service(Service):
class Challenge18Service():
	id = "Challenge18"
	name = "🙏🌍 Challenge18 🐋🌸 "
	welcome =  "*Welcome to 🙏🌍 Challenge18 🐋🌸* \n*שלחו* הודעה ואנחנו כבר נזכיר לכם :)"
	help = "Challenge18 help message"
	shortDescription = "Get your Challenge18 as whatsapp messages!"
	imageurl = "https://i.imgur.com/YdXGl4K.jpg"

	share = None

	# examples = {"example1":{"text":"","thumbnail":None, "answer":"This is awesome in 5 seconds"}, "example2":{"text":"","thumbnail":None, "answer":"להתקשר לברוך מחר בבוקר"}}
	examples = {}

	emojiValues = {1:["@🧡❤️💛💚💙💜🖤🤍🤎💔❣️💕💞💓💗💖💘💝💐🌷🌹🥀🌺🌸🌼🌻🪴🎍🍀☘️🌱🌿🌴🎋🍃🌳🌲🎄🌵"],
		2:["🍒"],
		3:["🌎🌍🌏🌐⚽👂🏃🏃‍♀️👟💸💵💴💶💷💰💳💎💲🤑📱🤳📲📞☎️📴📳📵💡🏐🏀🏈⚾🥎🎾🏉🎱🏓🥍🏏⛹️‍♀️⛹️🏌️‍♀️🏌️🥥🐜"],
		18:["🤹‍♀️🤹‍♂️🥇⌛"],
		10:["🎥"]}


	def __init__(self,db, api):
		Challenge18Service.share = self
		self.db = db
		self.api = api
		# if "upcoming" not in self.db or "dict" not in str(type(self.db["upcoming"])):
		# 	self.db["upcoming"] = {}
		# if "users" not in self.db:
		# 	self.db["users"] = {}

		self.id = Challenge18Service.id
		self.name = Challenge18Service.name
		self.welcome = Challenge18Service.welcome
		self.imageurl = Challenge18Service.imageurl
		# self.help = Challenge18Service.help


	def go(self):
		while(True):
			if "last2000" not in self.db:
				self.db["last2000"] = 0
			# if "upcoming" not in self.db or "dict" not in str(type(self.db["upcoming"])):
			# 	self.db["upcoming"] = {}
			if "users" not in self.db :
				self.db["users"] = {}

			''' UPDATE CHALLENGE DAYS '''
			''' SEND DAYLIES '''
			''' USER engagment '''

			''' check time after 20:00 '''

			passed2000 = time.time() - search_dates("20:00")[0][1].timestamp() > 0
			try:
				if passed2000 and time.time() - self.db["last2000"] > 60*60*23:
					self.db["last2000"] = time.time()
					for challenge in self.db["challenges"]:
						challenge["today"] += 1
			except :
				pass
			# passed2000 update day += 1


			# while len(self.db["upcoming"]) > 0:
			# 	key = self.db["upcoming"].pop(0)
			# 	origin, content = item
			# for key in list(self.db["upcoming"].keys()):
			# 	t = self.db["upcoming"][key]
			# 	if time.time()-t > 0:
			# 		userID,remID = key.split("_")
			# 		self.remind(userID, remID)
			# 	# self.api.backup(self.db)
			#
			#
			#
			# time.sleep(1)

	def prepUser(self, user, day):
		if "days" not in self.db["users"][user]:
			self.db["users"][user]["days"] =  {}
		if day not in self.db["users"][user]["days"]:
			self.db["users"][user]["days"][day] = 0
		if "score" not in self.db["users"][user]:
			self.db["users"][user]["score"] =  1

	def hasDay(self, msg):
		return False, -1, msg

	def emojiValue(self, char):
		''' get emoji values '''
		''' strip all characters '''

		for k in self.emojiValues:
			if char in self.emojiValues[k]:
				return k
		return 0

	def getScore(self, msg, max = 6):
		''' count hearts and emoji values '''

		# nmsg = ''.join(c for c in msg if c.isprintable())
		# if len(msg) != len(nmsg):
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		# 	msg = nmsg

		sum = 0
		for char in msg:
			print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",msg)
			print("x"+char+"x")
			sum += self.emojiValue(char)

		return len(msg)


	def rate(self,group, msg, user):
		challenge = None
		if group in self.db["challenges"]:
			challenge = self.db["challenges"][group]
			day = challenge["today"]
			isDay, d, m = self.hasDay(msg)
			if isDay:
				day = d
				msg = m

			''' max by day '''
			score = self.getScore(msg.replace(" ","").replace("❤️","@"), max = 6)
			self.prepUser(user, day)

			''' get score - later check by task'''
			self.db["users"][user]["score"] += score
			self.db["users"][user]["days"][day] += score

			''' for now just thankyou - later add custom message based on score / random '''
			sendBack = "*"+self.name+"*\n\n*Thank you! "+user.split("@")[0]+"\nyour current score is now "+str(self.db["users"][user]["score"])+"*"

			''' for now send directly to user - later in group '''
			self.api.send(user,sendBack) # send to user
			# self.api.send(group,sendBack) # send to user


	def process(self, info):
		origin, user, content = None, None, None
		if "origin" in info:
			origin = info["origin"]
		if "user" in info:
			user = info["user"]
		if "content" in info:
			content = info["content"]

		if "users" not in self.db:
			self.db["users"] = {}
		if "challenges" not in self.db:
			self.db["challenges"] = {"today":1}

		dbChanged = False

		userID = str(user)
		if userID not in self.db["users"]:
			self.db["users"][userID] = {}
			dbChanged = True
		if origin not in self.db["challenges"]:
			self.db["challenges"][origin] = {"today":1}
			dbChanged = True

		self.rate(origin, content,userID)

		user = self.db["users"][userID]

		if dbChanged:
			self.backup()
			# self.api.backup(self.db)

	def backup(self):
		self.api.backup(self.db)
		# self.api.backup({"upcoming":self.db["upcoming"],"users":User.usersToJSONusers(self.db["users"])})


	def updateDB(self, db):
		self.db = db

	def welcomeUser(self, origin):
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		if "users" not in self.db:
			self.db["users"] = {}
		if origin not in self.db["users"]:
			self.db["users"][origin] = origin
			self.backup()

		if "challenges" not in self.db:
			self.db["challenges"] = {}
		if origin not in self.db["challenges"]:

			today = datetime.date.today()
			if today == today + datetime.timedelta( (0-today.weekday()) % 7 ,weeks=0):
				day = today + datetime.timedelta( (0-today.weekday()) % 7 ,weeks=1)
			else:
				day = today + datetime.timedelta( (0-today.weekday()) % 7 ,weeks=0)

			day = (0 - today.weekday()) % 7
			if day is 0:
				day = -7
			else:
				day = -1 * day



			res = search_dates("next monday 20:00", add_detected_language=True)
			if res is not None:
				res= res[0][1]
			else:
				self.db["challenges"][origin] = {"today":1}
			dbChanged = True
