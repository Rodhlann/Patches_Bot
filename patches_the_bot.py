import datetime as dt
import game_data as gd 
import patches_helper as patches
import logging

logging.getLogger('').handlers = []
logging.basicConfig(filename='Patches.log',level=logging.INFO)

def main():

    savedHrefs = patches.getSavedHrefs() 

    logging.info("Initiating search")

    # PUBG
    logging.info("Finding patch notes for PUBG...")
    soup = patches.makeSoup(gd.pubg_url) 
    posts = soup.find_all("a", class_="large_title")
    for post in posts: 
        href = post['href']
        name = post.string
        if(all(string in name.lower() for string in gd.pubg_conditions)):
            if(href not in savedHrefs):
                patches.submit("PlayerUnknown's Battlegrounds", "PC", href, name)
            else: 
                logging.info(name + " already found!")
    # HEROES
    logging.info("Finding patch notes for HotS...")
    soup = patches.makeSoup(gd.hots_url) 
    posts = soup.find_all(class_="news-list__item__title")
    for post in posts:
        href = "http://us.battle.net" + post.find('a')['href']
        name = post.find('a').string.replace('\n', '')
        if(any(string in href.lower() for string in gd.hots_conditions)):
            if(href not in savedHrefs): 
                logging.info("Submitting: " + name)
                patches.submit("Heroes of the Storm", "PC", href, name) 
            else:
                logging.info(name + " already found!")
    # LoL
    logging.info("Finding patch notes for LoL...")
    soup = patches.makeSoup(gd.lol_url) 
    posts = soup.find_all("h4")
    for post in posts:
        href = "http://eune.leagueoflegends.com/" + post.find('a')['href']
        name = post.find('a').string.replace('\n', '')
        if(any(string in href.lower() for string in gd.lol_conditions)):
            if(href not in savedHrefs): 
                logging.info("Submitting: " + name)
                patches.submit("League of Legends", "PC", href, name) 
            else:
                logging.info(name + " already found!")
    # WoW
    logging.info("Finding patch notes for WoW...")
    soup = patches.makeSoup(gd.wow_url) 
    posts = soup.find_all("div", class_="NewsBlog-content")
    for post in posts:
        href = "https://worldofwarcraft.com/en-gb/news" + post.find('a')['href']
        name = post.find(class_="NewsBlog-title").string.replace('\n', '')
        if(any(string in href.lower() for string in gd.wow_conditions)):
            if(href not in savedHrefs): 
                logging.info("Submitting: " + name)
                patches.submit("World of Warcraft", "PC", href, name) 
            else:
                logging.info(name + " already found!")
    # CS:GO
    logging.info("Finding patch notes for CS:GO")
    soup = patches.makeSoup(gd.csgo_url) 
    posts = soup.find_all("div", class_="inner_post")
    for post in posts:
        href = post.find('h2').find('a')['href']
        name = post.find('h2').find('a').string.replace('\n', '')
        if(any(string in name.lower() for string in gd.csgo_conditions)):
            if(href not in savedHrefs): 
                logging.info("Submitting: " + name)
                patches.submit("Counter Strike: Global Offensive", "PC", href, name) 
            else:
                logging.info(name + " already found!")

    logging.info("Finished finding patch notes!")

logging.info("-------------------"+str(dt.datetime.today())+"-------------------") 
main() 

# TODOs: 
# 1. Cut down duplicate code 
# 2. Get at least 10 games in catalog 