"""
    instabot example
    Workflow:
        Like last images with hashtag.
"""

import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

hashtags = ["#doglife", "#doglove",
            "#puppy", "#dogstagraming", "#cutedog",
            "#doglovers", "#doggie", "#mydogiscutest",
            "#dogs", "#dogsofinstagram", "#dogsofinstaworld",
            "#dogoftheday", "#doginstagram", "#dogslife",
            "#dogsofinstgram", "#dogsofinsta", "#dogs_of_instagram",
            "#insta_dogs", "#instagramdog", "#lovedogs"]

u = "iam.dawg"
p = "!iamdawg@123"


bot = Bot()
bot.login(username=u, password=p, proxy=None)

wait = 5 * 60  # in seconds

while True:
    for hashtag in hashtags:
        bot.like_hashtag(hashtag)
    time.sleep(wait)