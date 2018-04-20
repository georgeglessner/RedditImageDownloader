#!/usr/bin/env python
'''

Reddit Image Downloader

Usage: download_images.py [-s SUBREDDIT] [-n NUMBER OF PICTURES] [-q SEARCH QUERY]

-h --help                           show this
-s --subreddit SUBREDDIT            specify subreddit
-n --number NUMBER OF PICTURES      specify number of pictures to download [default: 20]
-q --query SEARCH QUERY             specify a specific search term

'''

import praw
from credentials import *
import urllib
from prawcore import NotFound
from prawcore import PrawcoreException
import sys
import os
import signal
from docopt import docopt


def main():
    # initialize variables
    subreddit = ''
    num_pics = 0

    # handle 'ctrl + c' if downloads takes too long
    def sigint_handler(signum, frame):
        print '\nQuitting...'
        sys.exit(1)

    signal.signal(signal.SIGINT, sigint_handler)

    # connect to reddit
    reddit = praw.Reddit(
        client_id=ID,
        client_secret=SECRET,
        password=PASSWORD,
        user_agent=AGENT,
        username=USERNAME)

    # get values of arguments
    subreddit = arguments.get('--subreddit')
    num_pics = int(arguments.get('--number'))
    search_term = arguments.get('--query')

    # prompt for a subreddit if none given
    if subreddit == None:
        while True:
            # obtain subreddit to download images from, and number of images to download
            subreddit = raw_input('Please enter subreddit: ')

            # check that subreddit exists
            try:
                reddit.subreddits.search_by_name(subreddit, exact=True)
                break
            except NotFound:
                print 'Subreddit %s does not exist.' % subreddit

    # determine what to search
    if search_term == None:
        results = reddit.subreddit(subreddit).hot()
    else:
        results = reddit.subreddit(subreddit).search(
            search_term, params={'nsfw': 'yes'})

    # create images folder if one does not exits
    if not os.path.exists('./images'):
        os.mkdir('./images')

    # find images/gifs in subreddit
    try:
        count = 1
        for submission in results:
            if count <= num_pics:
                if 'https://i.imgur.com/' in submission.url or 'https://i.redd.it' in submission.url:
                    img_url = submission.url
                    _, extension = os.path.splitext(img_url)
                    if extension in ['.jpg', '.gif', '.jpeg', '.png']:
                        print '\nDownloading', subreddit + str(
                            count) + extension
                        print 'Source:', img_url
                        print 'Comments: https://www.reddit.com/r/' + subreddit + '/' + str(
                            submission)
                        urllib.urlretrieve(img_url, 'images/%s%i%s' %
                                           (subreddit, count, extension))
                        count += 1
                    # .gifv file extensions do not play, convert to .gif
                    elif extension == '.gifv':
                        print '\nDownloading', subreddit + str(count) + '.gif'
                        print 'Source:', img_url
                        print 'Comments: https://www.reddit.com/r/' + subreddit + '/' + str(
                            submission)
                        root, _ = os.path.splitext(img_url)
                        img_url = root + '.gif'
                        urllib.urlretrieve(img_url, 'images/%s%i%s' %
                                           (subreddit, count, '.gif'))
                        count += 1
                if 'https://thumbs.gfycat.com/' in submission.url:
                    img_url = submission.url
                    print '\nDownloading', subreddit + str(count) + '.gif'
                    print 'Source:', img_url
                    print 'Comments: https://www.reddit.com/r/' + subreddit + '/' + str(
                        submission)
                    urllib.urlretrieve(img_url, 'images/%s%i%s' %
                                       (subreddit, count, '.gif'))
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
                    print '\nDownloading', subreddit + str(count) + '.gif'
                    print 'Source:', img_url
                    print 'Comments: https://www.reddit.com/r/' + subreddit + '/' + str(
                        submission)
                    urllib.urlretrieve(img_url, 'images/%s%i%s' %
                                       (subreddit, count, '.gif'))
                    count += 1
            else:
                print '\nCompleted!\n'
                break

    except PrawcoreException:
        print '\nError accessing subreddit!\n'


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main()
