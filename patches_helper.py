import time
import datetime as dt
import sys
import os
import logging
# TODO: Phase out urllib 
from urllib import request, error
import praw
from praw.exceptions import APIException
from bs4 import BeautifulSoup
import pyrebase
import config
import email_handler as email
import sms_handler as sms
import requests
import json 

# -------- START GLOBALS ----------

savedHrefs = []

try: 
    reddit = praw.Reddit('bot1')
    reddit.user.me()
except Exception as e:
    logging.error(e)
    email.alert_email("(patches_helper.init - connecting to Reddit)\n\n" + str(e)) 
    sms.alert_sms("(patches_helper.init - connecting to Reddit)")
    sys.exit() 

try: 
    logging.info("Connecting to database...")
    firebase = pyrebase.initialize_app(config.dbconfig)
    auth = firebase.auth() 
    user = auth.sign_in_with_email_and_password(config.email, config.password)
    db = firebase.database() 
    logging.info("Database connection established...")
except Exception as e: 
    logging.error(e) 
    email.alert_email("(patches_helper.init - connecting to DB)\n\n" + str(e)) 
    sms.alert_sms("(patches_helper.init - connecting to DB)")
    sys.exit() 

# -------- END GLOBALS ----------

def submit(game, platform, link, name):
    response = None
    while response == None:
        try:
            # response = reddit.subreddit("patchnotes").submit(formatTitle(game, name, platform), url=link)
            # response.reply("Please message me if something is wrong with this post or you have any suggestions!")
            postToDB(user, link)
            logging.info(name + "' logged.")
            response = "Safeguard"
        except Exception as e:
            if e.error_type == 'RATELIMIT':
                logging.warning(e.message)
            else:
                logging.error(e)
                email.alert_email("(patches_helper.submit)\n\n" + str(e)) 
                sms.alert_sms("(patches_helper.submit)")
                sys.exit() 
            time.sleep(30)
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
        db.child("shortLinks").push({"link": data}, user['idToken'])
    except Exception as e:
        logging.error(e)
        email.alert_email("(patches_helper.postToDB)\n\n" + str(e)) 
        sms.alert_sms("(patches_helper.postToDB)")
        sys.exit() 
    logging.info("Database post successful!") 

def getPostsFromDB(user): 
    logging.info("Getting link data from database...")
    try: 
        user = auth.refresh(user['refreshToken'])
        data = db.child("shortLinks").get()
        if data.pyres != '':
            for link in data.each():
                savedHrefs.append(link.item[1]['link'])
    except Exception as e:
        logging.error(e)
        email.alert_email("(patches_helper.getPostsFromDB)\n\n" + str(e)) 
        sms.alert_sms("(patches_helper.getPostsFromDB)")
        sys.exit() 
    logging.info("Database retrieval successful!") 

def getSavedHrefs():
    # Method used to get USER variable, which is not available to getPostsFromDB
    # TODO: Figure out why USER variable isn't avaialble to getPostsFromDB
    getPostsFromDB(user) 
    return savedHrefs

def shortenUrl(url): 
    try: 
        post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + config.apiKey
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        return requests.post(post_url, data=json.dumps(payload), headers=headers).json()['id']
    except Exception as e: 
        logging.error(e)
        sys.exit() 
    