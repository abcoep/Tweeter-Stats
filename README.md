# Tweeter Stats

Copyright © 2015 Amit Shekhar Bongir

This is a simple and fun to run script, where stats imply a tweeter's 3 most :  
1) Retweeted tweets  
2) Frequently used hashtags  
3) Frequently used tweet words  
You can also use this script as a module for getting a tweeter's data. See *Use as a module* below.

## Building
This script is compatible with Python 3.4 or higher. It imports 5 modules : tweepy, json, os, stat, re; 4 of which are a part of the Python Library except tweepy, which you may need to install. For Linux based systems type the command:

    sudo apt-get install python-tweepy
    
The script makes use of Twitter's REST API using tweepy to fetch tweeter data. You need to authorize this script as an app in your twitter account to get 4 important things:  
1) Access token  
2) Access token secret  
3) Consumer key  
4) Consumer key secret  
which you will fill in the necessary places in *__main__* in *tweeter_stats.py*. [This](http://iag.me/socialmedia/how-to-create-a-twitter-app-in-8-easy-steps/) site will easily show you the steps to get them. When step 5 is reached, you may fill the application details as follows :  
Name : Tweeter Stats  
Description : Collects some interesting stats of a twitter user  
Website : https://github.com/amitbongir/Tweeter-Stats  

Ensure that the computer is connected to the Internet. Then run the script with :

    python3 tweeter_stats.py
    
In case you are receiving error, please check that you have entered valid username. If yes then check whether you have filled the above 4 tokens/keys properly at the correct places. And check if the Internet connection is established properly. Still the errors popup, then they are actually valid provided a stable version of tweepy is installed.

## Use as a module
You can use this script as a module *tweeter_stats* and use the TweeterUser class defined in it. You can get all the data collected by its objects by calling getData() function defined in it. It returns a Python dict (Refer the file "keys" for the dict's keys.) The data of all users collected through the objects are all saved in JSON format files in *Tweeters_Data* directory (created after atleast one tweeter's data is collected) in read-only format. The files are named in the form of username_stats.json.

## Entering username of tweeter
You can give the username of the tweeter dynamically at runtime or statically as argument to the constructor of the TweeterUser class. (See commented lines in *__main__* in *tweeter_stats.py* for the static arguments)

## Considering retweeted tweets
By default, the script considers only tweets made by the tweeter but not the ones he/she retweeted. By static arguments as discussed above, you can make the script consider the tweets retweeted by the tweeter also.

## Methodology of fetching tweets
1) For a tweeter whose data was not previously collected, all his/her tweets are fetched.  
2) For a tweeter whose data was previously collected, only the tweets that were posted after the previous collected tweets are collected, say n tweets. If n is less than 200, then (200 - n) of the most recent of the previous collected tweets are collected once again. This methodology ensures that we :
* fetch the latest tweets with their current retweet count.  
* save unnecessary downloading and time.

## License
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
