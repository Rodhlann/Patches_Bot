import time
import datetime as dt
import sys
import os
import logging
from urllib import request, error
import praw
from praw.exceptions import APIException
from bs4 import BeautifulSoup
import pyrebase
import config

# -------- START GLOBALS ----------

savedHrefs = []

try: 
    reddit = praw.Reddit('bot1')
    reddit.user.me()
except Exception as e:
    logging.error(e.message)
    sys.exit() 

try: 
    logging.info("Connecting to database...")
    firebase = pyrebase.initialize_app(config.dbconfig)
    auth = firebase.auth() 
    user = auth.sign_in_with_email_and_password(config.email, config.password)
    db = firebase.database() 
    logging.info("Database connection established...")
except error.HTTPError as e: 
    logging.error("Database connection error!") 
    sys.exit() 

# -------- END GLOBALS ----------

def submit(game, platform, link, name):
    response = None
    while response == None:
        try:
            response = reddit.subreddit("patchnotes").submit(formatTitle(game, name, platform), url=link)
            response.reply("Please message me if something is wrong with this post or you have any suggestions!")
            postToDB(user, link)
            logging.info(name + "' logged.")
        except APIException as e:
            if e.error_type == 'RATELIMIT':
                logging.warning(e.message)
            else:
                logging.error(e) 
                sys.exit()
            time.sleep(30)
        except Exception as e:
            logging.error(e)
            sys.exit()
    logging.info("Submission complete!")

def formatTitle(game, postTitle, platform): 
    date = str(dt.date.today()).replace('-', '/')
    return "["+game+"] ("+date+") ("+platform+") " + postTitle 

def makeSoup(url): 
    page_body = ""
    # NOTE: User agent prevents sites from blocking the bot 
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with request.urlopen(req) as page:
        page_body = page.read()
    return BeautifulSoup(page_body, 'html.parser')

def postToDB(user, data):
    logging.info("Posting " + data + " to database...")
    try: 
        user = auth.refresh(user['refreshToken'])
        db.child("links").push({"link": data}, user['idToken'])
    except Exception: 
        logging.error("Database post error!") 
        sys.exit() 
    logging.info("Database post successful!") 

def getPostsFromDB(user): 
    logging.info("Getting link data from database...")
    try: 
        user = auth.refresh(user['refreshToken'])
        data = db.child("links").get()
        for link in data.each():
            savedHrefs.append(link.item[1]['link'])
    except Exception: 
        logging.error("Database retrieval error!")
        sys.exit() 
    logging.info("Database retrieval successful!") 

def getSavedHrefs():
    # Method used to get USER variable, which is not available to getPostsFromDB
    # TODO: Figure out why USER variable isn't avaialble to getPostsFromDB
    getPostsFromDB(user) 
    return savedHrefs
    