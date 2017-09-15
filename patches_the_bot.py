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

logging.basicConfig(filename='Patches.log',level=logging.INFO)

# -------- START GLOBALS ----------

savedHrefs = []

try: 
    reddit = praw.Reddit('bot1')
    reddit.user.me()
except Exception as e:
    logging.error(e.message)
    sys.exit() 

# PUBG
pubg_url = "http://steamcommunity.com/games/578080/announcements"
pubg_conditions = ['early access -', 'update']

# HotS
hots_url = "http://us.battle.net/heroes/en/blog/"
hots_conditions = ['heroes-of-the-storm-patch', 'heroes-of-the-storm-hotfix', 'heroes-of-the-storm-balance']

# LoL
lol = reddit.subreddit('leagueoflegends')

# WoW
wow = reddit.subreddit('wow')

# CS:GO
csgo = reddit.subreddit('csgo') 

# -------- END GLOBALS ----------

def main():
    getSavedHrefs() 
    logging.info("Initiating search")

    # PUBG
    logging.info("Finding patch notes for PUBG...")
    soup = makeSoup(pubg_url) 
    posts = soup.find_all("a", class_="large_title")
    for post in posts: 
        href = post['href']
        name = post.string
        if(all(string in name.lower() for string in pubg_conditions)):
            if(href not in savedHrefs):
                submit("PlayerUnknown's Battlegrounds", "PC", href, name)
            else: 
                logging.info(name + " already found!")

    # HEROES
    logging.info("Finding patch notes for HotS...")
    soup = makeSoup(hots_url) 
    posts = soup.find_all(class_="news-list__item__title")
    for post in posts:
        href = "http://us.battle.net" + post.find('a')['href']
        name = post.find('a').string.replace('\n', '')
        if(any(string in href.lower() for string in hots_conditions)):
            if(href not in savedHrefs): 
                logging.info("Submitting: " + name)
                submit("Heroes of the Storm", "PC", href, name) 
            else:
                logging.info(name + " already found!")
    # # LoL
    # logging.info("Finding patch notes for LoL...")
    # submissions = lol.submissions(start=submission_interval)
    # for submission in submissions:
    #     if ('leagueoflegends.com/en/news/game-updates/patch/'.lower() in submission.url.lower()):
    #         if submission.id not in foundPosts: 
    #             submit("League of Legends", "PC", submission)
    #         else:
    #             logging.info("Most recent post for LoL already found...")
    #         break
    # # LoL - PBE
    # logging.info("Finding patch notes for LoL - PBE...")
    # submissions = lol.submissions(start=submission_interval)
    # for submission in submissions:
    #     if ('surrenderat20'.lower() in submission.url.lower() 
    #     and '-pbe-update'.lower() in submission.url.lower()):
    #         if submission.id not in foundPosts: 
    #             submit("League of Legends - PBE", "PC", submission)
    #         else: 
    #             logging.info("Most recent post for LoL - PBE already found...")
    #         break
    # # WoW
    # logging.info("Finding patch notes for World of Warcraft...")
    # submissions = wow.submissions(start=submission_interval)
    # for submission in submissions:
    #     if ('Patch Notes - WoW'.lower() in submission.title.lower() 
    #     and 'worldofwarcraft.com' in submission.url.lower() 
    #     and 'world-of-warcraft' in submission.url.lower() 
    #     and 'patch-notes' in submission.url.lower()):
    #         if submission.id not in foundPosts:
    #             submit("World of Warcraft", "PC", submission)
    #         else:
    #             logging.info("Most recent post for World of Warcraft already found...")
    #         break
    # #CS:GO
    # logging.info("Finding patch notes for CS:GO")
    # submissions = csgo.submissions(start=submission_interval)
    # for submission in submissions:
    #     if ('CS:GO Update: Release Notes for'.lower() in submission.title.lower()
    #     and 'blog.counter-strike.net/index.php' in submission.url.lower()):
    #         if submission.id not in foundPosts:
    #             submit("Counter Strike: Global Offensive", "PC", submission)
    #         else:
    #             logging.info("Most recent post for CS:GO already found...")
    #         break

    logging.info("Finished finding patch notes!")

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

def makeSoup(url): 
    page_body = ""
    with request.urlopen(url) as page:
        page_body = page.read()
    return BeautifulSoup(page_body, 'html.parser')

main() 

# TODOs: 
# 1. Find a better system for finding the patch notes outside of title comparison. Too likely to pick up an unintended post ----?
# 2. Cut down duplicate code 
# 3. Get at least 10 games in catalog 