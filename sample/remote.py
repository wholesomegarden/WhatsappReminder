import json
import os
import sys
import time

from webwhatsapi import WhatsAPIDriver

print("Environment", os.environ)
try:
    os.environ["SELENIUM"]
except KeyError:
    print("Please set the environment variable SELENIUM to Selenium URL")
    sys.exit(1)

from PIL import Image

from resizeimage import resizeimage

##Save session on "/firefox_cache/localStorage.json".
##Create the directory "/firefox_cache", it's on .gitignore
##The "app" directory is internal to docker, it corresponds to the root of the project.
##The profile parameter requires a directory not a file.
profiledir = os.path.join(".", "firefox_cache")
if not os.path.exists(profiledir):
    os.makedirs(profiledir)

driver = WhatsAPIDriver(
    profile=profiledir, client="remote", command_executor=os.environ["SELENIUM"]
)

print("Waiting for QR")
driver.wait_for_login()
print("Saving session")

import timg
obj = timg.Renderer()
# from qrtools import qrtools
# from PIL import Image
# import zbarlight
# qr = qrtools.QR()

#
# from PIL import Image
# from pyzbar.pyzbar import decode

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
s = 140
while c<30:
    c+=1
    print("BBBB")
    # print("Checking qr, status", driver.get_status())

    img = driver.get_qr()
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
    print("CCC",img)
    obj.load_image_from_file(img)

    obj.resize(s,s)
    s-=1
    # print(obj)
    obj.render(timg.Ansi24HblockMethod)
    print("DDD",s,s,s,s)
    time.sleep(10)
    # driver.save_firefox_profile(remove_old=False)
    # time.sleep(3)
    # try:
    #     driver.reload_qr()
    # except:
    #     print("refresh finised")
print("Bot started")

while True:
    time.sleep(.71)
    print("Checking for more messages, status", driver.get_status())
    for contact in driver.get_unread():
        for message in contact.messages:
            print(json.dumps(message.get_js_obj(), indent=4))
            sender = message.get_js_obj()["chat"]["contact"]["formattedName"]

            for contact in driver.get_contacts():
                print("CCCC",contact.get_safe_name() )
                if  sender in contact.get_safe_name():
                    chat = contact.get_chat()
                    chat.send_message("Hi "+sender+" !!!")


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
