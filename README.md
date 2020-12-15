# Teams-Bot
Python based Bot with Selenium

This bot attends the online classes (or meetings) held on Microsoft teams, according to the given timetable.Informs if bot is successfully joined the
meeting through discord.

Works perfectly fine in Windows 10...other OS no idea...

Python 3 should be installed to the run the bot...

## Python3 can be downloaded from here.
https://www.python.org/downloads/


## Webdrivers can be downloaded from here : Check your browser version and download accordingly..
1. Chrome----> https://chromedriver.chromium.org/ ..
2. Edge------> https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ ..
3. Firefox----> https://github.com/mozilla/geckodriver/releases ..


## To check browser version go to : ..

1. **Chrome**----> chrome://settings/help ..
2. **Edge**------> edge://help ..
3. **Firefox**----> Click the menu button ≡ Menu , click Help and select About Firefox

## Add the Path of your webdriver to
- in `line 196` mah = webdriver.Chrome("`PASTE YOUR WEBDRIVER PATH HERE`",options=opt,service_log_path='NUL') #Example ("E:\WebDrivers\chromedriver.exe",options=opt,service_log_path='NUL')

## Change this line if ur browser is not chrome...
1. **for Edge**---- > `line 196` mah = webdriver.Edge("`PASTE YOUR WEBDRIVER PATH HERE`",options=opt,service_log_path='NUL') #Example ("E:\WebDrivers\chromedriver.exe",options=opt,service_log_path='NUL')
2. **for Firefox**--- > `line 196` mah = webdriver.Firefox("`PASTE YOUR WEBDRIVER PATH HERE`",options=opt,service_log_path='NUL') #Example ("E:\WebDrivers\chromedriver.exe",options=opt,service_log_path='NUL')

## Configure
There are few things you got configure before running this bot.

 - Open Microsoft teams on your browser https://teams.microsoft.com/, login to your account, change the dashboard view to list view (from grid view), so that your classes are displayed in a list view. 
 - ![This is how list view looks like](https://i.imgur.com/KXTl84h.jpg)
 - Open *msbot.py*, and put your microsoft teams credentials in the **user** & **pwd** field. 
 - Example - `user = ('myemail@email.com')`
 - `pwd = ('mypassword')`
 - Open *discord_webhook.py* and put your discord webhook URL in the **webhook_url** variable. 
 - Example - `webhook_url = "https://discord.com/api/webhooks/...."`

## Database Edit

 - Edit database if done some mistake during entering the information in bot
 - Download Sqlite browser and edit through this...
 - Download link:https://sqlitebrowser.org/dl/

## Install

 - Clone the repository `git clone https://github.com/mah-hacker/Teams-Bot`
 - Install requirements.txt `pip install -r requirements.txt`
 
 ## Run the bot
 - Run the bot `python msbot.py`
