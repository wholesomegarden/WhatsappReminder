# app.py
from dateparser.search import search_dates
from WhatsappReminder import *

from threading import Thread


id = "0547772000"


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

print("@@@@@@@@@@@@@@@@@@@@@@@@@@1")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@2")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@3")

from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
# print("AAAAAAAA")
# print()
# driver1 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
# driver1 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#
# print("BBBBBBBBBB")
# driver1.get("https://google.com")
# print(str(driver1.page_source)[:100])
# print("CCCCCCCCCC")


def runReminder():

	# driver = WhatsAPIDriver(firefox_binary="/app/vendor/firefox/firefox",executable_path='/app/vendor/geckodriver/geckodriver',username="wholesomegarden")
	driver = WhatsAPIDriver(client='chrome', chrome_options=chrome_options,username="wholesomegarden")

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
	print("Waiting for QR")
	driver.wait_for_login()
	print("Saving session")


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
	status = "NotLoggedIn"
	img = None
	while status is not "LoggedIn":
		c+=1
		print("status", status)


		print("Checking qr, status", status)

		print("AAAAAAAAAAAAA")
		img = driver.get_qr("static/img/newQR.png")
		print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",str(img)[:100])
		# im_path = os.path.join("static/img/newQR.png")

		print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",c)
		print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",c)
		print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",c)
		print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",c)

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


		status = driver.get_status()
		# output = qr_scanner.extract(img)
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


	print("")
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
	print("@@@@@@@@@@@@@@@@@@")
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
	while True:
		time.sleep(.71)
		print("Checking for more messages, status", driver.get_status())
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
					print("-- Other")
				print("PROCESSING MESSAGE:",message)
				Manager.process(message.sender.id,message.content)


from flask import Flask, render_template
# app = Flask(__name__)
app=Flask(__name__,template_folder='templates')


import os
arr = os.listdir()
for a in arr:
	# print(a)
	pass
# input()

PEOPLE_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def hello_world():

	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "newQR.png")
	return render_template("index.html", user_image = full_filename)

runners = 0

def flaskRun():
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	print("GONNA RUN ASYNC")
	if runners < 1:
		runners += 1
		t = Thread(target=flaskRunAsync,args=[None,])
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
	# input()
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	print("AAAAAAAAAAAA ASYNC")
	runReminder()


if __name__ == '__main__':
	flaskRun()
	print("STARTING APP")
	print("STARTING APP")
	print("STARTING APP")
	print("STARTING APP")
	print("STARTING APP")
	app.run(debug=True, host='0.0.0.0')
else:
	flaskRun()
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
