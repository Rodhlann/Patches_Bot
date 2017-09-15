import praw
import time
import datetime as dt
import json
import sys 
import os 
from praw.exceptions import APIException

# 1 Month 
submission_interval = time.mktime((dt.date.today() - dt.timedelta(30)).timetuple())
foundPosts = []

try: 
    reddit = praw.Reddit('bot1')
    reddit.user.me()
except Exception as e:
    print ("[UNCAUGHT ERROR] " + e.message)
    sys.exit() 

pubg = reddit.subreddit('pubattlegrounds')
heroes = reddit.subreddit('heroesofthestorm')
lol = reddit.subreddit('leagueoflegends')
wow = reddit.subreddit('wow')

def main():
    getFoundPosts() 
    print ("[INFO] Initiating search")

    # PUBG
    print ("[INFO] Finding patch notes for PUBG...")
    submissions = pubg.submissions(start=submission_interval)
    for submission in submissions:
        if ('Early Access -'.lower() in submission.title.lower() 
            and 'Update'.lower() in submission.title.lower() 
            and 'http://steamcommunity.com/games/578080/announcements' in submission.url.lower()):
            if submission.id not in foundPosts: 
                submit("PlayerUnknown's Battlegrounds", "PC", submission)
            else: 
                print ("[INFO] Most recent post for PUBG already found...")
            break    
    # HEROES
    print ("[INFO] Finding patch notes for HotS...")
    submissions = heroes.submissions(start=submission_interval)
    for submission in submissions:
        if ('us.battle.net'.lower() in submission.url.lower() 
            and 'heroes-of-the-storm-patch-notes' in submission.url.lower()):
            if submission.id not in foundPosts: 
                submit("Heroes of the Storm", "PC", submission)
            else:
                print ("[INFO] Most recent post for HotS already found...")
            break
    # LoL
    print ("[INFO] Finding patch notes for LoL...")
    submissions = lol.submissions(start=submission_interval)
    for submission in submissions:
        if ('leagueoflegends.com/en/news/game-updates/patch/'.lower() in submission.url.lower()):
            if submission.id not in foundPosts: 
                submit("League of Legends", "PC", submission)
            else:
                print ("[INFO] Most recent post for LoL already found...")
            break
    # LoL - PBE
    print ("[INFO] Finding patch notes for LoL - PBE...")
    submissions = lol.submissions(start=submission_interval)
    for submission in submissions:
        if ('surrenderat20'.lower() in submission.url.lower() 
        and '-pbe-update'.lower() in submission.url.lower()):
            if submission.id not in foundPosts: 
                submit("League of Legends - PBE", "PC", submission)
            else: 
                print ("[INFO] Most recent post for LoL - PBE already found...")
            break
    # WoW
    print ("[INFO] Finding patch notes for World of Warcraft...")
    submissions = wow.submissions(start=submission_interval)
    for submission in submissions:
        if ('Patch Notes - WoW'.lower() in submission.title.lower() 
        and 'worldofwarcraft.com' in submission.url.lower() 
        and 'world-of-warcraft' in submission.url.lower() 
        and 'patch-notes' in submission.url.lower()):
            if submission.id not in foundPosts:
                submit("World of Warcraft", "PC", submission)
            else:
                print ("[INFO] Most recent post for World of Warcraft already found...")
            break

    print ("[INFO] Finished finding patch notes!")

def submit(game, platform, submission): 
    usedIds = open("posts.txt", "a")
    response = None 
    while(response == None): 
        try: 
            response = reddit.subreddit("patchnotes").submit(formatTitle(game, submission.title, platform), url=submission.url)
            response.reply("Originally posted by " + submission.author.name + "\n\nPlease message me if something is wrong with this post or you have any suggestions!")
            usedIds.write(submission.id + '\n')
            print ("[INFO] Id '"+submission.id+"' logged.")
        except APIException as e:
            if e.error_type == 'RATELIMIT':
                sys.stdout.write("[WARNING] %s%%   \r"%(e))
                sys.stdout.flush()
            else: 
                print ("[API ERROR] " + e.message)
                sys.exit()
            time.sleep(30) 
        except Exception as e: 
            print ("[UNCAUGHT ERROR] " + e.message)
            sys.exit() 
    print ("")
    print ("[INFO] Submission for " + game + " done!")
    usedIds.close() 

def formatTitle(game, postTitle, platform): 
    date = str(dt.date.today()).replace('-', '/')
    return "["+game+"] ("+date+") ("+platform+") " + postTitle 

def getFoundPosts():
    if os.path.exists("posts.txt"): 
        usedIds = open("posts.txt", "r")
        for id in usedIds:
            foundPosts.append(id.replace('\n', ''))
    else: 
        usedIds = open("posts.txt", "w+") 
    usedIds.close() 

main() 

# TODOs: 
# 1. Find a better system for finding the patch notes outside of title comparison. Too likely to pick up an unintended post 
# 2. Cut down duplicate code 
# 3. Get at least 10 games in catalog 