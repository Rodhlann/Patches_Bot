# Patches_Bot
Reddit Patch Notes Bot

In order to run this code you will need to install PRAW (pip install praw --user) 

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

The posts.txt file is generated automatically on run and contains a list of IDs that are associated to the submissions you have already posted. You should not have to enter any data in this file manually. 
  
If you would like to add more games to Patches_Bot please contact me and we can move forward with adding those. 
I would like to have as many games as possible, but I think I will need to refactor to make the program run faster/more efficiently
if it gets too big. 

I would also like to eventually create an account for this bot, as I am currently just using my personal account for now. This change might 
make it easier to collaborate in the future. 

Thanks for taking a look! 
