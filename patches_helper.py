import praw
import time
import datetime as dt
import json
import sys 
import os 
from praw.exceptions import APIException
import logging 
from urllib import request
from bs4 import BeautifulSoup

# -------- START GLOBALS ----------

savedHrefs = []

try: 
    reddit = praw.Reddit('bot1')
    reddit.user.me()
except Exception as e:
    logging.error(e.message)
    sys.exit() 

# -------- END GLOBALS ----------

def submit(game, platform, link, name):
    oldHrefs = open("posts.txt", "a")
    response = None
    while(response == None):
        try:
            response = reddit.subreddit("patchnotes").submit(formatTitle(game, name, platform), url=link)
            response.reply("Please message me if something is wrong with this post or you have any suggestions!")
            oldHrefs.write(link + '\n')
            logging.info(name + "' logged.")
        except APIException as e:
            if e.error_type == 'RATELIMIT':
                logging.warning(e.message)
            else:
                logging.error(e.message) 
                sys.exit()
            time.sleep(30)
        except Exception as e:
            logging.error(e.message)
            sys.exit()
    logging.info("Submission complete!")
    oldHrefs.close() 

def formatTitle(game, postTitle, platform): 
    date = str(dt.date.today()).replace('-', '/')
    return "["+game+"] ("+date+") ("+platform+") " + postTitle 

def getSavedHrefs():
    if os.path.exists("posts.txt"): 
        oldHrefs = open("posts.txt", "r")
        for id in oldHrefs:
            savedHrefs.append(id.replace('\n', ''))
    else: 
        oldHrefs = open("posts.txt", "w+")  
    oldHrefs.close() 
    return savedHrefs

def makeSoup(url): 
    page_body = ""
    # NOTE: User agent prevents sites from blocking the bot 
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with request.urlopen(req) as page:
        page_body = page.read()
    return BeautifulSoup(page_body, 'html.parser')