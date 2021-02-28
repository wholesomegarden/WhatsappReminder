#Service.py
import time
import requests
# ws = create_connection("ws://https://colors.crystalvision.co.il/api/")
# # ws = create_connection()
# wss = websockets.connect("wss://colors.crystalvision.co.il/ws/crystalweb")

import json
from websocket import create_connection



# import asyncio
# import time
# import websockets

# data = {"command":"startPollingTags","tags":[{"header":"Amount Left to feed 2","tagName":"ROBOT_1_ROW10_AMOUNT_LEFT_TO_FEED_2"},{"header":"Daily amount 2","tagName":"ROBOT_1_ROW10_DAILY_AMOUNT_2"},{"header":"Accumulated amount 2","tagName":"ROBOT_1_ROW10_ACCUMULATED_AMOUNT_2"},{"header":"Meal amount 2","tagName":"ROBOT_1_ROW10_MEAL_AMOUNT_2"},{"header":"Last Day amount 2","tagName":"ROBOT_1_ROW10_LAST_DAY_AMOUNT_2"},{"header":"Amount Left to feed 3","tagName":"ROBOT_1_ROW10_AMOUNT_LEFT_TO_FEED_3"},{"header":"Daily amount 3","tagName":"ROBOT_1_ROW10_DAILY_AMOUNT_3"},{"header":"Accumulated amount 3","tagName":"ROBOT_1_ROW10_ACCUMULATED_AMOUNT_3"},{"header":"Meal amount 3","tagName":"ROBOT_1_ROW10_MEAL_AMOUNT_3"},{"header":"Last Day amount 3","tagName":"ROBOT_1_ROW10_LAST_DAY_AMOUNT_3"}],"sender":"web","id":5576}
# cip = "wss://colors.crystalvision.co.il/ws/crystalweb"
# async def sendData():
# 	async with websockets.connect(cip) as websocket:
# 		while 1:
# 			try:
# 				#a = readValues() #read values from a function
# 				#insertdata(a) #function to write values to mysql
# 				await websocket.send(data)
# 				print('data updated')
# 				back = await websocket.recv()
# 				print('got',back)
# 				time.sleep(20) #wait and then do it again
# 			except Exception as e:
# 				print(e)
#
# asyncio.get_event_loop().run_until_complete(sendData())
#



pheaders = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip',
"Cache-Control": "no-cache",
"Pragma": "no-cache",
'DNT' : '1', # Do Not Track Request Header
'Connection' : 'close' }
class ClearVisionService(object):
	id = "ClearVision"
	name = "ClearVision!"
	welcome = "*Welcome to ClearVision! Service* \n\nשלחו לנו פקודות בכדי לתקשר עם ClearVision API"
	help = "send a message to get it back"
	imageurl = "https://yt3.ggpht.com/ytc/AAUvwnhgdHkoOO5ESnB-7wkQuBY1MrroC1emLGA6TynMlg=s900-c-k-c0x00ffffff-no-rj"
	shortDescription = "ClearVision ClearVision ClearVision"
	share = None

	examples = {"_":{"text":"Hello World","thumbnail":None}}

	def __init__(self,db, api):
		ClearVisionService.share = self

		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ClearVision",ClearVisionService.share)
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

	def ClearVision(self,code = "print('Hello World')", data = {"language": "python"}, purl = "https://emkc.org/api/v1/ClearVision/execute"):
		if "source" not in data:
			data["source"] = ""
		data["source"] = code

		print("SENDING DATA:",str(data))
		r = requests.post(purl, data, headers=pheaders)
		if r.status_code == 200:
			out = r.json()
			# out = "".join("".join(r.json()["output"].split("[")[1:])[::-1].split("]")[1:])[::-1]
			return True, out
		return False, r.json()["stdout"]


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

		# data = {"command":"startPollingTags","tags":[{"header":"Amount Left to feed 2","tagName":"ROBOT_1_ROW10_AMOUNT_LEFT_TO_FEED_2"},{"header":"Daily amount 2","tagName":"ROBOT_1_ROW10_DAILY_AMOUNT_2"},{"header":"Accumulated amount 2","tagName":"ROBOT_1_ROW10_ACCUMULATED_AMOUNT_2"},{"header":"Meal amount 2","tagName":"ROBOT_1_ROW10_MEAL_AMOUNT_2"},{"header":"Last Day amount 2","tagName":"ROBOT_1_ROW10_LAST_DAY_AMOUNT_2"},{"header":"Amount Left to feed 3","tagName":"ROBOT_1_ROW10_AMOUNT_LEFT_TO_FEED_3"},{"header":"Daily amount 3","tagName":"ROBOT_1_ROW10_DAILY_AMOUNT_3"},{"header":"Accumulated amount 3","tagName":"ROBOT_1_ROW10_ACCUMULATED_AMOUNT_3"},{"header":"Meal amount 3","tagName":"ROBOT_1_ROW10_MEAL_AMOUNT_3"},{"header":"Last Day amount 3","tagName":"ROBOT_1_ROW10_LAST_DAY_AMOUNT_3"}],"sender":"web","id":5576}

		# data = {"command":"getTagValue","tags":[{"header":"Amount Left to feed 2","tagName":"ROBOT_1_ROW10_AMOUNT_LEFT_TO_FEED_2"},{"header":"Daily amount 2","tagName":"ROBOT_1_ROW10_DAILY_AMOUNT_2"},{"header":"Accumulated amount 2","tagName":"ROBOT_1_ROW10_ACCUMULATED_AMOUNT_2"},{"header":"Meal amount 2","tagName":"ROBOT_1_ROW10_MEAL_AMOUNT_2"},{"header":"Last Day amount 2","tagName":"ROBOT_1_ROW10_LAST_DAY_AMOUNT_2"},{"header":"Amount Left to feed 3","tagName":"ROBOT_1_ROW10_AMOUNT_LEFT_TO_FEED_3"},{"header":"Daily amount 3","tagName":"ROBOT_1_ROW10_DAILY_AMOUNT_3"},{"header":"Accumulated amount 3","tagName":"ROBOT_1_ROW10_ACCUMULATED_AMOUNT_3"},{"header":"Meal amount 3","tagName":"ROBOT_1_ROW10_MEAL_AMOUNT_3"},{"header":"Last Day amount 3","tagName":"ROBOT_1_ROW10_LAST_DAY_AMOUNT_3"}],"sender":"web","id":5576}


		data = {"command":"getTagValue","tagName":content,"sender":"web","id":92370}
		# data = {"command":"getTagValue","tagName":"ROBOT_2_FEEDER_1_CAL_FACTOR","sender":"web","id":92370}

		# self.api.send(origin, "Sending to ClearVision\n\n"+str(data))
		# self.api.send(origin, pre+"Code Finished: "+str(res)+"\n"+output+"\n"+"\n"+str(extra))
		ws = create_connection("wss://colors.crystalvision.co.il/ws/crystalweb")
		# data = {"command":"startPollingTags","tags":[{"header":"Amount Left to feed 2","tagName":"ROBOT_1_ROW10_AMOUNT_LEFT_TO_FEED_2"},{"header":"Daily amount 2","tagName":"ROBOT_1_ROW10_DAILY_AMOUNT_2"},{"header":"Accumulated amount 2","tagName":"ROBOT_1_ROW10_ACCUMULATED_AMOUNT_2"},{"header":"Meal amount 2","tagName":"ROBOT_1_ROW10_MEAL_AMOUNT_2"},{"header":"Last Day amount 2","tagName":"ROBOT_1_ROW10_LAST_DAY_AMOUNT_2"},{"header":"Amount Left to feed 3","tagName":"ROBOT_1_ROW10_AMOUNT_LEFT_TO_FEED_3"},{"header":"Daily amount 3","tagName":"ROBOT_1_ROW10_DAILY_AMOUNT_3"},{"header":"Accumulated amount 3","tagName":"ROBOT_1_ROW10_ACCUMULATED_AMOUNT_3"},{"header":"Meal amount 3","tagName":"ROBOT_1_ROW10_MEAL_AMOUNT_3"},{"header":"Last Day amount 3","tagName":"ROBOT_1_ROW10_LAST_DAY_AMOUNT_3"}],"sender":"web","id":5576}
		cip = "wss://colors.crystalvision.co.il/ws/crystalweb"
		datax = json.dumps(data).encode('utf-8')
		print("Sending data")
		ws.send(datax)
		print("Sent")
		print("Receiving...")
		result =  ws.recv()
		di = json.loads(result)
		prepT = ""
		print(result)
		# for tag in di["Tags"]:
		# 	prepT += "*"+tag["tagName"] +"* : "+tag["response"]+"\n\n"
		try:
			prepT += "*"+di["data"]["tagName"] +"* : "+di["data"]["value"]+"\n\n"
		except:
			prepT = str(di)
		# prepT =  di["data"]["tageName"]
		print("Received '%s'" % result)
		ws.close()
		self.api.send(origin, "GOT BACK:\n\n"+prepT)

		#
		# # importing the requests library
		#
		# # defining the api-endpoint
		# API_ENDPOINT = "https://colors.crystalvision.co.il/api/"
		#
		# # sending post request and saving response as response object
		# r = requests.post(url = API_ENDPOINT, data = data)
		#
		# # extracting response text
		# pastebin_url = r.text
		# print("The pastebin URL is:%s"%pastebin_url)



		# self.api.send(origin, pastebin_url)

		#
		# pre = ""
		# if len(content) < 2:
		# 	res, dict = self.ClearVision()
		# else:
		# 	res, dict = self.ClearVision(code = content)
		# 	# pre = "X"
		#
		# output = dict.pop("output")
		# extra = dict
		#
		# self.api.send(origin, pre+"Code Finished: "+str(res)+"\n"+output+"\n"+"\n"+str(extra))
		# sendBack = content
		#
		# withLink = True
		# if withLink:
		# 	answer = ":answerid:555"
		# 	myLink = self.api.genLink(origin, answer)
		# 	sendBack += "\n\n"+answer+":\n"+myLink
		#
		# self.db["upcoming"].append([origin, sendBack])


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
		if "users" not in self.db:
			self.db["users"] = {}
		if origin not in self.db["users"]:
			self.db["users"][origin] = origin
			self.backup()
