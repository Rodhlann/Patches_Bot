from urllib import request
from bs4 import BeautifulSoup
import praw
import time
import datetime as dt
import json
import sys 
import os 
from praw.exceptions import APIException
import logging 

logging.basicConfig(filename='Patches.log',level=logging.INFO)

# 1 Month 
submission_interval = time.mktime((dt.date.today() - dt.timedelta(30)).timetuple())
foundPosts = []

try: 
    reddit = praw.Reddit('bot1')
    reddit.user.me()
except Exception as e:
    print(e) 
    sys.exit() 

#pubg
url = "http://steamcommunity.com/games/578080/announcements"
s = ""
with request.urlopen(url) as page:
    s = page.read()
soup = BeautifulSoup(s, 'html.parser')

link = ""
name = ""
posts = soup.find_all("a", class_="large_title")
for post in posts: 
    if ('Early Access -'.lower() in post.string.lower()
        and 'Update'.lower() in post.string.lower()):
        link = post['href']
        name = post.string

#HoTS
url = "http://us.battle.net/heroes/en/blog/"
with request.urlopen(url) as page:
    s = page.read()
soup = BeautifulSoup(s, 'html.parser')


posts = soup.find_all("a")
for post in posts:
    if(any(url in ('heroes-of-the-storm-patch', 'heroes-of-the-storm-hotfix', 'heroes-of-the-storm-balance')) for url in post.string.lower()):
        link = post['href']
        name = post.string


def submit(game, platform, link, name): 
    response = None 
    while(response == None): 
        try: 
            response = reddit.subreddit("test").submit(formatTitle(game, name, platform), url=link)
        except APIException as e:
            if e.error_type == 'RATELIMIT':
                logging.warning(e.message)
            else: 
                logging.error("[API ERROR] " + e.message)
                sys.exit()
            time.sleep(30) 
        except Exception as e: 
            logging.error(e.message)
            sys.exit() 
    logging.info("Submission for " + game + " done!")

def formatTitle(game, postTitle, platform): 
    date = str(dt.date.today()).replace('-', '/')
    return "["+game+"] ("+date+") ("+platform+") " + postTitle 

submit("PUBG", "PC", link, name) 