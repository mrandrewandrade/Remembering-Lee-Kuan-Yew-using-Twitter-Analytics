import sys
import jsonpickle
import os
import tweepy
 
# API_KEY and API_SECRET removed
auth = tweepy.AppAuthHandler("", "")

# Ensure tweepy waits on API rate limits
api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)
  
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

#search query
search_query = 'Lee Kuan Yew'

# Some arbitrary large number not to limit search
max_tweets = 10000000
# Max tweets per query the API permits
tweets_per_qry = 100
# File to store the tweets
output_file_name = 'Lee_Kuan_Yew.txt' 
 
 
# Start scraping from a specific start ID (lower limit = start_id)
# Else go as far back as API allows (no lower limit)
start_id = None 
 
# If results are below a specific ID, set max_id to that ID.
# else start from the most recent tweet (no upper limit)
max_id = -1L
 
tweet_count = 0

print("Downloading max {0} tweets".format(max_tweets))

with open(output_file_name, 'w') as f:
    while tweet_count < max_tweets:
        try:
            if (max_id <= 0):
                if (not start_id):
                    new_tweets = api.search(q=search_query, count=tweets_per_qry)
                else:
                    new_tweets = api.search(q=search_query, count=tweets_per_qry,
                                            since_id=start_id)
            else:
                if (not start_id):
                    new_tweets = api.search(q=search_query, count=tweets_per_qry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=search_query, count=tweets_per_qry,
                                            max_id=str(max_id - 1),
                                            since_id=start_id)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                #dump the tweets into JSON format
                f.write(jsonpickle.encode(tweet._json) +
                        '\n')
            tweet_count += len(new_tweets)
            print("Downloaded {0} tweets".format(tweet_count))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
           #sometimes twitter is over capacity so sleep then continue
            if e.reason == "[{u'message': u'Over capacity', u'code': 130}]":
                sleep(2)
                continue 
            # Exit if any other type of error break and indicate error
            print("some error : " + str(e))
            break
 
print ("Downloaded {0} tweets, Saved to {1}".format(tweet_count, output_file_name))

