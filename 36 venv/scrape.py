"""
This goes and scrapes the subreddit defined in the sub constant. It looks for comments containing an imgur link and
sets the users background to that image. While this is the correct format for photoshop battles, it may be different
for other subreddits and that change is left as an exercise to the reader
"""

import praw
import ctypes
import random
import re
import requests
import os
from PIL import Image
import time

# CONSTANTS
user32 = ctypes.windll.user32
sub = 'photoshopbattles'
SPI_SETDESKWALLPAPER = 0x14     #which command (20)
SPIF_UPDATEINIFILE   = 0x0
attempts = 0
jpgsrc = 'wallpaper.jpg'
pngsrc = 'wallpaper.png'
abspath = os.getcwd()
jpg_fp = os.path.join(abspath , jpgsrc)
png_fp = os.path.join(abspath, pngsrc)


reddit = praw.Reddit(user_agent='Desktop Changer',
                     client_id=os.environ['REDDIT_ID'],
                     client_secret=os.environ['REDDIT_SECRET'])


def parse_imgur_url(url):
    """Imgur regex"""
    return re.search(r'(https?\://(.*)imgur\.com/[^\)]+)', url).group(1)


if __name__ == "__main__":
    post = reddit.subreddit(sub).random()
    while True:
        if attempts > 5:
            "if we fail 5 times, every post is probably deleted. move to next post"
            attempts = 0
            post = reddit.subreddit(sub).random()
        rand_comment = random.choice(post.comments.list())
        try:
            """
            This is kinda garbage and hacky but essentially, look for imgur in the comment body,
            passs it off to the regex object, add .jpg to the end of it if it doesn't have it 
            See if the file size is >2kb (the image for deleted imgur post is 1kb... usually
            then try to convert it to png with pillow (corrupted images will fail & throw exception)
            then make it into a desktop image
            sleep until next time
            """
            if 'imgur' in rand_comment.body:
                attempts += 1
                url = parse_imgur_url(rand_comment.body)
                if url.endswith('jpg'):
                    r = requests.get(url)
                else:
                    r = requests.get(url + '.jpg')
                with open(jpgsrc, "wb") as f:
                    f.write(r.content)
                if os.path.getsize(jpg_fp) > 2000:
                    try:
                        Image.open(jpg_fp).save(png_fp)
                    except Exception as e:
                        continue
                    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 1, png_fp, SPIF_UPDATEINIFILE)
                    # the 1 is a constant for 'fit' mode of images. thia makes it so the full thing appears, with black
                    # bars to make it fit if needed.
                    time.sleep(3600)
                else:
                    attempts += 1
                    continue
            if 'that are not a photoshop' in rand_comment.body:
                #magic string for catching automod
                attempts += 1
        except Exception as e:
            """
            Just some thing to make sure we don't get stuck looking at a bad post forever - things that could cause
            exceptions here are - the regex failing, file writing failing, bad internets maybe?
            """
            attempts += 1






