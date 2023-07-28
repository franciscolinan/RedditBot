from reddit import Reddit
from anti_detect import CreateDriver
import undetected_chromedriver as uc
import json
import concurrent.futures
from time import time
import random

def RunBot(bot: Reddit):
    if not bot.GetInitCookies():
        while not bot.GoMainPage():
            print("GoMainPage fail: retrying")

        bot.SetInitCookies(True)

    while not bot.IsloggedIn() and not bot.LogIn():
        print("Failed to login: " + bot.GetUsername() + ":" + bot.GetPassword())

    #Check if its banned

    if (bot.CheckBrowseDuration()):
        bot.ResetBrowseDuration()
        bot.SetBrowseDuration(random.randint(3600, 7200))
        communities = bot.GetBrowseCommunities()
        bot.SetCurrentBrowseCommunity(random.choice(communities))

    elif bot.GetCurrentUrl() != "https://www.reddit.com/" + bot.GetCurrentBrowseCommunity() + "/":
        bot.GoTo(bot.GetCurrentBrowseCommunity())

    #if (time() - bot.GetPostTimestamp() > 60):
        #bot.CreatePost(False, False, False)

    if bot.CheckActionTime():
        if bot.ScrollDown():
            bot.ResetActionTime()
            bot.SetActionDuration(random.randint(1, 8))
    input()

if __name__ == "__main__":
    bots = []

    # Read the config file
    with open('config.json') as file:
        config = json.load(file)

    for key in config:
        profile = config[key]

        driver = CreateDriver(profile)
        
        reddit = Reddit(driver, profile["username"], profile["password"], profile["browse_communities"])
        
        bots.append(reddit)

    # Run bots
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            future_results = [executor.submit(RunBot, bot) for bot in bots]

            # Wait for all tasks to complete
            concurrent.futures.wait(future_results)

    input()