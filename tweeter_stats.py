"""
 * Tweeter Stats: Collects some interesting stats of a Twitter user
 * Copyright (C) 2015  Amit Shekhar Bongir  amitbongir@yahoo.in
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see <http://www.gnu.org/licenses/> or
 * write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 * Boston MA 02110-1301, USA.
 *****************************************************************************/
"""
import tweepy
import json
import os
import stat
import re

class TwitterUser:
	def __init__(self, api, username=u'', retweets=False):
		self._data = {}
		self._tweets = []
		self._latestCount = 0
		while not username:
			username = input("Enter username: ")
		self._data['username'] = username
		print("Fetching "+username+"'s tweets")
		print("Please wait ...")
		if self.readFile():
			if not self.getLatestTweets(api):		
				os.chdir("../")
				return
		else:
			if not self.getAllTweets(api):
				os.remove(self._fname)
				os.chdir("../")
				return
			self._data['mostRetweeted'] = [{'text':u'', 'count':-1}] * 3
			self._data['tweetWords'] = {}
			self._data['hashtags'] = {}
			self._data['popularTw'] = [u''] * 3
			self._data['popularH'] = [u''] * 3
			self._data['pTwCount'] = 0
			self._data['pHCount'] = 0
		latestTweet = json.loads(json.dumps(self._tweets[0]._json))
		self._data['tweetCount'] = latestTweet['user']['statuses_count']
		self._data['followersCount'] = latestTweet['user']['followers_count']
		self._data['friendsCount'] = latestTweet['user']['friends_count']
		self._data['location'] = latestTweet['user']['location']
		self.mostRetweetedTweets(retweets)
		if self._latestCount:
			self.collectTwAndH()
			self.popularTwAndH()
		self.saveData()
		os.chdir("../")
		self.displayPopular()
	
	def readFile(self):
		dirName = "Tweeters_Data"
		if not os.path.exists(dirName):
			os.mkdir(dirName)
		os.chdir(dirName)
		self._fname = self._data['username'] + '_stats.json'
		if not os.path.isfile(self._fname):
			f = open(self._fname, 'w')
			f.close()
			return 0
		else:
			f = open(self._fname, 'r')
			if os.stat(self._fname).st_size:
				self._data = json.loads(f.read())
				f.close()
				return 1
			else:
				f.close()
				return 0
	
	def getAllTweets(self, api):
		try:
			prevTweets = api.user_timeline(self._data['username'], count=200)
		except:
			print("No user with username "+self._data['username']+" exists")
			return 0
		self._data['sinceID'] = prevTweets.since_id
		self._tweets.extend(prevTweets)
		oldest = self._tweets[-1].id - 1
		while len(prevTweets) > 0:
			prevTweets = api.user_timeline(self._data['username'], count=200, max_id=oldest)
			self._tweets.extend(prevTweets)
			oldest = self._tweets[-1].id - 1
		self._latestCount = len(self._tweets)
		return 1
	
	def getLatestTweets(self, api):
		sinceID = self._data['sinceID']
		while True:
			try:
				latestTweets = api.user_timeline(self._data['username'], count=200, since_id=sinceID)
			except:
				print("User "+self._data['username']+" either changed the username or deleted account")
				return 0
			if len(latestTweets):
				sinceID = latestTweets.since_id
				self._latestCount += len(latestTweets)
				self._tweets.extend(latestTweets)
			else:
				break
		if self._latestCount < 200:
			self._tweets.extend(api.user_timeline(self._data['username'], count=200-self._latestCount, max_id=self._data['sinceID']))
		self._data['sinceID'] = sinceID
		return 1

	def mostRetweetedTweets(self, retweets):
		latestCnt = self._latestCount
		self._latestTweetsData = []
		for tweet in self._tweets:
			if latestCnt:
				tweetJson = json.dumps(tweet._json)
				if not retweets and 'retweeted_status' in tweetJson:
					continue
				self._latestTweetsData.append(json.loads(tweetJson))
				latestCnt -= 1
			i = 0
			while i < 3:
				if tweet.retweet_count > self._data['mostRetweeted'][i]['count']: 
					break
				i += 1
			if i < 3:
				tweetText = tweet.text
				if tweetText[0:3] == "RT ":
					tweetText = tweetText[3:]
				self._data['mostRetweeted'].insert(i, {'text':tweetText, 'count':tweet.retweet_count})
				self._data['mostRetweeted'].pop()

	def collectTwAndH(self):
		tweetsText = u''
		for tweet in self._latestTweetsData:
			tweetsText += tweet['text'] + u' '
			tweetHashtags = tweet['entities']['hashtags']
			if tweetHashtags:
				for hashtag in tweetHashtags:
					hashtagText = hashtag['text'].lower()
					if hashtagText in self._data['hashtags']:
						self._data['hashtags'][hashtagText] += 1
					else:
						self._data['hashtags'][hashtagText] = 1
		tweetsText = tweetsText.lower()
		for tweetText in tweetsText.split():
			if "http" in tweetText:
				tweetText = tweetText[0:tweetText.index("http")]
			words = (re.sub('[^0-9a-zA-z_]+', ' ', tweetText)).split()
			for word in words:
				if word not in self._data['hashtags']:
					if word in self._data['tweetWords']:
						self._data['tweetWords'][word] += 1
					else:
						self._data['tweetWords'][word] = 1

	def popularTwAndH(self):
		twk = list(self._data['tweetWords'].keys())
		twv = list(self._data['tweetWords'].values())
		hk = list(self._data['hashtags'].keys())
		hv = list(self._data['hashtags'].values())

		i = twCount = hCount = 0
		while i < 3:
			if twk:
				maxWIndex = twv.index(max(twv))
				self._data['popularTw'][twCount] = twk[maxWIndex]
				twk.remove(twk[maxWIndex])
				twv.remove(twv[maxWIndex])
				twCount += 1
			if hk:
				maxHIndex = hv.index(max(hv))
				self._data['popularH'][hCount] = hk[maxHIndex]
				hk.remove(hk[maxHIndex])
				hv.remove(hv[maxHIndex])
				hCount += 1
			i += 1
		self._data['pTwCount'] = twCount
		self._data['pHCount'] = hCount

	def saveData(self):
		os.chmod(self._fname, stat.S_IWUSR)
		f = open(self._fname, 'w')
		json.dump(self._data, f, ensure_ascii=False)
		f.close()
		os.chmod(self._fname, stat.S_IRUSR)

	def displayPopular(self):
		print("\n3 most retweeted tweets:\n")
		for i in range(0, 3):
			print(self._data['mostRetweeted'][i]['text'])
			print("Retweet count: " + str(self._data['mostRetweeted'][i]['count']) + "\n")
		print('\n'+str(self._data['pTwCount'])+" most used tweet words\n")
		for i in range(0, self._data['pTwCount']):
			tw = self._data['popularTw'][i]
			print(tw + " - " + str(self._data['tweetWords'][tw]) + " times")
		print('\n\n' + str(self._data['pHCount']) + " most used hashtags\n")
		for i in range(0, self._data['pHCount']):
			h = self._data['popularH'][i]
			print('#' + h + " - " + str(self._data['hashtags'][h]) + " times")
		print('')

	#Returns all collected data to an external user of this class
	def getData(self):
		return self._data

if __name__ == "__main__":

	access_token = "access_token_here"
	access_token_secret = "access_token_secret_here"
	consumer_key = "consumer_key_here"
	consumer_secret = "consumer_secret_here"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	# Pass username="username" as argument to TwitterUser() to avoid entering it at runtime
	# Pass retweets=True to consider retweeted tweets of the user as well. Default is False
	tweeter = TwitterUser(api)

