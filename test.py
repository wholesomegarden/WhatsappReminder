# test.py
from dateparser.search import search_dates
from WhatsappReminder import *
id = "0547772000"

#
# msg = "send message to Omer tomorrow morning "
# Manager.process(id, msg)
#
#

msg = "call omer thursday morning"
Manager.process(id, msg)

export PATH="$HOME/wholesomegarden/WhatsappReminder:$PATH"
#
# import wapy
#
# wapy.init()
# while True:
#     wapy.unread()
#     wapy.response('-wapy', 'text', text='Hello World!')
import os
import time
import matplotlib.pyplot as plt
from QRMatrix import *

from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
from skimage import io

from webwhatsapi import WhatsAPIDriver
driver = WhatsAPIDriver(username="mkhase")
img = driver.get_qr("i.png")
print(img)
# time.sleep(4)
QRCode = QRMatrix("decode", img)
print(QRCode.decode())
print("@@@@@@@@@@@@@@@@@@")
print("XXXXXXXX")
# # i = io.imread(img)
# # image = color.rgb2gray(i)
#
# image_rescaled = rescale(image, 0.25, anti_aliasing=False)
# io.imsave(img, image_rescaled)
print("XXXXXXXX")
import timg
obj = timg.Renderer()
obj.load_image_from_file(img)
obj.resize(106,106)
obj.render(timg.Ansi24HblockMethod)


for contact in driver.get_contacts():
    print("CCCC",contact.get_safe_name() )
    if  "@@@@@@@@@@@@@@@@@@@@@@@@@" in contact.get_safe_name():
        chat = contact.get_chat()
        chat.send_message("Hi Jack")



# 4. In case the QR code expires, you can use the reload_qr function to reload it
# driver.reload_qr()
# driver.view_unread()
# driver.get_all_chats()
# 7. To send a message, get a Contact object, and call the send_message function with the message.
# <Contact Object>.send_message("Hello")
# 8. Sending a message to an ID, whether a contact or not.
# driver.send_message_to_id(id, message)
