from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import re
import os.path
from os import path
import sqlite3
import schedule
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import discord_webhook

user = ('')
pwd = ('')
opt = Options()
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 2, 
    "profile.default_content_setting_values.notifications": 2 
  })

# driver = webdriver.Chrome(chrome_options=opt,service_log_path='NUL')
driver = None

url = "https://teams.microsoft.com/"

def login():
    global mah
    mah.implicitly_wait(25)
    time.sleep(4)
    username = mah.find_element_by_id('i0116')
    username.send_keys(user)
    time.sleep(2)
    enter = mah.find_element_by_id('idSIButton9')
    enter.click()
    time.sleep(2)
    password = mah.find_element_by_id("i0118")
    password.send_keys(pwd)
    time.sleep(2)
    enter = mah.find_element_by_id('idSIButton9')
    enter.click()
    enter = mah.find_element_by_id('idSIButton9')
    enter.click()
    time.sleep(5)

def createDB():
	conn = sqlite3.connect('mah.db')
	c=conn.cursor()
	# Create table
	c.execute('''CREATE TABLE mah(class text, start_time text, end_time text, day text)''')
	conn.commit()
	conn.close()
	print("Created timetable Database")



def validate_input(regex,inp):
	if not re.match(regex,inp):
		return False
	return True

def validate_day(inp):
	days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

	if inp.lower() in days:
		return True
	else:
		return False


def add_timetable():
	if(not(path.exists("mah.db"))):
			createDB()
	op = int(input("1. Add class\n2. Done adding\nEnter option : "))
	while(op==1):
		name = input("Enter class name : ")
		start_time = input("Enter class start time in 24 hour format: (HH:MM) ")
		while not(validate_input("\d\d:\d\d",start_time)):
			print("Invalid input, try again")
			start_time = input("Enter class start time in 24 hour format: (HH:MM) ")

		end_time = input("Enter class end time in 24 hour format: (HH:MM) ")
		while not(validate_input("\d\d:\d\d",end_time)):
			print("Invalid input, try again")
			end_time = input("Enter class end time in 24 hour format: (HH:MM) ")

		day = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")
		while not(validate_day(day.strip())):
			print("Invalid input, try again")
			end_time = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")


		conn = sqlite3.connect('mah.db')
		c=conn.cursor()

		# Insert a row of data
		c.execute("INSERT INTO mah VALUES ('%s','%s','%s','%s')"%(name,start_time,end_time,day))

		conn.commit()
		conn.close()

		print("Class added to database\n")

		op = int(input("1. Add class\n2. Done adding\nEnter option : "))


def view_timetable():
	conn = sqlite3.connect('mah.db')
	c=conn.cursor()
	for row in c.execute('SELECT * FROM mah'):
		print(row)
	conn.close()



def joinclass(class_name,start_time,end_time):
	global mah

	try_time = int(start_time.split(":")[1]) + 15
	try_time = start_time.split(":")[0] + ":" + str(try_time)

	time.sleep(5)


	classes_available = mah.find_elements_by_class_name("name-channel-type")

	for i in classes_available:
		if class_name.lower() in i.get_amahribute('innerHTML').lower():
			print("JOINING CLASS ",class_name)
			i.click()
			break


	time.sleep(4)


	try:
		joinbtn = mah.find_element_by_class_name("ts-calling-join-button")
		joinbtn.click()

	except:
		#join button not found
		#refresh every minute until found
		k = 1
		while(k<=15):
			print("Join button not found, trying again")
			time.sleep(60)
			mah.refresh()
			joinclass(class_name,start_time,end_time)
			# schedule.every(1).minutes.do(joinclass,class_name,start_time,end_time)
			k+=1
		print("Seems like there is no class today.")  
		discord_webhook.send_msg(class_name=class_name,status="noclass",start_time=start_time,end_time=end_time)
	time.sleep(6)
	webcam = mah.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
	if(webcam.get_attribute('title')=='Turn camera off'):
		webcam.click()
	time.sleep(2)

	microphone = mah.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[2]/div/button/span[1]')
	if(microphone.get_attribute('title')=='Mute microphone'):
		microphone.click()
	time.sleep(1)   

	enter = mah.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
	enter.click()
	print("CLASS JOINED ",class_name)

	discord_webhook.send_msg(class_name=class_name,status="joined",start_time=start_time,end_time=end_time)

	tmp = "%H:%M"

	class_running_time = datetime.strptime(end_time,tmp) - datetime.strptime(start_time,tmp)

	time.sleep(class_running_time.seconds)


	back = mah.find_element_by_id('app-bar-12a84919f-59d8-4441-a975-2a8c2643b741')
	back.click() #come back to homepage
	time.sleep(1)

	end = mah.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/multi-call-list/div/div/calling-monitor/div/div/div[2]/calling-unified-bar/section/div/div/div[2]/items-group/div/item-widget/push-button/div/button')
	end.click()
	print("Class left")
	discord_webhook.send_msg(class_name=class_name,status="left",start_time=start_time,end_time=end_time)





def start_browser():

	global mah
	mah = webdriver.Chrome("`PASTE YOUR WEBDRIVER PATH HERE`",options=opt,service_log_path='NUL') #Example ("E:\WebDrivers\chromedriver.exe",options=opt,service_log_path='NUL')

	mah.get(url)


	if("login.microsoftonline.com" in mah.current_url):
		login()



def sched():
	conn = sqlite3.connect('mah.db')
	c=conn.cursor()
	for row in c.execute('SELECT * FROM mah'):
		#schedule all classes
		name = row[0]
		start_time = row[1]
		end_time = row[2]
		day = row[3]

		if day.lower()=="monday":
			schedule.every().monday.at(start_time).do(joinclass,name,start_time,end_time)
		if day.lower()=="tuesday":
			schedule.every().tuesday.at(start_time).do(joinclass,name,start_time,end_time)	
		if day.lower()=="wednesday":
			schedule.every().wednesday.at(start_time).do(joinclass,name,start_time,end_time)	 
		if day.lower()=="thursday":
			schedule.every().thursday.at(start_time).do(joinclass,name,start_time,end_time)
		if day.lower()=="friday":
			schedule.every().friday.at(start_time).do(joinclass,name,start_time,end_time)
		if day.lower()=="saturday":
			schedule.every().saturday.at(start_time).do(joinclass,name,start_time,end_time)		
		if day.lower()=="sunday":
			schedule.every().sunday.at(start_time).do(joinclass,name,start_time,end_time)		


	#Start browser
	start_browser()
	while True:
		# Checks whether a scheduled task
		# is pending to run or not
		schedule.run_pending()
		time.sleep(1)

print('_|_|_|_|_|  _|_|_|_|    _|_|    _|      _|    _|_|_|              _|_|_|      _|_|    _|_|_|_|_|')  
print('    _|      _|        _|    _|  _|_|  _|_|  _|                    _|    _|  _|    _|      _|    ')  
print('    _|      _|_|_|    _|_|_|_|  _|  _|  _|    _|_|    _|_|_|_|_|  _|_|_|    _|    _|      _|    ') 
print('    _|      _|        _|    _|  _|      _|        _|              _|    _|  _|    _|      _|    ')  
print('    _|      _|_|_|_|  _|    _|  _|      _|  _|_|_|                _|_|_|      _|_|        _|   \n \n ')  
                                                                                                  		
if __name__=="__main__":
    
	op = int(input(("1. Modify Timetable\n2. View Timetable\n3. Start Bot\nEnter option : ")))
	
	if(op==1):
		add_timetable()
	if(op==2):
		view_timetable()
	if(op==3):
		sched()

