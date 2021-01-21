#Service.py
import time

class InnovationService(object):
	id = "Innovation"
	name = "✨Innovation✨"
	welcome = "Welcome to ✨WhatsappMaster Innovation Channel✨ !\nאם הגעתם כי יש לכם בקשה או רעיון, אם הגעתם כדי להשקיע, ואם החברה שלכם תשמח להשתמש בווטסאפ אצלה במערכת\nמוזמנים לכתוב לי ונדבר על זה!\nתודה רבה על התעניינות, באהבה גדולה,\nתמי"
	help = "send a message to get it back"
	imageurl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnPIAyp1vEo_mbJy_xyAC0fy4hSVA6tjLqrg&usqp=CAU"
	shortDescription = "יש לכם רעיון שיעבוד טוב בווטסאפ?! כתבי לי כאן"
	share = None

	examples = {}

	def __init__(self,db, api):
		InnovationService.share = self

		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Innovation",InnovationService.share)
		self.db = db
		self.api = api
		if "upcoming" not in self.db:
			self.db["upcoming"] = []
		if "users" not in self.db:
			self.db["users"] = {}

	def go(self):
		while(False):
			if "upcoming" not in self.db:
				self.db["upcoming"] = []
			if "users" not in self.db:
				self.db["users"] = {}

			while len(self.db["upcoming"]) > 0:
				item = self.db["upcoming"].pop(0)
				origin, content = item
				self.api.send(origin, content, thumnail = "test")
				# self.api.backup(self.db)

			time.sleep(1)

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

		if user not in self.db["users"]:
			self.db["users"][user] = user




	def backup(self):
		self.api.backup(self.db)

	def updateDB(self, db):
		self.db = db
		# self.db = User.jsonUsersToUsers(db)

	def welcomeUser(self, origin):
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
		if origin not in self.db["users"]:
			self.db["users"][origin] = origin
			self.backup()
