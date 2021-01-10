# pastebin.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os, time

driver1 = webdriver.Firefox()

driver1.get("https://accounts.random.org/")

print(driver1.page_source)

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
