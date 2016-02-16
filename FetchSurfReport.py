#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib.request
import html5lib
import tweepy
from pushover import init, Client

#Twitter API Globals
CONSUMER_KEY = "{Insert CONSUMER KEY}"
CONSUMER_SECRET = "{Insert CONSUMER_SECRET}"
ACCESS_KEY = "{Insert ACCESS KEY}"
ACCESS_SECRET = "{Insert ACCESS SECRET}"

#Pushover API Globals
API_TOKEN = "{Insert API TOKEN}"
USER_KEY = "{Insert USER KEY}"

## Scrape data from Coastalwatch
def get_coastalwatch_report():
	## HTTP GET URL 
	webpage = urllib.request.urlopen("http://www.coastalwatch.com/surf-cams-surf-reports/nsw/cronulla")
	## Loop through surf report retreiving required data.
	soup = BeautifulSoup(webpage, "html5lib")
	for i in soup.select(".surfReport"):

		##Output Current Swell
		for i in soup.select(".today .swell"):
			report = "Current Swell: " + str(i.get_text(strip=True)) + "\n"

		##Output Current Wind Speed
		for i in soup.select(".today .wind .val"):
			report += "Current Wind: " + str(i.get_text(strip=True))

		##Output Current Wind Direction
		for i in soup.select(".today .wind .dir"):
			report += " " + str(i.get_text(strip=True)) + "\n"

		##Output Todays Rating
		for i in soup.select(".surfReport li h4 strong"):
			report += str(i.get_text(strip=True))

		##Output Todays Written Report
		for i in soup.find_all("p", attrs = { "class" : "noMarginBottom" }):
			report += " - " + str(i.get_text(strip=True))

	return(report);

# Tweet report to twitter
def tweet_to_twitter(astring):

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	# Update twitter status as per limit 140 characters
	astring = astring[0:126] + " ..." + " #Cronulla"
	api.update_status(astring[0:140])

# Send report via Pushover notification
def send_to_pushover(astring):
	client = Client(USER_KEY, api_token = API_TOKEN)
	astring = "***Coastalwatch Report***\n" + astring
	client.send_message(astring, sound="bike")

if __name__ == "__main__":
	coastalwatch = get_coastalwatch_report()
	print(coastalwatch)
	##tweet_to_twitter(coastalwatch)
	send_to_pushover(coastalwatch)
