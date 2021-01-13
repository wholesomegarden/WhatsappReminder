# app.py
from dateparser.search import search_dates
from ServiceImporter import *

from threading import Thread


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
import os, sys, time
import json

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
