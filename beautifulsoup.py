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

def formatTitle(game, postTitle, platform):
    date = str(dt.date.today()).replace('-', '/')
    return "["+game+"] ("+date+") ("+platform+") " + postTitle

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

link = ""
name = ""
s = ""

#pubg
url = "http://steamcommunity.com/games/578080/announcements"
with request.urlopen(url) as page:
    s = page.read()
soup = BeautifulSoup(s, 'html.parser')

# posts = soup.find_all("a", class_="large_title")
# for post in posts: 
#     if (all(title in ('early access -', 'update')) for title in post.string.lower()):
#         link = post['href']
#         name = post.string

# submit("PUBG", "PC", link, name)

#HoTS
url = "http://us.battle.net/heroes/en/blog/"
with request.urlopen(url) as page:
    s = page.read()
soup = BeautifulSoup(s, 'html.parser')

posts = soup.find_all(class_="news-list__item__title")
hots_conditions = ['heroes-of-the-storm-patch', 'heroes-of-the-storm-hotfix', 'heroes-of-the-storm-balance']
for post in posts:
    href = post.find('a')['href']
    name = post.find('a').string.replace('\n', '')
    if(any(string in href.lower() for string in hots_conditions)):
        print(name + " : " + href)

# submit("HOTS", "PC", link, name)