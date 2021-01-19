#Service.py
import time

class ExperimentalService(object):
	id = "Experimental"
	name = "🚀Experimental🚀"
	welcome = "Welcome to 🚀Experimental🚀 Service \nUsed for system experiments"
	help = "Experimental Experimental Experimental"
	imageurl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmaJKloEMiBpQRA9woJw4XnuWXCWeN2BO70w&usqp=CAU"
	shortDescription = "System Experiments 🧪"
	share = None

	examples = {"services":{"text":"Show Public Services","thumbnail":None}}

	def __init__(self,db, api, master):
		ExperimentalService.share = self

		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Experimental",ExperimentalService.share)
		self.db = db
		self.api = api
		self.master = master
		#
		# if "upcoming" not in self.db:
		# 	self.db["upcoming"] = []
		# if "users" not in self.db:
		# 	self.db["users"] = {}

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

		# if "users" not in self.db:
		# 	self.db["users"] = {}
		#
		# if user not in self.db["users"]:
		# 	self.db["users"][user] = user
		# 	self.api.send(origin, "WELCOME "+user)
		# 	self.backup()

		# sendBack = content
		#
		# withLink = True
		# if withLink:
		# 	answer = ":answerid:555"
		# 	myLink = self.api.genLink(origin, answer)
		# 	sendBack += "\n\n"+answer+":\n"+myLink

		# self.db["upcoming"].append([origin, sendBack])


		sendBack = content
		myLink = ""
		withLink = True
		if withLink:
			answer = content
			myLink = self.api.genLink(origin, answer, newLink = "a")
			sendBack += "\n\n"+answer+":\n"+myLink

		#
		self.master.driver.sendMessage(origin,sendBack)

		''' invite tests '''
		service = "Master"
		groupName = service
		myLink = "https://akeyo.io/w?join"

		path = None
		if service in self.master.services and "obj" in self.master.services[service] and self.master.services[service]["obj"] is not None:
			groupName = self.master.services[service]["obj"].name
			imageurl = self.master.services[service]["obj"].imageurl
			if imageurl is not None:
				path = self.master.download_image(service=service,pic_url=imageurl)
		if path is None:
			path = self.master.download_image()
		imagepath = path


		for service in self.master.services:
			text, thumb = self.master.inviteToService(service=service)
			print(text, thumb)
			self.master.sendMessage(origin, text, thumbnail = thumb)



	def backup(self):
		self.api.backup(self.db)

	def updateDB(self, db):
		self.db = db
		# self.db = User.jsonUsersToUsers(db)
