# app.py
import os, sys, time
import json
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webwhatsapi import WhatsAPIDriver

from pprint import pprint

from ServiceImporter import *

# export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"

later = None
print(
'''
:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::
::::                         ::::
::::    WHATSAPP MASTER      ::::
::::                         ::::
:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::
'''
)

'''
Prep Vars
	DB

load services
Init - load WhatsApp
	wait for login
loadDB
backupDB

handle incoming
parse admin
isUserOrGroup
isFirst
? welcome

handle outgoing

'''
#
# class Service(object):
#
# 	def __init__(self) -> Service:
# 		pass
#
# 	'''process incoming message '''
# 	def runAsync(backupDelegate,sendDelegate) -> bool :
# 		pass
#
# 	def run() -> bool:
# 		pass
#
# 	def process(userID, message) -> bool:
# 		pass
#
#     def getDB() -> dict:
# 		pass
#
# 	def setDB(db) -> bool:
# 		pass
#
# 	def backup(backupDelegate) -> bool:
# 		pass
#
# 	def sendMsg(sendDelegate) -> bool:
# 		pass



runLocal = False
if runLocal:
	print(
	'''
	:::::::::::::::::::::::::::::::::
	::::    RUNNING LOCALLY      ::::
	:::::::::::::::::::::::::::::::::
	'''
	)
	print('export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"')


class Master(object):
	print(
	'''
	:::::::::::::::::::::::::::::::::
	:::::::::::::::::::::::::::::::::
	::::                         ::::
	::::     MASTER DRIVER       ::::
	::::                         ::::
	:::::::::::::::::::::::::::::::::
	:::::::::::::::::::::::::::::::::
	'''
	)
	shares = []

	''' DB init '''
	db = {
		"masters":["972512170493", "972547932000"],
		"users":{"id":{"services":{"groupID":None}}},
		"services":{"Reminders":{"dbID":None,"incomingTarget":None},"Proxy":{"dbID":None,"incomingTarget":None},"Danilator":{"dbID":None,"incomingTarget":None}},
		"groups": {"id":"service"},
		"id":"972547932000-1610379075@g.us"}

	serviceFuncs = {"services":{ "Reminder":None, "Proxy":None, "Danilator":None}}
	serviceGroupNames = {}

	serviceThreads = { }

	def LoadServices(self):
		# load list of services
		for service in self.db["services"]:


			if "reminders".lower() == service.lower():
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				ReminderService.go(sendDelegate=self.driver.sendMessage,backupDelegate=self.backupService)
				self.serviceFuncs["services"][service]=ReminderService.process
				self.serviceGroupNames[service] = "🔔 Reminders 🔔".encode('unicode-escape').decode('ASCII')


			if "danilator".lower() == service.lower():
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				print("FFFFFFFFFFFFFFFFFFFFFFFFFFF")
				DanilatorService.go(sendDelegate=self.driver.sendMessage,backupDelegate=self.backupService)
				self.serviceFuncs["services"][service]=DanilatorService.process
				self.serviceGroupNames[service] = "💚 Danilator 💚"

			try:
				if "dbID" not in self.db["services"][service]:
					self.db["services"][service]["dbID"] = None

				dbID = self.db["services"][service]["dbID"]
				''' create new db group '''
				if dbID is None:
					print("-------------------------------")
					print("     CREATING NEW DB GROUP   "+service)
					print("-------------------------------")
					groupName = service

					newGroup = self.driver.newGroup(newGroupName = service+"_DB", number = "+"+self.db["masters"][1], local = runLocal)
					newGroupID = newGroup.id
					self.db["services"][service]["dbID"] = newGroupID
					self.driver.sendMessage(newGroupID, '{"init":"TRUE"}')
					self.backup()
				else:
					print("-------------------------------")
					print("service: ",service,"  dbID: ",dbID)
					print("-------------------------------")

			except Exception as e:
				print(" ::: ERROR - LOAD SERVICES ::: ","\n",e,e.args,"\n")

	''' start master driver and log in '''
	def __init__(self, profileDir = "/app/session/rprofile2"):
		Master.shares.append(self)
		self.db = Master.db
		self.serviceFuncs = Master.serviceFuncs
		self.lastQR = 0
		self.runners = 0
		self.driver = None
		self.status = "INIT"

		asyncInit = Thread(target = self.initAsync,args = [profileDir])
		asyncInit.start()
		# return self

	def initAsync(self, profileDir = "/app/session/rprofile2"):

		''' init driver variables '''
		if len(Master.shares) > 1:
			profileDir += "-"+str(len(Master.shares))
		chrome_options = webdriver.ChromeOptions()
		chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
		chrome_options.add_argument("user-data-dir="+profileDir);
		chrome_options.add_argument('--profile-directory='+profileDir)

		if not runLocal:
			self.driver = WhatsAPIDriver(profile = profileDir, client='chrome', chrome_options=chrome_options,username="wholesomegarden")
		else:
			self.driver = WhatsAPIDriver(username="wholesomegarden",profile=None)
		driver = self.driver

		print(''' ::: waiting for login ::: ''')
		driver.wait_for_login()
		try:
			self.status = status = driver.get_status()
		except Exception as e:
			print(" ::: ERROR - Status Init ::: ","\n",e,e.args,"\n")

		''' preping for qr '''
		if status is not "LoggedIn":
			img = None
			triesCount = 0
			maxtries = 40

			while status is not "LoggedIn" and triesCount < maxtries:
				triesCount+=1

				print("-------------------------------")
				print("status:",status,"tries:",triesCount,"/",maxtries)
				print("-------------------------------")

				self.lastQR += 1
				try:
					img = driver.get_qr("static/img/QR"+str(self.lastQR)+".png")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
					print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",str(img)[17:130])

				except Exception as e:
					print(" ::: ERROR - QR Fetching ::: ","\n",e,e.args,"\n")

				# im_path = os.path.join("static/img/newQR.png")

				print(''' ::: rechecking status ::: ''')
				try:
					self.status = status = driver.get_status()
				except Exception as e :
					self.status = status = "XXXXXXXX"
					print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")

		if status is "LoggedIn":
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::   MASTER IS LOGGED IN!    ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			# if runLocal:
			# 	self.driver.save_firefox_profile(remove_old=False)

			''' load DB '''
			## overwrite to init db
			initOverwrite = False
			if initOverwrite:
				self.backup()
			# driver.updateDB(self.db,number=self.db["id"])
			lastDB = self.loadDB()
			self.db = lastDB
			self.db["init"] = time.time()
			self.db["backupInterval"] = 10*60
			if runLocal:
				self.db["backupInterval"] = 0

			self.db["backupDelay"] = 10
			if runLocal:
				self.db["backupDelay"] = 3

			self.db["lastBackup"] = 0
			self.db["lastBackupServices"] = 0
			self.backup()
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::     DATABASE LOADED       ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(self.db)
			print()

			''' Load Services '''
			# print("SSSSSSSSSSSSSSSSSSSSs")
			self.LoadServices()
			# print("SSSSSSSSSSSSSSSSSSSSs")

			''' process incoming '''
			process = Thread(target = self.ProcessIncoming, args=[None])
			process.start()
		else:
			print(" ::: ERROR - COULD NOT LOG IN  ::: ","\n")


	def loadDB(self, number = None):
		if number is None:
			number = self.db["id"]
		return self.driver.loadDB(number = number)


	def backupService(self,db = None, service = None):

		data = [db,service]
		# self.backupServiceAsync(data)
		bT = Thread(target = self.backupServiceAsync,args = [data])
		bT.start()

	def backupServiceAsync(self,data):
		time.sleep(self.db["backupDelay"])
		db, service = data
		print("SSSSSSSSS",service,db)
		if time.time() - self.db["lastBackupServices"] < self.db["backupInterval"]:
			return False

		if service is None or len(service) == 0:
			return None

		backupChat = None
		if service in self.db["services"]:
			chatID = self.db["services"][service]["dbID"]
			if chatID is not None:
				bchat = None
				try:
					bchat = self.driver.getChat(chatID)
				except Exception as e:
					print(" ::: ERROR - COULD NOT GET BACKUPCHAT"+e+" ::: ","\n")
				if bchat is not None:
					print("FFFFFFFFFFFFFFFUCKKK")
					# self.driver.sendMessage(chatID,"FFFFFFFFFFFFFFFUCKKK")

					backupChat = chatID
			else:
				print(" ::: ERROR - SERVICE HAS NO BACKUPCHAT"+" ::: ","\n")


		if backupChat is not None:
			if db is not None:
				return self.driver.updateDB(db,number=backupChat)
			else:
				return self.loadDB(backupChat)
		else:
			print(" ::: ERROR - BackupChat NOT FOUND for :"+service+": service ::: \n")
		self.db["lastBackupServices"] = time.time()



	def backup(self, now = None):
		bT = Thread(target = self.backupAsync,args = [now])
		bT.start()

	def backupAsync(self,data):
		now = data
		if now is None:
			time.sleep(self.db["backupDelay"])
			if time.time() - self.db["lastBackup"] < self.db["backupInterval"]:
				return False
		self.db["lastBackup"] = time.time()
		return self.driver.updateDB(self.db,number=self.db["id"])

	def ProcessServiceAsync(self, service, chatID, message):
		serviceT = Thread(target = self.ProcessService, args = [[service, chatID, message]])
		serviceT.start()

	def ProcessService(self, data):
		# try:
		service, chatID, text = data
		self.serviceFuncs["services"][service](chatID, text)
		# except Exception as e:
		# 	print(" ::: ERROR - Processing Service ::: ",serice,":::",chatID,":::",text,":::","\n",e,e.args,"\n")

	def ProcessIncoming(self, data):
		print(
		'''
		===================================
		    Processing Incoming Messages
		===================================
		'''
		)
		lastm = None
		loopc = 0
		delay = 0.5
		while True:
			# try:
			if True:
				if loopc % 20 == 0:
					''' ::: rechecking status ::: '''
					try:
						self.status = status = self.driver.get_status()
						print(" ::: status is",status,"::: ")
					except Exception as e:
						self.status = status = "XXXXXXXX"
						print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")


				''' all unread messages '''
				for contact in self.driver.get_unread():
					# print("MMMMMMMMMMXXX",contact)
					# print("MMMMMMMMMMXXX",contact)
					# print("MMMMMMMMMMXXX",contact)
					# print("MMMMMMMMMMXXX",contact)
					# print("MMMMMMMMMMXXX",contact)
					for message in contact.messages:
						print("MMMMMMMMMM",message)

						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						# pprint(vars(contact))
						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						# pprint(vars(message))
						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						# print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
						if runLocal:
							chatID = message.chat_id["_serialized"]
						else:
							chatID = message.chat_id
						try:
							chat = self.driver.get_chat_from_id(chatID)
						except Exception as e:
							print(" ::: ERROR - _serialized chatID ::: "+chatID+" ::: ","\n",e,e.args,"\n")

						''' incoming from: '''
						''' Personal Chat  '''
						senderName = message.get_js_obj()["chat"]["contact"]["formattedName"]
						senderID = message.sender.id
						fromGroup = False
						if "c" in chatID:
							print(
							'''
							===================================
							   Incoming Messages from '''+senderID+" "+senderName+'''
							===================================
							'''
							)
						# ''' Group Chat '''
						elif "g" in chatID:
							fromGroup = True
							print(
							'''
							===============================================
							   Incoming Messages from \"'''+senderID+" in "+senderName+'''\" GROUP
							===============================================
							'''
							)

						if message.type == "chat":
							text = message.content

							print("TTTTTXXXXXXXXXTTTTTTT",text)
							''' subscribe to service '''

							''' SENT FROM GROUP CHAT '''

							if "%%%!%%%" in text:

								print("YYYYYYYYYYYYYYYYYYYY")
								print("YYYYYYYYYYYYYYYYYYYY")
								print("YYYYYYYYYYYYYYYYYYYY")
								target = text.split(u"%%%!%%%")[1]
								self.driver.sendMessage(chatID,"Adding Service to DB: "+target)
								self.db["services"][target] = {"dbID":None,"incomingTarget":None}
								self.LoadServices()
								# self.serviceFuncs["services"][target] = None

								self.backup(now = True)
							else:
								print("XXXXXXXXXXXXXXXXXXX")
								print("XXXXXXXXXXXXXXXXXXX")
								print("XXXXXXXXXXXXXXXXXXX")



							if fromGroup is True:
								''' GOT REGISTRATION COMMAND '''
								if text[0] is "=":
									foundService = None
									target = text[1:]

									''' register group to service '''
									for service in self.db["services"]:
										if target.lower() == service.lower():
											foundService = service

											foundChat = False
											if chatID in self.db["groups"]:
												targetService = self.db["groups"][chatID]
												print("TTTTTTTTTTTTTTTTTTTT")
												print(targetService, service)
												if targetService is not None:
													if targetService.lower() == service.lower():
														foundChat = True
														self.driver.sendMessage(chatID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())

											if not foundChat:
												print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
												print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
												print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
												self.driver.sendMessage(chatID,"Subscribing to service: "+service)
												self.db["groups"][chatID] = service
												self.backup()

									if foundService is None:
										self.driver.sendMessage(chatID,"service: "+target+" Not Found")

								''' Chat is not registered first time'''
								if chatID not in self.db["groups"]:
									# print("SSSSSSSSSSSSSSSSSSSSSS")
									self.driver.sendMessage(chatID,"This chat is not registered with any service yet\nYou can register it by sending =service_name")
									# print("JJJJJJJJJJJJJJ")
									self.db["groups"][chatID] = None
									# print("SSSSSSSSSSSSSSSSSSSSSS")
									self.backup()
								elif self.db["groups"][chatID] is not None:
									''' Chat is known '''
									target = self.db["groups"][chatID]
									print("MMMMMMMMMMMMMMMM",target)
									''' adding new user to service from group'''

									foundService = None
									for service in self.db["services"]:
										if target.lower() == service.lower():
											foundService = service


											''' CHAT IS REGISTERED TO SERVICE! '''
											''' PROCESS INCOMNG MESSAGE in SERVICE '''
											if foundService is not None and text[0] is not "=":
												# self.driver.sendMessage(chatID,text+" ::: GONNA BE PROCESSED BY "+target)

												''' this is where the magic happens - send to service'''
												self.ProcessServiceAsync(service,chatID,text)



									if foundService is None:
										self.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)


								else:
									''' service is None '''
									self.driver.sendMessage(chatID,"You can register this chat by sending =service_name")



							elif text[0] is "=":
								''' person registering service with ='''
								target = text[1:]
								dbChanged = False

								''' check target service in db '''
								serviceFound = False
								for service in self.db["services"]:
									print("______________ ----------"+service)
									print("")
									if not serviceFound and target.lower() == service.lower():
										''' service found '''
										serviceFound = True

										if chatID not in self.db["users"]:
											self.db["users"][chatID] = {'services': {}}
											dbChanged = True
											''' first time user '''
											# self.db["users"][senderID] = {'services': {'Reminders': {'groupID': None}}}
										else:
											''' known user '''



										foundChat = None
										if service in self.db["users"][chatID]["services"]:

											serviceChat = self.db["users"][chatID]["services"][service]

											# self.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
											try:
												foundChat = self.driver.get_chat_from_id(serviceChat)
											except:
												print('chat could not be found')

										if foundChat is not None:
											check_participents = False
											if check_participents:
												if senderID in foundChat.get_participants_ids() or True:
													'''##### check that user is participant '''
													self.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
													self.driver.sendMessage(serviceChat,"subscirbed to: "+target)
												else:
													foundChat = None
											else:
												self.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
												self.driver.sendMessage(serviceChat,"subscirbed to: "+target)

										''' create new group '''
										if foundChat is None:
											groupName = service
											if service in self.serviceGroupNames:
												groupName = self.serviceGroupNames[service]

											newGroup = self.driver.newGroup(newGroupName = groupName, number = "+"+senderID.split("@")[0], local = runLocal)
											newGroupID = newGroup.id
											self.newG = newGroupID

											self.db["users"][chatID]['services'][service] = newGroupID
											self.db["groups"][newGroupID] = target
											dbChanged = True
											print(
											'''
											===============================================
											 ''' + senderID +" is NOW SUBSCRIBED TO "+ target +" :D "+'''
											===============================================
											'''
											)

								if not serviceFound:
									self.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)
									print(
									'''
									===============================================
									  SERVICE '''+ target +" IS NOT AVAILABLE"+'''
									===============================================
									'''
									)
								if dbChanged:
									self.backup()



						'''
						lastm = message
						print(json.dumps(message.get_js_obj(), indent=4))
						for contact in self.driver.get_contacts():
							# print("CCCC",contact.get_safe_name() )
							if  sender in contact.get_safe_name():
								chat = contact.get_chat()
								# chat.send_message("Hi "+sender+" !!!*"+message.content+"*")
						print()
						print()
						print(sender)
						print()
						print()
						print("class", message.__class__.__name__)
						print("message", message)
						print("id", message.id)
						print("type", message.type)
						print("timestamp", message.timestamp)
						print("chat_id", message.chat_id)
						print("sender", message.sender)
						print("sender.id", message.sender.id)
						print("sender.safe_name", message.sender.get_safe_name())
						if message.type == "chat":
							print("-- Chat")
							print("safe_content", message.safe_content)
							print("content", message.content)
							# Manager.process(message.sender.id,message.content)
							# contact.chat.send_message(message.safe_content)
						elif message.type == "image" or message.type == "video":
							print("-- Image or Video")
							print("filename", message.filename)
							print("size", message.size)
							print("mime", message.mime)
							print("caption", message.caption)
							print("client_url", message.client_url)
							message.save_media("./")
						else:
							print("-- Other type:",str(message.type))
						print("PROCESSING MESSAGE:",message)
						'''

			else:
				pass
			# except Exception as e:
			# 	print(" ::: ERROR - CHECKING MESSAGES ::: ","\n",e,e.args,"\n")

			loopc += 1; loopc = loopc % 120
			time.sleep(delay)

	def quit(self):
		self.driver.quit()

	def Nothing(data):
		print(":::Nothign::: DATA=",data)



''' running master '''
master = None
timeout = time.time()
maxtimeout = 30
# while master is None and time.time()-timeout < maxtimeout:
# try:
# # if True:
# 	# master = Master()
# 	# print("9999999999999999999999999999")
# 	# print("9999999999999999999999999999")
# 	# print("9999999999999999999999999999")
# 	# print("9999999999999999999999999999")
#
# 	maxtimeout = 0
#
# # else:
# # 	pass
# except Exception as e:
# 	print(" ::: ERROR - init Master ::: ","\n",e,e.args,"\n")



''' running front server '''
from flask import Flask, render_template, redirect

app = Flask(__name__,template_folder='templates')

qrfolder = os.path.join('static', 'img')
app.config['QR_FOLDER'] = qrfolder

''' setting referals '''
refs = {"yo":"https://api.WhatsApp.com/send?phone=+972512170493"}
refs["yoo"] = "https://web.WhatsApp.com/send?phone=+972512170493"

@app.route('/')
def hello_world():
	master = Master.shares[0]
	full_filename = os.path.join(app.config['QR_FOLDER'], "QR"+str(master.lastQR)+".png")
	if master.status == "LoggedIn":
		return render_template("loggedIn.html", user_image = full_filename, status = master.status)
	else:
		return render_template("index.html", user_image = full_filename, status = master.status)

@app.route('/<path:text>', methods=['GET', 'POST'])
def all_routes(text):
	if text in refs:
		return redirect(refs[text])
	else:
		return redirect("/")


#
# if __name__ == '__main__':
# 	print(
# 	'''
# 	===================================
# 		   Running Front Server
# 	===================================
# 	'''
# 	)
# 	app.run(debug=True, host='0.0.0.0',use_reloader=False)
# else:
# 	print("################################")
# 	print("################################")
# 	print("################################")
# 	print("################################")
# 	print("################################")
# 	print("################################")
#

def flaskRun(master):
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	global running
	# if reminder.runners < 1 and running < 1:
	if True:
		# running += 1
		# reminder.runners += 1
		t = Thread(target=flaskRunAsync,args=[master,])
		t.start()
	else:
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")


def flaskRunAsync(data):
	master = data
	# input()
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	master = Master()
	master = Master.shares[0]
	print("9999999999999999999999999999")
	print("9999999999999999999999999999")
	print("9999999999999999999999999999")
	print("9999999999999999999999999999")



if __name__ == '__main__':
	flaskRun(master)
	print("STARTING APP")
	# print("STARTING APP")
	# print("STARTING APP")
	# print("STARTING APP")
	# print("STARTING APP")
	if runLocal :
		pass
		app.run(debug=True, host='0.0.0.0',use_reloader=False)
	# app.run(debug=True, host='0.0.0.0',use_reloader=False)
else:
	flaskRun(master)
	# app.run(debug=True, host='0.0.0.0',use_reloader=False)
	print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")




'''
id = "0547772000"

# heroku logs -t -a whatsappreminder
# heroku ps:exec -a whatsappreminder

## import geckodriver
# https://www.askpython.com/python/examples/python-automate-facebook-login

# heroku config:set WEB_CONCURRENCY=1 -a whatsappreminder
# https://github.com/pyronlaboratory/heroku-integrated-firefox-geckodriver

# https://www.reddit.com/r/firefox/comments/h8s7qd/how_do_i_make_firefox_work_on_heroku/
# https://github.com/evosystem-jp/heroku-buildpack-firefox
# https://stackoverflow.com/questions/43713445/selenium-unable-to-find-a-matching-set-of-capabilities-despite-driver-being-in
# https://www.guru99.com/selenium-python.html

#
# msg = "send message to Omer tomorrow morning "
# Manager.process(id, msg)
#
#
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
print()
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!2")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!3")


msg = "call omer thursday morning"
# Manager.process(id, msg)

# export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"



#
# import wapy
#
# wapy.init()
# while True:
#     wapy.unread()
#     wapy.response('-wapy', 'text', text='Hello World!')
import os
import time
import json
import os
import sys

from QRMatrix import *

# from skimage import data, color
# from skimage.transform import rescale, resize, downscale_local_mean
from webwhatsapi import WhatsAPIDriver
# from skimage import io


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os

profileDir = "/app/session/rprofile2"

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
chrome_options.add_argument("user-data-dir="+profileDir);
chrome_options.add_argument('--profile-directory='+profileDir)
# print("AAAAAAAA")
# print()
driver1 = webdriver.Chrome(options = chrome_options, executable_path=os.environ.get("CHROMEDRIVER_PATH"))
# # driver1 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# #

# # print("BBBBBBBBBB")
print("================================")
print("================================")
print("================================")
print("================================")
print("================================")
print(" ")


driver1.get("https://accounts.random.org/")

# print(driver1.page_source)

try:
	block = driver1.find_element_by_id("account-overview-block")
	print("==========================")
	print(" LOGGED IN!!!!!!!!! A",block)
	print("==========================")
except:
	print("==========================")
	print(" NO BLOCK LOGGED OUT A ")
	print("==========================")


username = driver1.find_element_by_id("login-login")
password = driver1.find_element_by_id("login-password")
# btn   = driver1.find_element_by_css_selector("button.btn btn-primary")

username.send_keys("takeyo")
password.send_keys("12345678abcd")
password.send_keys(Keys.ENTER)
# Step 4) Click Login
time.sleep(5)
block = driver1.find_element_by_id("account-overview-block")


try:
	block = driver1.find_element_by_id("account-overview-block")
	print("==========================")
	print(" LOGGED IN!!!!!!!!! B",block)
	print("==========================")
except:
	print("==========================")
	print(" NO BLOCK LOGGED OUT B")
	print("==========================")


print(" ")
print("================================")
print("================================")
print("================================")
print("================================")
print(" ")
driver1.quit()

# driver.get("http://www.python.org")
# print("CCCCCCCCCC")

print("@@@@@@@@@@@@@@@@@@@@@@@@@@1")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@2")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@3")
# return False

running = 0

class Reminder(object):

	def __init__(self):
		self.lastQR = 0
		self.runners = 0
		self.driver = None
		self.status = "INIT"

	def quit(self):
		self.driver.quit()

	def runReminder(self):
		# driver = WhatsAPIDriver(firefox_binary="/app/vendor/firefox/firefox",executable_path='/app/vendor/geckodriver/geckodriver',username="wholesomegarden")
		profile = "/app/session/rprofile2"
		# profile = None
		driver = WhatsAPIDriver(profile = profile, client='chrome', chrome_options=chrome_options,username="wholesomegarden")
		# driver = WhatsAPIDriver(client='chrome', chrome_options=chrome_options,username="wholesomegarden")
		self.driver = driver

		# driver.driver.get("chrome://version")
		# print(str(driver.driver.page_source))
		# print("")

		print("@@@@@@@@@@@@@@@@@@@@@@@@@@4")
		print("@@@@@@@@@@@@@@@@@@@@@@@@@@5")
		print("@@@@@@@@@@@@@@@@@@@@@@@@@@6")

		print("####################")
		print("####################")
		print("####################")
		Manager.go(driver)
		print("MANAGER StarteD")
		print("####################")
		print("####################")
		print("####################")

		# driver.get_status()
		print("Waiting for Login")
		driver.wait_for_login()
		# print("Saving session")


		# from qrtools import qrtools
		# from PIL import Image
		# import zbarlight
		# qr = qrtools.QR()

		#
		# from PIL import Image

		# import os
		# import numpy as np
		# import pyboof as pb

		# # pb.init_memmap() #Optional
		#
		# class QR_Extractor:
		#     # Src: github.com/lessthanoptimal/PyBoof/blob/master/examples/qrcode_detect.py
		#     def __init__(self):
		#         self.detector = pb.FactoryFiducial(np.uint8).qrcode()
		#
		#     def extract(self, img_path):
		#         if not os.path.isfile(img_path):
		#             print('File not found:', img_path)
		#             return None
		#         image = pb.load_single_band(img_path, np.uint8)
		#         self.detector.detect(image)
		#         qr_codes = []
		#         for qr in self.detector.detections:
		#             qr_codes.append({
		#                 'text': qr.message,
		#                 'points': qr.bounds.convert_tuple()
		#             })
		#         return qr_codes


		# qr_scanner = QR_Extractor()

		print("AAA")
		c = 0
		s = 60
		maxtries = 40
		try:
			self.status = status = driver.get_status()
		except :
			self.status = status = "XXXXXXXX"
			print("STATUS ERROR XXX")
		img = None
		while status is not "LoggedIn" and c < maxtries:
			c+=1
			print("status", status)

			print("AAAAAAAAAAAAA")
			self.lastQR += 1
			try:
				img = driver.get_qr("static/img/QR"+str(self.lastQR)+".png")
			except :
				print("QR ERROR XXX")
			print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
			print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
			print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
			print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
			print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
			print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
			print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",str(img)[:100])
			# im_path = os.path.join("static/img/newQR.png")

			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",c,"/",maxtries)
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",c,"/",maxtries)
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",c,"/",maxtries)
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",c,"/",maxtries)

			# pathlib.Path().absolute()
			# os.system("cp newQR.png sample/static/img/newQR.png")

			# img = driver.get_qr("newQR.png")
			# from PIL import Image
			# print("BBBBBBBBBBBBBBB")
			# decoded = decode(Image.open(im_path))
			# print(decoded, "#######################")
			# print(decoded, "#######################")
			# print(decoded, "#######################")
			# print(decoded, "#######################")
			# print(decoded, "#######################")
			# print(decoded, "#######################")
			# print(decoded, "#######################")

			# for barcode in decoded:
			# 	print("@@@@@@@@@@@@@@@@@@@")
			# 			# the barcode data is a bytes object so if we want to draw it
			# 	# on our output image we need to convert it to a string first
			# 	# barcodeData = barcode.data.decode("utf-8")
			# 	# barcodeType = barcode.type
			# 	# # draw the barcode data and barcode type on the image
			# 	# text = "{} ({})".format(barcodeData, barcodeType)
			# 	print("@@@@@@@@@@@@@@@@@@@")
			# 	# print(text)
			# 	# printQR(barcodeData)
			# 	print("@@@@@@@@@@@@@@@@@@@XXXXXXXX")


			print("Checking qr, status", status)

			try:
				self.status = status = driver.get_status()
			except :
				self.status = status = "XXXXXXXX"
				print("STATUS ERROR XXX")			# output = qr_scanner.extract(img)
			# print(output,"!!!!!!!!!!!!!!!!WDIOUSICNOIUCJ)(Z*UCINJ)(ZP*DFJYUF)((P*SUD)(UASIDMUJ))")
			# print(qr.decode(img))
			# print(qr.data)

			# print("BBBB2")
			# with open(img, 'r+b') as f:
			#     with Image.open(f) as image:
			#         cover = resizeimage.resize_cover(image, [57, 57])
			#         cover.save(img, image.format)
			# #
			# qr.decode(img)
			# print (qr.data)
			# print(retval,"!!!!!!!!!!!!!!!!!!!")
			#
			# print("CCC",img)
			# obj.load_image_from_file(img)

			# obj.resize(s,s)
			# s-=1
			# print(obj)
			# obj.render(timg.Ansi24HblockMethod)
			# print("DDD",s,s,s,s)
			# time.sleep(10)
			# driver.save_firefox_profile(remove_old=False)
			# time.sleep(3)
			# try:
			#     driver.reload_qr()
			# except:
			#     print("refresh finised")
		print("Bot started")
		# driver.save_firefox_profile()

		# print("waiting for qr code")
		# img = driver.get_qr("static/img/newQR.png")
		# os.system("cp newQR.png static/img/newQR.png")

		# print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		# print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		# print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		# print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		# print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		# print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		# print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",str(img)[:100])
		# time.sleep(4)
		# QRCode = QRMatrix("decode", img)
		# print(QRCode.decode())
		print("@@@@@@@@@@@@@@@@@@@")
		print("DONEEEEEEEEEEEEEEEE")
		print("DONEEEEEEEEEEEEEEEE")
		print("DONEEEEEEEEEEEEEEEE")
		print("DONEEEEEEEEEEEEEEEE")
		print("DONEEEEEEEEEEEEEEEE")
		# # i = io.imread(img)
		# # image = color.rgb2gray(i)
		#
		# image_rescaled = rescale(image, 0.25, anti_aliasing=False)
		# io.imsave(img, image_rescaled)
		print("XXXXXXXXX")
		# import timg
		# obj = timg.Renderer()
		# obj.load_image_from_file(img)
		# obj.resize(106,106)
		# obj.render(timg.Ansi24HblockMethod)
		#
		#
		# for contact in driver.get_contacts():
		#     print("CCCC",contact.get_safe_name() )
		#     if  "@@@@@@@@@@@@@@@@@@@@@@@@@" in contact.get_safe_name():
		#         chat = contact.get_chat()
		#         chat.send_message("Hi Jack")

		lastm = None
		loopc = 0
		while True:
			loopc += 1
			loopc = loopc % 120
			time.sleep(.5)
			if loopc % 20 == 0:
				self.status = driver.get_status()
				print("Checking for more messages, status", self.status)
			for contact in driver.get_unread():
				for message in contact.messages:
					lastm = message
					print(json.dumps(message.get_js_obj(), indent=4))
					sender = message.get_js_obj()["chat"]["contact"]["formattedName"]
					for contact in driver.get_contacts():
						# print("CCCC",contact.get_safe_name() )
						if  sender in contact.get_safe_name():
							chat = contact.get_chat()
							chat.send_message("Hi "+sender+" !!!*"+message.content+"*")
					print()
					print()
					print(sender)
					print()
					print()
					print("class", message.__class__.__name__)
					print("message", message)
					print("id", message.id)
					print("type", message.type)
					print("timestamp", message.timestamp)
					print("chat_id", message.chat_id)
					print("sender", message.sender)
					print("sender.id", message.sender.id)
					print("sender.safe_name", message.sender.get_safe_name())
					if message.type == "chat":
						print("-- Chat")
						print("safe_content", message.safe_content)
						print("content", message.content)
						Manager.process(message.sender.id,message.content)
						# contact.chat.send_message(message.safe_content)
					elif message.type == "image" or message.type == "video":
						print("-- Image or Video")
						print("filename", message.filename)
						print("size", message.size)
						print("mime", message.mime)
						print("caption", message.caption)
						print("client_url", message.client_url)
						message.save_media("./")
					else:
						print("-- Other type:",str(message.type))
					print("PROCESSING MESSAGE:",message)



from flask import Flask, render_template, redirect
# app = Flask(__name__)
app=Flask(__name__,template_folder='templates')


import os
arr = os.listdir()
for a in arr:
	# print(a)
	pass
# input()

reminder = Reminder()










PEOPLE_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def hello_world():
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "QR"+str(reminder.lastQR)+".png")
	if reminder.status == "LoggedIn":
		return render_template("loggedIn.html", user_image = full_filename, status = reminder.status)
	else:
		return render_template("index.html", user_image = full_filename, status = reminder.status)


def flaskRun(reminder):
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	global running
	if reminder.runners < 1 and running < 1:
		running += 1
		reminder.runners += 1
		t = Thread(target=flaskRunAsync,args=[reminder,])
		t.start()
	else:
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
		print(runners,"!!!!!!!!!!!!!!!!!!!!!!!!!RUNNERS")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")
	print("AFTER GONNA RUN ASYNC")


def flaskRunAsync(data):
	reminder = data
	# input()
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	reminder.runReminder()


if __name__ == '__main__':
	flaskRun(reminder)
	print("STARTING APP")
	print("STARTING APP")
	print("STARTING APP")
	print("STARTING APP")
	print("STARTING APP")
	app.run(debug=True, host='0.0.0.0')
else:
	flaskRun(reminder)
	print("STARTING APP22222222222")
	print("STARTING APP22222222222")
	print("STARTING APP22222222222")
	print("STARTING APP22222222222")
	print("STARTING APP22222222222")
	print("STARTING APP22222222222")


# 4. In case the QR code expires, you can use the reload_qr function to reload it
# driver.reload_qr()
# driver.view_unread()
# driver.get_all_chats()
# 7. To send a message, get a Contact object, and call the send_message function with the message.
# <Contact Object>.send_message("Hello")
# 8. Sending a message to an ID, whether a contact or not.
# driver.send_message_to_id(id, message)
'''
