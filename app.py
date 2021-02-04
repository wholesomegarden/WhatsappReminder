# app.py
import os, sys, time
import errno
import traceback

import random
import string
import json
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webwhatsapi import WhatsAPIDriver

from pprint import pprint as pp

# from ServiceImporter import *

# export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"
# heroku config:set WEB_CONCURRENCY=1
# heroku config:add TZ="Asia/Jerusalem" -a whatsappreminder

from ServiceLoader import *
from MasterService import *

runLocal = False
production = False
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

# runLocal = True
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
	shares = []
	# groups {"service":target, "invite":groupInvite, "user":senderID, "link":self.master.newRandomID()}
	# db = {
	# 	"masters":["972512170493", "972547932000"],
	# 	"users":{"id":{"services":{"groupID":None}}},
	# 	"services":{"Reminders":{"dbID":None,"incomingTarget":None},"Proxy":{"dbID":None,"incomingTarget":None},"Danilator":{"dbID":None,"incomingTarget":None}},
	# 	"groups": {"id":"service"},
	# 	"id":"972547932000-1610379075@g.us"}

	# db = {'masters': ['972512170493', '972547932000'], 'system': ['972512170493', '972543610404'], 'users': {}, 'groups': {}, 'id': '972547932000-1610379075@g.us', 'lastBackup': 1611071801.4876792, 'init': 1611071653.7335632, 'backupInterval': 0, 'backupDelay': 3, 'lastBackupServices': 0, 'servicesDB': {'Echo': {'dbID': '972512170493-1610802351@g.us'}, 'Danilator': {'dbID': '972512170493-1610802360@g.us'}, 'Reminders': {'dbID': '972512170493-1610802365@g.us'}, 'Music': {'dbID': '972512170493-1610802370@g.us'}, 'Master': {'dbID': '972512170493-1610965551@g.us'}, 'Experimental': {'dbID': '972512170493-1611059017@g.us'}}, 'availableChats': {'Master': {'972512170493-1611068831@g.us': 'https://chat.whatsapp.com/GhTABLFn3Aq18MI89MFBU8', '972512170493-1611071667@g.us': 'https://chat.whatsapp.com/LGABshra2Wd8rpZ8AduhuX'}, 'Music': {'972512170493-1611071128@g.us': 'https://chat.whatsapp.com/G3VQkKSrsuZJ3OiRz3Iof9', '972512170493-1611071137@g.us': 'https://chat.whatsapp.com/JN4juvGVYbbLVOoehExtTY'}, 'Experimental': {'972512170493-1611059125@g.us': 'https://chat.whatsapp.com/GIUwJiF3iCg1vioSHkkkQ8', '972512170493-1611059200@g.us': 'https://chat.whatsapp.com/IZXOC41bg112sKwE5UcoQO'}}}

	# db = {'masters': ['972512170493', '972547932000'], 'system': ['972512170493', '972543610404'], 'users': {}, 'groups': {}, 'id': '972547932000-1610379075@g.us'}
	# mynumber = '972512170493'
	mynumber = '972584422646'
	operator = '972547932000'
	emptyNumber = '972543610404'
	db = {'masters': [mynumber, operator], 'system': [mynumber, emptyNumber], 'users': {}, 'groups': {}, 'id': '972584422646-1612438185@g.us'}

	 # 'lastBackup': 1611071801.4876792, 'init': 1611071653.7335632, 'backupInterval': 0, 'backupDelay': 3, 'lastBackupServices': 0, 'servicesDB': {'Echo': {'dbID': '972512170493-1610802351@g.us'}, 'Danilator': {'dbID': '972512170493-1610802360@g.us'}, 'Reminders': {'dbID': '972512170493-1610802365@g.us'}, 'Music': {'dbID': '972512170493-1610802370@g.us'}, 'Master': {'dbID': '972512170493-1610965551@g.us'}, 'Experimental': {'dbID': '972512170493-1611059017@g.us'}}, 'availableChats': {'Master': {'972512170493-1611068831@g.us': 'https://chat.whatsapp.com/GhTABLFn3Aq18MI89MFBU8', '972512170493-1611071667@g.us': 'https://chat.whatsapp.com/LGABshra2Wd8rpZ8AduhuX'}, 'Music': {'972512170493-1611071128@g.us': 'https://chat.whatsapp.com/G3VQkKSrsuZJ3OiRz3Iof9', '972512170493-1611071137@g.us': 'https://chat.whatsapp.com/JN4juvGVYbbLVOoehExtTY'}, 'Experimental': {'972512170493-1611059125@g.us': 'https://chat.whatsapp.com/GIUwJiF3iCg1vioSHkkkQ8', '972512170493-1611059200@g.us': 'https://chat.whatsapp.com/IZXOC41bg112sKwE5UcoQO'}}}

	services = {}
	links = {}
	runningSubscriptions = 0
	baseURL = "akeyo.io/w?"
	if production:
		baseURL = "akeyo.io/p?"
	else:
		print("::::::::::STAGING::::::::::::::")
	# availableChats = {}
	publicServices = ["Music","Danilator","Reminders","Stock", "Challenge18"]
	sendToAny = ["Challenge18"]

	''' start master driver and log in '''
	def __init__(self, profileDir = "/app/session/rprofile2"):
		Master.shares.append(self)
		self.db = Master.db
		# self.services = ServiceLoader.LoadServices(self)

		self.status = "INIT"
		self.lastQR = 0
		self.driver = None
		self.masterService = None

		self.runLocal = runLocal
		self.startBackup = False
		self.activity = False
		self.backupNow = False


		asyncInit = Thread(target = self.initAsync,args = [profileDir])
		asyncInit.start()

	def inviteToService(self, service = "Master" ,beta = " (Beta)", noImage = True, fromChat = None, public = False):
		if service in self.services and "obj" in self.services[service] and self.services[service]["obj"] is not None:

			print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSs",service)
			obj = self.services[service]["obj"]
			groupName = obj.name
			serviceInvite = "/"+service.lower()

			title = "Join  " + groupName
			desc = obj.shortDescription
			if "master" in service.lower():
				serviceInvite = ""
				# title += beta
			else:
				title += "  Service"

			# image = self.download_image(pic_url=obj.imageurl)
			text = ""
			link = "https://"+self.baseURL
			if not public and fromChat is not None and fromChat in self.db["groups"] and self.db["groups"][fromChat] is not None and "link" in self.db["groups"][fromChat] and self.db["groups"][fromChat]["link"] is not None:
				noImage = False
				text = "Join "+groupName+ beta
				link += self.db["groups"][fromChat]["link"] + "/="+service.lower()

			else:
				noImage = False
				text = "Enjoying "+groupName+ " ?!"
				link += "join" + serviceInvite
			text +="\n" + link
			if not fromChat:
				text +="\nShare it with friends you love!✨" + beta

			imageurl = obj.imageurl
			if noImage:
				imageurl = ""
			thumbnail = {"imageurl":imageurl,"title":title,"desc":desc,"link":link}

			print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSs",service,"text",text,"thumb",thumbnail)
			return text, thumbnail

		return None, None



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
			profileDir = "/"+"/".join(profileDir.split("/")[2:])+"L"
			chrome_options = webdriver.ChromeOptions()
			executable_path = "/home/magic/wholesomegarden/WhatsappReminder/chromedriver"
			binPath = "/usr/bin/google-chrome"
			profileDir = "/home/magic/wholesomegarden/WhatsappReminder"+profileDir

			print(binPath, executable_path)
			# input()
			chrome_options.binary_location = binPath
			# chrome_options.add_argument('incognito')
			# chrome_options.add_argument('headless')
			# chrome_options.add_argument("--headless")
			chrome_options.add_argument("--disable-dev-shm-usage")
			chrome_options.add_argument("--no-sandbox")
			chrome_options.add_argument("--window-size=1420,3600")
			chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
			# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
			# chrome_options.add_argument('user-agent={0}'.format(user_agent))
			chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US;q=0.9'})

			# chrome_options.add_argument("--user-agent=New User Agent")
			chrome_options.add_argument("user-data-dir="+profileDir);
			chrome_options.add_argument('--profile-directory='+profileDir+"rprofile2/Profile 1")
			self.driver = WhatsAPIDriver(profile = profileDir, client='chrome', chrome_options=chrome_options,username="wholesomegarden", binPath = binPath)

			# self.driver = webdriver.Chrome(executable_path,chrome_options=chrome_options)
			# self.driver = WhatsAPIDriver(username="wholesomegarden",profile=None)

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
				self.backup(now = True)
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
			# self.backup()
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::     DATABASE LOADED       ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(self.db)
			print()
			if "groups" in self.db:
				for group in self.db["groups"]:
					if "links" in self.db["groups"][group]:
						for link in self.db["groups"][group]["links"]:
							self.links[link] = self.db["groups"][group]["links"][link]

				print(''' :::::::::::::::::::::::::::::::::::: ''')
				print(''' :::::::::::::::::::::::::::::::::::: ''')
				print(''' ::::                           ::::: ''')
				print(''' ::::     LINKS LOADED          ::::: ''')
				print(''' ::::                           ::::: ''')
				print(''' :::::::::::::::::::::::::::::::::::: ''')
				print(''' :::::::::::::::::::::::::::::::::::: ''')
				print(self.links)
				print()

			# if "availableChats" in self.db:
			# 	for group in self.db["groups"]:
			# 		if "links" in self.db["groups"][group]:
			# 			for link in self.db["groups"][group]["links"]:
			# 				self.links[link] = self.db["groups"][group]["links"][link]
			#
			# 	print(''' :::::::::::::::::::::::::::::::::::: ''')
			# 	print(''' :::::::::::::::::::::::::::::::::::: ''')
			# 	print(''' ::::                           ::::: ''')
			# 	print(''' ::::  AVAILABLE CHATS LOADED   ::::: ''')
			# 	print(''' ::::                           ::::: ''')
			# 	print(''' :::::::::::::::::::::::::::::::::::: ''')
			# 	print(''' :::::::::::::::::::::::::::::::::::: ''')
			# 	print(self.links)
			# 	print()

			self.services = ServiceLoader.LoadServices(send = self.send, backup = self.backupService, genLink = self.genLink, master = self)
			self.initServicesDB()
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' ::::     SERVICES LOADED       ::::: ''')
			print(''' ::::                           ::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(''' :::::::::::::::::::::::::::::::::::: ''')
			print(self.services)
			print()
			#
			# ''' Load Services '''
			# # print("SSSSSSSSSSSSSSSSSSSSs")
			# self.LoadServices()
			# # print("SSSSSSSSSSSSSSSSSSSSs")
			''' RUNNING MASTER SERVICE '''
			self.masterService = MasterService.share #MasterService(runLocal, self)

			''' process incoming '''
			process = Thread(target = self.ProcessIncoming, args=[None])
			process.start()

			''' check available groups '''
			process2 = Thread(target = self.checkAvailableGroups, args=[None])
			process2.start()
		else:
			print(" ::: ERROR - COULD NOT LOG IN  ::: ","\n")


	def checkAvailableGroups(self,data):
		minAvailable = 2
		while(True):
			if "availableChats" not in self.db:
				self.db["availableChats"] = {}

			# print("AVAILABLE GROUPS",self.db["availableChats"])
			goBackup = False
			# pp(self.db["availableChats"])
			try:
				for service in self.services:
					if service not in self.db["availableChats"]:
						self.db["availableChats"][service] = {}

					for chat in self.db["availableChats"][service]:
						delChat = None
						try:
							participants = self.driver.group_get_participants_ids(chat)
						except:
							delChat = chat
							traceback.print_exc()
						# pp(["PPPPPPPPPPPPP",participants])
						if delChat is None:
							# print("CHAT",chat,"PARTICIPANTS",participants)
							newParticipant = None

							for participant in participants:
								# print(participant)
								chatID = ""
								try:
									if runLocal and False:
										chatID = participant["_serialized"]
									else:
										chatID = participant
								except:
									try:
										chatID = participant["user"]+"@c.us"
									except:
										pass
								# print("CCCCCCCCCCCC",chatID)
								if chatID is not "" and chatID.split("@")[0] not in self.db["system"]:
									print("CCCCCCCCCCCC",chatID)
									newParticipant = chatID

							if newParticipant is not None:
								print("NEEEEEEWWWWWWW USSERRRRR IN GROUUUP")
								print("NEEEEEEWWWWWWW USSERRRRR IN GROUUUP")
								print("NEEEEEEWWWWWWW USSERRRRR IN GROUUUP")
								print("NEEEEEEWWWWWWW USSERRRRR IN GROUUUP")
								print("NEEEEEEWWWWWWW USSERRRRR IN GROUUUP",participant)

								firstKey = list(self.db["availableChats"][service])[0]
								newGroupID = firstKey
								invite = self.db["availableChats"][service].pop(firstKey)

								# service = "Master"
								if newParticipant not in self.db["users"]:
									self.db["users"][newParticipant] = {}

								link = self.newRandomID()
								self.db["users"][newParticipant][service] = newGroupID
								self.db["groups"][newGroupID] = {"service":service, "invite":invite, "link":link, "user":newParticipant, "links":{}}
								#
								# if "links" not in self.db["groups"][target]:
								# 	self.db["groups"][target]["links"] = {}
								#
								linkDataGroup = {"service":service, "chatID":newGroupID, "answer":"", "invite":invite, "user":newParticipant}
								self.db["groups"][newGroupID]["links"][link] = linkDataGroup
								self.links[link] = linkDataGroup

								print(newParticipant," IS NOW REGISTED",firstKey,invite)

								# chatName = self.master.services[service]["obj"].name
								# welcome = "Thank you for Subscribing to "+chatName
								welcome = self.services[service]["obj"].welcome #A
								obj = None
								if "obj" in self.services[service]:
									obj = self.services[service]["obj"]

								toAdd = ""
								if obj is not None:
									# self.setGroupIcon(newGroupID, obj.imageurl)

									if len(obj.examples) > 0:
										toAdd += "\n\n"
										toAdd += "See Examples: (click the link or type)\n"
										for example in obj.examples:
											key = example
											answer = key
											text = ""
											if "answer" in obj.examples[key]:
												answer = obj.examples[key]["answer"]
											if "text" in obj.examples[key]:
												text = obj.examples[key]["text"]
											toAdd += "*"+answer+"* : "+text+"\n"
											toAdd += self.baseURL + link +"/"+key + "\n\n"
									obj.welcomeUser(newGroupID)
								self.driver.sendMessage(newGroupID, welcome+toAdd)
								goBackup = True
								self.runningSubscriptions-=1
						else:
							self.db["availableChats"][service].pop(delChat)
							goBackup = True

				for service in self.db["availableChats"]:
					if len(self.db["availableChats"][service]) < minAvailable:
						self.masterService.createGroup([None,None,None], service = service)


			except Exception as e:
				print("EEEEEEEEEEEEEEEE checking available groups",e)
				traceback.print_exc()

			if goBackup:
				self.backup(now = True)

			time.sleep(1)

	def makeDirs(self, filename):
		if not os.path.exists(os.path.dirname(filename)):
		    try:
		        os.makedirs(os.path.dirname(filename))
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise

	def setGroupIcon(self, group_id, imageurl):
		print("SETTING GROUP ICON!")
		imagepath = self.download_image(pic_url=imageurl)
		return self.driver.groupIcon(group_id, imagepath)

		# res = self.driver.set_group_icon(group_id, imagepath)
		base64 = image = self.driver.convert_to_base64(imagepath,is_thumbnail=True, hardresize=True)
		code = "WAPI.setGroupIcon('"+group_id+"', '"+base64+"')"
		res = self.driver.driver.execute_script(script = code)
		# self.driver.execute_script(script=code)
		print("SETTING GROUP ICON! SET",str(res))


	def download_image(self, service="test", pic_url="https://img-authors.flaticon.com/google.jpg", img_name = 'thumnail.jpg'):
		if  pic_url is None:
			return ""
		if service is None or img_name is None:
			return None
		if pic_url is "":
			return pic_url

		final_path = service+"/"+img_name
		self.makeDirs(final_path)
		with open(final_path, 'wb') as handle:
		        response = requests.get(pic_url, stream=True)
		        if not response.ok:
		            print(response)
		        for block in response.iter_content(1024):
		            if not block:
		                break
		            handle.write(block)

		return os.path.abspath(final_path)


	def sendMessage(self, chatID, content, thumbnail = None, service = "test"):
		if thumbnail is not None:
			imageurl = "https://media1.tenor.com/images/7528819f1bcc9a212d5c23be19be5bf6/tenor.gif"
			title = "AAAAAAAAAA"
			desc = "BBBBBBB"
			link = imageurl
			path = ""

			sendAttachment = False
			if "imageurl" in thumbnail:
				if thumbnail["imageurl"] is None:
					thumbnail["imageurl"] = ""
					imageurl = ""
				else:
					imageurl = thumbnail["imageurl"]
				path = self.download_image(service = service, pic_url=imageurl)
				print("PPPPPPPPPPPPPPPPPPP",path)
				if "title" in thumbnail and thumbnail["title"] is not None:
					title = thumbnail["title"]
					if "desc" in thumbnail and thumbnail["desc"] is not None:
						desc = thumbnail["desc"]
						if "link" in thumbnail and thumbnail["link"] is not None:
							link = thumbnail["link"]
							sendAttachment = True

			if sendAttachment:
				res = self.driver.send_message_with_thumbnail(path,chatID,url=link,title=title,description=desc,text=content)
				print(res)
				print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT", path, "LINK",link,"TEXT",content)
				return res

		return self.driver.sendMessage(chatID, content)

	def send(self, api, service, target, content, thumnail = None):
		sendThread = Thread(target = self.sendAsync, args = [[api, service, target, content, thumnail]])
		sendThread.start()
		return True


	#UX WELCOME AFTER SUBSCIBING TO
	def sendAsync(self, data):
		api, service, target, content, thumbnail = data
		print("!!!!!!!!!!!!")
		if service in self.services:
			if self.services[service]["api"] is api:
				targetIsService = False
				subscribed = target in self.db["groups"] and "service" in self.db["groups"][target] and service.lower() == self.db["groups"][target]["service"].lower()
				if service in self.sendToAny:
					subscribed = True
				if len(target.split("/")) > 1 and len(target.split("/")[0]) > 0 and len(target.split("/")[1]) > 0:
					if target.split("/")[0] in self.services:
						targetService = target.split("/")[0]
						link = "/".join(target.split("/")[1:])
						if "obj" in self.services[targetService]:
							obj = self.services[targetService]["obj"]
							if obj is not None:
								#Get Nicknames
								self.ProcessServiceAsync(obj,{"origin":service+"/"+link, "user":link, "content":content})

				elif subscribed:
					print("THUMB")
					print("THUMB")
					print("THUMB")
					print("THUMB")
					print("THUMB")
					print(thumbnail)
					return self.sendMessage(target, content, thumbnail=thumbnail, service = service)




	def Process(self,contact):
		for message in contact.messages:
			print("MMMMMMMMMM",message.content)

			if runLocal and False: ## FOR FIREFOX
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

				''' SEND TO MASTER SERVICE '''
				self.masterService.ProcessChat(message)

				# self.driver.remove_participant_group()
				# if message.type == "chat":
				# 	text = message.content
				#
				# 	print("TTTTTXXXXXXXXXTTTTTTT",text)
				# 	''' subscribe to service '''
				#
				# 	''' SENT FROM GROUP CHAT '''
				#
				# 	if "%%%!%%%" in text:
				# 		target = text.split(u"%%%!%%%")[1]
				# 		self.driver.sendMessage(chatID,"Adding Service to DB: "+target)
				# 		self.db["services"][target] = {"dbID":None,"incomingTarget":None}
				# 		ServiceLoader.LoadService(service = target, send = self.send, backup = self.backupService, genLink = self.genLink)
				# 		# self.LoadServices()
				# 		# self.serviceFuncs["services"][target] = None
				#
				# 		self.backup(now = True)
				# 	else:
				# 		print("XXXXXXXXXXXXXXXXXXX")
				# 		print("XXXXXXXXXXXXXXXXXXX")
				# 		print("XXXXXXXXXXXXXXXXXXX")
				#
				# 	if text[0] is "/":
				# 		# "//div[@class='VPvMz']/div/div/span[@data-testid='menu']"
				# 		print("##################################")
				# 		print("##################################")
				# 		print("#####                      #######")
				# 		print("##################################")
				# 		print("##################################", text)
				# 		dotsSide = self.driver.tryOut(self.driver.driver.find_element_by_xpath,text,click=True)
				#
				# 	if text[0] is "-":
					# 	''' person unsubscribing service with -'''
					# 	target = text[1:]
					# 	dbChanged = False
					# 	now = False
					#
					# 	''' check target service in db '''
					# 	serviceFound = False
					# 	for service in self.services:
					# 		print("______________ ----------"+service)
					# 		print("")
					# 		if not serviceFound and target.lower() == service.lower():
					# 			target = service
					#
					# 			''' service found '''
					# 			serviceFound = True
					#
					# 			if chatID not in self.db["users"]:
					# 				self.db["users"][chatID] = {}
					# 				dbChanged = True
					# 				''' first time user '''
					# 				# self.db["users"][senderID] = {'services': {'Reminders': {'groupID': None}}}
					# 			else:
					# 				pass
					# 				''' known user '''
					#
					#
					# 			foundChat = None
					# 			if chatID in self.db["groups"]:
					# 				if "service" in self.db["groups"][chatID]:
					# 					self.db["groups"][chatID]["service"] = None
					#
					# 			if service in self.db["users"][chatID]:
					# 				serviceChat = self.db["users"][chatID][service]
					#
					# 				# self.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
					# 				if serviceChat is not None:
					# 					try:
					# 						self.db["users"][chatID].pop(service)
					# 						self.driver.sendMessage(chatID,"Unsubscribing from: *"+service+"*")
					# 						print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
					# 						print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
					# 						print("UUUUUUU    UNSUBSCRIBING       UUUUUUUUUUUU")
					# 						print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
					# 						print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
					# 						print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",chatID,service)
					# 						dbChanged = True
					# 						now = True
					#
					# 					except:
					# 						print('chat could not be found')
					# 	if not serviceFound:
					# 		self.driver.sendMessage(chatID,"you are not subscirbed to: *"+service+"*")
					#
					#
					# if text[0] is "=":
					# 	''' person registering service with ='''
					# 	target = text[1:]
					# 	dbChanged = False
					# 	now = False
					#
					# 	''' check target service in db '''
					# 	serviceFound = False
					#
					# 	serviceChat = ""
					# 	for service in self.services:
					# 		print("______________ ----------"+service)
					# 		print("")
					# 		if not serviceFound and target.lower() == service.lower():
					# 			target = service
					#
					# 			''' service found '''
					# 			serviceFound = True
					#
					# 			if chatID not in self.db["users"]:
					# 				self.db["users"][chatID] = {}
					# 				dbChanged = True
					# 				''' first time user '''
					# 				# self.db["users"][senderID] = {'services': {'Reminders': {'groupID': None}}}
					# 			else:
					# 				pass
					# 				''' known user '''
					#
					#
					# 			foundChat = None
					# 			if service in self.db["users"][chatID]:
					#
					# 				serviceChat = self.db["users"][chatID][service]
					#
					# 				# self.driver.sendMessage(senderID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
					# 				if serviceChat is not None:
					# 					try:
					# 						foundChat = self.driver.get_chat_from_id(serviceChat)
					# 					except:
					# 						print('chat could not be found')
					#
					#
					# 			chatName = target
					# 			welcome = "Thank you for Subscribing to "+target
					# 			try:
					# 				chatName = self.services[service]["obj"].name
					# 				welcome = "Thank you for Subscribing to "+chatName
					# 				welcome = self.services[service]["obj"].welcome
					# 			except:
					# 				pass
					#
					# 			if foundChat is not None:
					# 				check_participents = False
					# 				if check_participents:
					# 					if senderID in foundChat.get_participants_ids() or True:
					# 						'''##### check that user is participant '''
					# 						self.driver.sendMessage(senderID,"You are already subscirbed to: "+chatName+" \nYou can unsubscribe with -"+target.lower())
					# 						self.driver.sendMessage(serviceChat,"subscirbed to: "+chatName)
					# 					else:
					# 						foundChat = None
					# 				else:
					# 					gotLink = False
					# 					groupName = service
					# 					path = self.download_image()
					# 					inviteLink = ""
					#
					# 					print("$$$$$$$$$$$$$$$$$$$$$$$")
					# 					print(serviceChat, self.db["groups"][serviceChat]  )
					# 					if serviceChat in self.db["groups"] and self.db["groups"][serviceChat] is not None and "invite" in self.db["groups"][serviceChat]:
					# 						if self.db["groups"][serviceChat]["invite"] is not None:
					# 							inviteLink = self.db["groups"][serviceChat]["invite"]
					# 							gotLink = True
					# 							if service in self.services and "obj" in self.services[service] and self.services[service]["obj"] is not None:
					# 								groupName = self.services[service]["obj"].name
					# 								imageurl = self.services[service]["obj"].imageurl
					# 								if imageurl is not None:
					# 									path = self.download_image(service=service,pic_url=imageurl)
					#
					#
					# 					content = "You are already subscirbed to:\n"+chatName+" \n"
					# 					if gotLink:
					# 						content+= inviteLink
					# 					content+="\n"+"You can unsubscribe with -"+target.lower()
					#
					# 					if gotLink:
					# 						res = self.driver.send_message_with_thumbnail(path,senderID,url=inviteLink,title="Open  "+groupName,description="xxx",text=content)
					# 					else:
					# 						self.driver.sendMessage(senderID,content)
					# 					self.driver.sendMessage(serviceChat,"subscirbed to: "+chatName)
					#
					#
					# 			''' create new group '''
					# 			if foundChat is None:
					# 				print(
					# 				'''
					# 				===============================================
					# 				 ''' + senderID +" CREATING NEW GROUP "+ target +" :D "+'''
					# 				===============================================
					# 				'''
					# 				)
					# 				groupName = service
					# 				path = self.download_image()
					# 				if service in self.services and "obj" in self.services[service] and self.services[service]["obj"] is not None:
					# 					groupName = self.services[service]["obj"].name
					# 					imageurl = self.services[service]["obj"].imageurl
					# 					if imageurl is not None:
					# 						path = self.download_image(service=service,pic_url=imageurl)
					#
					#
					#
					# 				imagepath = path
					# 				newGroup, groupInvite = self.driver.newGroup(newGroupName = groupName, number = "+"+senderID.split("@")[0], local = runLocal, image=imagepath)
					# 				newGroupID = newGroup.id
					#
					# 				self.newG = newGroupID
					#
					# 				self.db["users"][chatID][service] = newGroupID
					# 				self.db["groups"][newGroupID] = {"service":target, "invite":groupInvite}
					# 				dbChanged = True
					# 				now = True
					# 				print(
					# 				'''
					# 				===============================================
					# 				 ''' + senderID +" is NOW SUBSCRIBED TO "+ target +" :D "+'''
					# 				===============================================
					# 				'''
					# 				)
					#
					# 				res = self.driver.send_message_with_thumbnail(path,senderID,url=groupInvite,title="Open  "+groupName,description="BBBBBBBB",text="Thank you! you are now subscribed to: "+chatName+" \n"+str(groupInvite)+"\nPlease check your new group :)")
					# 				# self.driver.sendMessage(senderID,"Thank you! you are now subscribed to: "+chatName+" \n"+str(groupInvite)+"\nPlease check your new group :)")
					# 				self.driver.sendMessage(newGroupID,welcome)
					# 				# self.driver.sendMessage(serviceChat,"subscirbed to: "+target)
					#
					# 	if not serviceFound:
					# 		self.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)
					# 		print(
					# 		'''
					# 		===============================================
					# 		  SERVICE '''+ target +" IS NOT AVAILABLE"+'''
					# 		===============================================
					# 		'''
					# 		)
					# 	if dbChanged:
					# 		self.backup(now=now)
					#

			# ''' Group Chat '''
			elif "g" in chatID:
				fromGroup = True
				print(
				'''
				===============================================
				   Incoming Messages in Group \"'''+senderName+" from "+senderID+'''
				===============================================
				'''
				)
				if message.type == "chat":
					text = message.content



					# ''' GOT REGISTRATION COMMAND '''
					# if text[0] is "=":
					# 	foundService = None
					# 	target = text[1:]
					#
					# 	''' register group to service '''
					# 	for service in self.services:
					# 		if target.lower() == service.lower():
					# 			foundService = service
					#
					# 			foundChat = False
					# 			if chatID in self.db["groups"]:
					# 				if "service" not in self.db["groups"][chatID]:
					# 					invite = None
					# 					if "invite" in self.db["groups"][chatID]:
					# 						invite = self.db["groups"][chatID]["invite"]
					# 					link = None
					# 					if "link" in self.db["groups"][chatID]:
					# 						link = self.db["groups"][chatID]["link"]
					# 					self.db["groups"][chatID] = {"service":service,"invite":invite, "link":link}
					#
					# 				targetService = self.db["groups"][chatID]["service"]
					# 				print("TTTTTTTTTTTTTTTTTTTT")
					# 				print(targetService, service)
					# 				if targetService is not None:
					# 					if targetService.lower() == service.lower():
					# 						foundChat = True
					# 						self.driver.sendMessage(chatID,"You are already subscirbed to: "+target+" \nYou can unsubscribe with -"+target.lower())
					#
					# 			if not foundChat:
					# 				print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
					# 				print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
					# 				print("SSSSSSSSSSSSSSSSSSSSSSsxxxxx")
					# 				self.driver.sendMessage(chatID,"Subscribing to service: "+self.services[service]["obj"].name)
					# 				self.driver.sendMessage(chatID,self.services[service]["obj"].welcome)
					# 				link = self.genLink(api = self.services[service]["api"],service=service,chatID=chatID,answer="")
					# 				self.db["groups"][chatID] = {"service":service, "invite":None, "link":link}
					# 				self.backup()
					#
					# 	if foundService is None:
					# 		self.driver.sendMessage(chatID,"service: "+target+" Not Found")

					''' Chat is not registered first time'''
					if chatID not in self.db["groups"]:
						# print("SSSSSSSSSSSSSSSSSSSSSS")
						self.driver.sendMessage(chatID,"This chat is not registered with any service yet\nYou can register it by sending =service_name")
						# print("JJJJJJJJJJJJJJ")
						self.db["groups"][chatID] = {"service":None, "invite":None, "link":None}
						# print("SSSSSSSSSSSSSSSSSSSSSS")
						self.backup()

					if self.db["groups"][chatID] is not None:
						''' Chat is known '''
						if "service" not in self.db["groups"][chatID]:
							invite = None
							if "invite" in self.db["groups"][chatID]:
								invite = self.db["groups"][chatID]["invite"]
							# self.db["groups"][chatID] = {"service":self.db["groups"][chatID],"invite":invite}
							link = None
							if "link" in self.db["groups"][chatID]:
								link = self.db["groups"][chatID]["link"]
							self.db["groups"][chatID] = {"service":None,"invite":invite, "link":link}
							self.driver.sendMessage(chatID,"This chat is not registered with any service yet\nYou can register it by sending =service_name")

						target = self.db["groups"][chatID]["service"]
						print("MMMMMMMMMMMMMMMM",target)

						if target is not None:
							foundService = None
							for service in self.services:
								if target.lower() == service.lower():
									foundService = service

									''' CHAT IS REGISTERED TO SERVICE! '''
									''' PROCESS INCOMNG MESSAGE in SERVICE '''
									if foundService is not None:

										''' this is where the magic happens - send to service'''

										if "obj" in self.services[foundService]:
											obj = self.services[foundService]["obj"]
											if obj is not None:
												#Get Nicknames
												self.ProcessServiceAsync(obj,{"origin":chatID, "user":senderID, "content":text})
												# obj.process({"origin":chatID, "user":senderID, "content":text})

										# self.ProcessServiceAsync(service,chatID,text)


							if foundService is None:
								self.driver.sendMessage(chatID,target+" : is not recognized as a service "+target)


	def processAsync(self, data):
		contact = data
		if contact is not None:
			self.Process(contact)

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
		delay = 0.25
		while True:
			# try:
			if True:
				if loopc % 40 == 0:
					''' ::: rechecking status ::: '''
					try:
						self.status = status = self.driver.get_status()
						print(" ::: status is",status,"::: ")
					except Exception as e:
						self.status = status = "XXXXXXXX"
						print(" ::: ERROR - Status Fetching ::: ","\n",e,e.args,"\n")


				''' all unread messages '''
				for contact in self.driver.get_unread():
					inThread = False
					if inThread:
						cThread = Thread(target=self.processAsync, args = [contact])
						cThread.start()
					else:
						self.Process(contact)


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

	def initServicesDB(self, service = None):
		check = self.services
		if service is not None:
			check = [service]
		for service in check:
			# try:
			if True:
				if "servicesDB" not in self.db:
					self.db["servicesDB"] = {}

				if service not in self.db["servicesDB"]:
					self.db["servicesDB"][service] = {}

				if "dbID" not in self.db["servicesDB"][service]:
					self.db["servicesDB"][service]["dbID"] = None

				dbID = self.db["servicesDB"][service]["dbID"]
				''' create new db group '''
				db = {}
				if dbID is not None:
					try:
						db = self.loadDB(dbID)
					except:
						db = None
						traceback.print_exc()

					if db is None:
						db = {}
						dbID = None

				if dbID is None:
					print("-------------------------------")
					print("     CREATING NEW DB GROUP   "+service)
					print("-------------------------------")
					groupName = service

					# if "masters" not in self.db:
						# self.db["masters"] =
					newGroupID,invite = self.driver.newGroup(newGroupName = service+"_DB", number = "+"+self.db["masters"][1], local = runLocal)
					# print(newGroup)
					# if "tuple" in str(type(newGroup)):
					# 	newGroup = newGroup[0]
					# print(newGroup)
					# newGroupID = newGroup.id
					self.db["servicesDB"][service]["dbID"] = newGroupID
					db = {"init":True}
					self.backup()
					self.driver.sendMessage(newGroupID, json.dumps(db))
					if service is not None:
						return newGroupID


				print("-------------------------------")
				print("service: ",service,"  dbID: ",dbID)
				print("-------------------------------")
				print(db)
				# while()
				self.services[service]["obj"].updateDB(db)

			# except Exception as e:
			else:
				print(" ::: ERROR - LOAD SERVICES ::: ","\n",e,e.args,"umbm\n")

	def loadDB(self, number = None):
		if number is None:
			if "id" not in self.db or self.db["id"] is None:
				newGroupID,invite = self.driver.newGroup(newGroupName = "DB", number = "+"+self.db["masters"][1], local = runLocal)

				code = "WAPI.removeParticipantGroup('"+newGroupID+"', '"+self.db["masters"][1]+"@c.us"+"')"
				self.driver.driver.execute_script(script=code)

				self.db["id"] = newGroupID

				self.sendMessage(newGroupID, "NEW DB\n"+newGroupID+"\n"+invite)
				self.sendMessage(newGroupID, str(self.db))
				self.backup(now=True)
				# if obj is not None:
				# 	imageurl = obj.imageurl
				# 	# imageurl = "https://aux2.iconspalace.com/uploads/whatsapp-flat-icon-256.png"
				# 	# imageurl = ""
				# 	self.master.setGroupIcon(newGroupID, imageurl)
			# else:
			number = self.db["id"]
		return self.driver.loadDB(number = number)

	def backupService(self, db = None, service = None, api = None):
		data = [db,service]
		# self.backupServiceAsync(data)
		if service in self.services:
			if self.services[service]["api"] is api:
				bT = Thread(target = self.backupServiceAsync,args = [data])
				bT.start()

	def newRandomID(self, N = 3):
		pas = False
		res = ""
		while(not pas):
			rand = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=N))
			new = True
			for target in self.db["groups"]:
				if "link" in self.db["groups"][target]:
					if self.db["groups"][target]["link"] == rand:
						new = False
			if new:
				pas = True
				res = rand
		return res

	def genLink(self, api = None, service = None, chatID = None, answer = "", newLink = "", asMaster = False):
		if asMaster is False:
			if api is None or service is None or chatID is None or answer is None:
				return "https://google.com/x"

		if service in self.services:
			if self.services[service]["api"] is api:

				target = chatID
				if target in self.db["groups"] and "service" in self.db["groups"][target] and service.lower() == self.db["groups"][target]["service"].lower():
					if "links" not in self.db["groups"][target]:
						self.db["groups"][target]["links"] = {}

					linkBase = ""
					if not asMaster:
						if "link" not in self.db["groups"][target]:
							linkBase = self.db["groups"][target]["link"] = self.newRandomID()
						else:
							linkBase = self.db["groups"][target]["link"]

					fullLink = linkBase +"/"+ newLink
					invite = "https://google.com/xy"
					if "invite" in self.db["groups"][target] and self.db["groups"][target]["invite"] is not None:
						invite = self.db["groups"][target]["invite"]

					user = None
					if "user" in self.db["groups"][target]:
						user = self.db["groups"][target]["user"]

					linkData = {"service":service, "chatID":chatID, "answer":answer, "invite":invite, "user":user}

					self.db["groups"][target]["links"][fullLink] = linkData
					self.links[fullLink] = linkData


					linkDataGroup = {"service":service, "chatID":chatID, "answer":"", "invite":invite, "user":user}
					self.db["groups"][target]["links"][linkBase] = linkDataGroup
					self.links[linkBase] = linkDataGroup


					self.backup()

					# sub = "akeyo.io/w?"
					sub = self.baseURL
					fullurl = sub + fullLink

					return fullurl

		return "https://google.com/x"

	def backupServiceAsync(self,data):
		time.sleep(self.db["backupDelay"])
		db, service = data
		print("SSSSSSSSS",service,db)
		if time.time() - self.db["lastBackupServices"] < self.db["backupInterval"]:
			return False

		if service is None or len(service) == 0:
			return None

		backupChat = None
		if service in self.db["servicesDB"]:
			chatID = self.db["servicesDB"][service]["dbID"]
			if chatID is not None:
				bchat = None
				try:
					bchat = self.driver.getChat(chatID)
				except Exception as ex:
					# print(" ::: ERROR - COULD NOT GET BACKUPCHAT",service,e," ::: ","\n")
					# traceback.print_exc()
					try:
						chatID = self.initServicesDB(service = service)
						bchat = self.driver.getChat(chatID)
						self.db["servicesDB"][service]["dbID"] = chatID
					except Exception as e:
						print(" ::: ERROR - COULD NOT INIT BACKUPCHAT",service,e," ::: ","\n")
						traceback.print_exc()
				if bchat is not None:
					print("FFFFFFFFFFFFFFFUCKKK yea")
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
		if not self.startBackup:
			self.startBackup = True
			self.backupstart()

		self.activity = True
		if now:
			self.backupNow = True

	def backupstart(self, now = None):
		bT = Thread(target = self.backupAsync,args = [now])
		bT.start()

	def backupAsync(self,data, delay = 4*60):
		while(True):
			t = time.time()
			while(time.time()-t < delay and not self.backupNow):
				time.sleep(10)
			if self.activity or self.backupNow:
				self.activity = False
				self.backupNow = False
				self.db["lastBackup"] = time.time()
				self.driver.updateDB(self.db,number=self.db["id"])


		# now = data
		# if now is not None:
		# else:
		# 	time.sleep(self.db["backupDelay"])
		# 	if time.time() - self.db["lastBackup"] < self.db["backupInterval"]:
		# 		return False

	def ProcessServiceAsync(self, obj, info):
		serviceT = Thread(target = self.ProcessService, args = [[obj,info]])
		serviceT.start()

	def ProcessService(self, data):
		# try:
		# service, chatID, text = data
		obj, info = data
		obj.process(info)
		# self.serviceFuncs["services"][service](chatID, text)

		# except Exception as e:
		# 	print(" ::: ERROR - Processing Service ::: ",serice,":::",chatID,":::",text,":::","\n",e,e.args,"\n")



	def quit(self):
		self.driver.quit()

	def Nothing(data):
		print(":::Nothign::: DATA=",data)



''' running master '''
master = None
timeout = time.time()
maxtimeout = 30

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
	master = Master.shares[0]

	if "exit" in text:
		print("EXITTT")
		print("EXITTT")
		print("EXITTT")
		print("EXITTT")
		text = text.split("exit/")[1]
		return
		return redirect("https://chat.whatsapp.com/JmnYDofCd7v0cXzfBgcVDO")
		return render_template("exit.html", user_image = "full_filename", status = "s")

	if "join" == text:
		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")

	if "join" in text:
		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ",text,len(text))
		master.runningSubscriptions+=1
		place = master.runningSubscriptions
		service = "Master"
		if len(text.split("/")) > 1 and len(text.split("/")[1]) > 0:
			afterSlash = text.split("/")[1]
			foundService = None
			for serv in master.services:
				if afterSlash.lower() == serv.lower():
					foundService = serv
			if foundService is not None:
				service = foundService

		while(len(master.db["availableChats"][service]) == 0 or place < master.runningSubscriptions):
			time.sleep(0.5)
			# print("NEW USER WAITING FOR MASTER GROUP")

		firstKey = list(master.db["availableChats"][service])[0]
		return redirect(master.db["availableChats"][service][firstKey])
		#
		# master.backup(now = True)
		# runningSubscriptions-=1
		#



	if text.split("/")[0] in master.links:
		print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
		print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
		print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
		print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
		print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
		print("SERVING LINK "+text)
		linkData = master.links[text.split("/")[0]]
		foundCmd = False
		if len(text.split("/")) > 1:
			data = None
			cmd = "/".join(text.split("/")[:2])
			print("CCCCCCCCCCCCCCCCCCCCCC",master.links)
			print("CCCCCCCCCCCCCCCCCCCCCC")
			print("CCCCCCCCCCCCCCCCCCCCCC")
			print("CCCCCCCCCCCCCCCCCCCCCC")
			print("CCCCCCCCCCCCCCCCCCCCCC",cmd)
			if cmd in master.links:
				linkData = master.links[cmd]
				foundCmd = True

		if linkData is not None and "service" in linkData and "chatID" in linkData and "answer" in linkData and "invite" in linkData:
			# service = linkData["service"]
			service, chatID, answer, invite = linkData["service"], linkData["chatID"], linkData["answer"], linkData["invite"]
			user = chatID
			if "user" in linkData and linkData["user"] is not None:
				user = linkData["user"]
			if "obj" in master.services[service]:
				obj = master.services[service]["obj"]
				if obj is not None:
					#Get Nicknames

					toSend = ""
					if foundCmd:
						toSend += answer
						if len(text.split("/")) > 2:
							toSend += "/" + "/".join(text.split("/")[2:])
					else:
						if len(text.split("/")) > 1:
							toSend += "/".join(text.split("/")[1:])

					if toSend in obj.examples:
						print("EEEEEXXXXXXAMMMPLEEEEEE XMPL")
						if "answer" in obj.examples[toSend]:
							toSend = obj.examples[toSend]["answer"]

						master.sendMessage(chatID, toSend)
						time.sleep(1)

					master.ProcessServiceAsync(obj,{"origin":chatID, "user":user, "content":toSend})

				print("RRRRRRRRRRRRRRRRRRRRRedirecting")	#
				print("RRRRRRRRRRRRRRRRRRRRRedirecting")	#
				print("RRRRRRRRRRRRRRRRRRRRRedirecting")	#
				print("RRRRRRRRRRRRRRRRRRRRRedirecting")	#
				print("RRRRRRRRRRRRRRRRRRRRRedirecting")	#
				print("RRRRRRRRRRRRRRRRRRRRRedirecting",invite)	#
				return redirect(invite)

	if text in refs:
		return redirect(refs[text])
	else:
		return redirect("/")


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
	if runLocal :
		pass
		app.run(debug=True, host='0.0.0.0',use_reloader=False)
	# app.run(debug=True, host='0.0.0.0',use_reloader=False)
	print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
	# print("STARTING APP22222222222")
