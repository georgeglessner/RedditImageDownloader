#!/usr/bin/env python

import praw
from credentials import *
import requests
import urllib
from prawcore import NotFound
import sys
import os
import signal

#initialize variables
subreddit = ''
num_pics = 0

# handle 'ctrl + c' if downloads takes too long
def sigint_handler(signum, frame):
    print '\nQuitting...'
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)

# connect to reddit
reddit = praw.Reddit(client_id=ID,
                     client_secret=SECRET,
                     password=PASSWORD,
                     user_agent=AGENT,
                     username=USERNAME)

# create images folder if one does not exits
if not os.path.exists('./images'):
    os.mkdir('./images')

# command line arguments
if len(sys.argv) > 1:
    # check for valid arguments
    if len(sys.argv) != 3:
        print 'invalid number of arguments. Format is "python images.py subreddit number"'
        sys.exit(1)

    # check that subreddit exists
    subreddit = sys.argv[1]
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
        print 'Subreddit %s does not exist.' % subreddit
        sys.exit(1)

    # check that int was input
    try:
        num_pics = int(sys.argv[2])
    except ValueError:
        print("Not a number.")
        sys.exit(1)
else:
    while True:
        # obtain subreddit to download images from, and number of images to download
        subreddit = raw_input('Please enter subreddit: ')

        # check that subreddit exists
        try:
            reddit.subreddits.search_by_name(subreddit, exact=True)
            break
        except NotFound:
            print 'Subreddit %s does not exist.' % subreddit

    while True:
        # get number of pics requested
        num_pics = raw_input('Please enter number of pics: ')

        # check that int was input
        try:
            num_pics = int(num_pics)
            break
        except ValueError:
            print("Not a number.")

count = 0

# find images/gifs in subreddit
for submission in reddit.subreddit(subreddit).hot():
    if count < num_pics:
        if 'https://i.imgur.com/' in submission.url or 'https://i.redd.it' in submission.url:
            img_url = submission.url
            _, extension = os.path.splitext(img_url)
            if extension in ['.jpg', '.gif', '.jpeg', '.png']:
                print 'Downloading...'
                urllib.urlretrieve(img_url, 'images/%s_%s%s' % (subreddit, str(submission.id), extension))
                count += 1
            # .gifv file extensions do not play, convert to .gif
            elif extension == '.gifv':
                print 'Downloading...'
                root, _ = os.path.splitext(img_url)
                img_url = root + '.gif'
                urllib.urlretrieve(img_url, 'images/%s_%s.%s' % (subreddit, str(submission.id), 'gif'))
                count += 1
        if 'https://thumbs.gfycat.com/' in submission.url:
            img_url = submission.url
            print 'Downloading...'
            urllib.urlretrieve(img_url, 'images/%s_%s.%s' % (subreddit, str(submission.id), 'gif'))
            count += 1
        # some gfycat conversions will not work due to capitalizations of link
        if 'https://gfycat.com/' in submission.url:
            img_url = submission.url
            img_url = img_url.split('https://', 1)
            img_url = 'https://thumbs.' + img_url[1]
            if 'gifs/detail/' in img_url:
                img_url = img_url.split('gifs/detail/', 1)
                img_url = img_url[0] + img_url[1]
            root, _ = os.path.splitext(img_url)
            img_url = root + '-size_restricted.gif'
            print 'Downloading...'
            urllib.urlretrieve(img_url, 'images/%s_%s.%s' % (subreddit, str(submission.id[:4]), 'gif'))
            count += 1
    else:
        break

print '\nCompleted!\n'
