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
lol_url = "http://eune.leagueoflegends.com/en/news/game-updates"
lol_conditions = ['/game-updates/patch/patch-']
lol_pbe_url="http://www.surrenderat20.net/search/label/PBE/"
lol_pbe_conditions = ['-pbe-update']

# WoW
wow_url = "https://worldofwarcraft.com/en-gb/news/"
wow_conditions = ['patch-notes', 'hotfixes']

# CS:GO
csgo_url = "http://blog.counter-strike.net/index.php/category/updates/"
csgo_conditions = ['release notes for'] 

# -------- END GLOBALS ----------

def main():
    getSavedHrefs() 
    logging.info("-------------------"+str(dt.datetime.today())+"-------------------") 
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
    # LoL
    logging.info("Finding patch notes for LoL...")
    soup = makeSoup(lol_url) 
    posts = soup.find_all("h4")
    for post in posts:
        href = "http://eune.leagueoflegends.com/" + post.find('a')['href']
        name = post.find('a').string.replace('\n', '')
        if(any(string in href.lower() for string in lol_conditions)):
            if(href not in savedHrefs): 
                logging.info("Submitting: " + name)
                submit("League of Legends", "PC", href, name) 
            else:
                logging.info(name + " already found!")
    # # LoL - PBE
    # logging.info("Finding patch notes for LoL - PBE...")
    # soup = makeSoup(lol_pbe_url) 
    # posts = soup.find_all("h1", class_="news-title")
    # for post in posts:
    #     href = post.find('a')['href']
    #     name = post.find('a').string.replace('\n', '')
    #     if(any(string in href.lower() for string in lol_pbe_conditions)):
    #         if(href not in savedHrefs): 
    #             logging.info("Submitting: " + name)
    #             submit("League of Legends - PBE", "PC", href, name) 
    #         else:
    #             logging.info(name + " already found!")
    # # WoW
    logging.info("Finding patch notes for WoW...")
    soup = makeSoup(wow_url) 
    posts = soup.find_all("div", class_="NewsBlog-content")
    for post in posts:
        href = "https://worldofwarcraft.com/en-gb/news" + post.find('a')['href']
        name = post.find(class_="NewsBlog-title").string.replace('\n', '')
        if(any(string in href.lower() for string in wow_conditions)):
            if(href not in savedHrefs): 
                logging.info("Submitting: " + name)
                submit("World of Warcraft", "PC", href, name) 
            else:
                logging.info(name + " already found!")
    #CS:GO
    logging.info("Finding patch notes for CS:GO")
    soup = makeSoup(csgo_url) 
    posts = soup.find_all("div", class_="inner_post")
    for post in posts:
        href = post.find('h2').find('a')['href']
        name = post.find('h2').find('a').string.replace('\n', '')
        if(any(string in name.lower() for string in csgo_conditions)):
            if(href not in savedHrefs): 
                logging.info("Submitting: " + name)
                submit("Counter Strike: Global Offensive", "PC", href, name) 
            else:
                logging.info(name + " already found!")

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
    # NOTE: User agent prevents sites from blocking the bot 
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with request.urlopen(req) as page:
        page_body = page.read()
    return BeautifulSoup(page_body, 'html.parser')

main() 

# TODOs: 
# 1. Find a better system for finding the patch notes outside of title comparison. Too likely to pick up an unintended post ----?
# 2. Cut down duplicate code 
# 3. Get at least 10 games in catalog 