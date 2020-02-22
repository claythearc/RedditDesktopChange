##PSBATTLE BACKGROUND 

Hello fellow nerds - I wrote a python script to change my desktop background to a random photoshop from /r/PhotoshopBattles.

Written and tested on Python 3.6, but should work on most versions of Python3

This is kinda hacky atm and no plans to really clean it up, but here it is :)

-Python packages needed:

 - Praw (Reddit Wrapper)
 - Pillow (Imaging library)
 - Requests (web requests)
 
 Step 1: Generate reddit app here https://www.reddit.com/prefs/apps
 
 Step 2: Add CLient ID and Client Secret to environment variables REDDIT_ID and REDDIT_SECRET
 
 Once installed with `pip install Praw Pillow Requests` it's as simple as `python scrape.py`
 
   