"""
    instabot example
    Workflow:
        Like user's, follower's media by user_id.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

u = "iam.dawg"
p = "!iamdawg@123"

users = ["dogsofinstagram", "dogs.lovers", "pupps.paws.pupps", "doggosbeingdoggos"]

bot = Bot()
bot.login(username=u, password=p, proxy=None)

for username in users:
    bot.like_followers(username, nlikes=3)
