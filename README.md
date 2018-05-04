# Reddit Image Downloader

A reddit application that downloads pictures and gifs from a given subreddit.

# Setup 
1. Create a [reddit personal use script application](https://www.reddit.com/prefs/apps/).

2. Add a `credentials.py` file to your working directory and add your applications credentials.

		ID='YOUR_ID'  
		SECRET='YOUR_SECRET'  
		PASSWORD='YOUR_PASSWORD'  
		AGENT='Example Bot by /u/example_bot'  
		USERNAME='YOUR_USERNAME'  

3. Run `pip install -r requirements.txt`

# Usage


	Usage: download_images.py [-s SUBREDDIT] [-n NUMBER OF PICTURES] [-p PAGE] [-q SEARCH QUERY] 

	-h --help                           show this
	-s --subreddit SUBREDDIT            specify subreddit
	-n --number NUMBER OF PICTURES      specify number of pictures to download [default: 20]
	-p --page PAGE                      hot, top, controversial, new, rising [default: hot]
	-q --query SEARCH QUERY             specify a specific search term


Your images will appear in the "images" folder created by the application.

__Helpful note:__ To view .gif files on a Mac select the image(s) and press "cmd" + "y".


