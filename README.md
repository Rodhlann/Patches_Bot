# Patches_Bot
Reddit Patch Notes Bot

In order to run this code you will need to install the following libraries until I setup a setup.py: 
 - PRAW (pip3 install praw --user) 
 - BeautifulSoup4 (pip3 install beautifulsoup4 --user) 
 - Pyrebase (pip3 install pyrebase --user) 

You will also need to create file called praw.ini with this content: 
```
[bot1]
client_id=
client_secret=
password=
username=
user_agent=
```

The client_id and client_secret are given to you when you create an app on your reddit.com profile. 
The username and password are your reddit credentials
The user_agent is free text to describe your bot/script 


There is also a config file that I will need to distribute on a case by case basis, if you are interested in 
contributing. 

All of the previously submitted posts are now saved to firebase so that we are not posting duplicate patch notes. 
  
If you would like to add more games to Patches_Bot, or contribute in any other way, please contact me and we can move forward with that process.  

Thanks for taking a look! 
