"""
I'd heard about the concept of sentiment analysis, but never tried it previously.
This is a first attempt at getting to know the basic ideas behind sentiment analysis, mostly based on a tutorial.
Tweepy is a way to easily access the Twitter API in Python, in this script it creates an iterable containing 200 tweets
Textblob then checks every word in the tweet for positive or negative words, and if the score is non zero, the tweet
is qualified as either positive or negative. 
"""

from textblob import TextBlob
import tweepy
import sys

# Importing the Twitter API keys, no you can't see them
mykeys = open(r'C:\Users\harol\Desktop\login.txt', 'r').read().splitlines()
api_key = mykeys[0]
api_secret_key = mykeys[1]
access_token = mykeys[2]
acess_token_secret = mykeys[3]

# Setting up the OAuth handler
auth_handler = tweepy.OAuthHandler(
    consumer_key=api_key, consumer_secret=api_secret_key)
auth_handler.set_access_token(access_token, acess_token_secret)


api = tweepy.API(auth_handler)
search_term = "Covid-19"
tweet_number = 200

tweets = tweepy.Cursor(api.search, q=search_term,
                       lang='en').items(tweet_number)

tweetlist = []
polarity = 0
positive = 0
neutral = 0
negative = 0
# Clean up the tweeterinos (@ and RT)
# And then print them
for tweet in tweets:
    final_text = tweet.text.replace("RT", "")
    if final_text.startswith(" @"):
        position = final_text.index(":")
        final_text = final_text[position+2:]
        tweetlist.append(final_text)
    if final_text.startswith("@"):
        position = final_text.index("")
        final_text = final_text[position+2:]
        tweetlist.append(final_text)

    # Use TextBlob for sentiment analysis
    # Every word gets a score and the score per search term is aggregated
    analysis = TextBlob(final_text)
    tweet_polarity = analysis.polarity
    if tweet_polarity > 0.00:
        positive += 1
    elif tweet_polarity < 0.00:
        negative += 1
    elif tweet_polarity == 0.00:
        neutral += 1
    polarity += tweet_polarity

# Save the cleaned Tweets
with open(r'C:\Users\harol\Desktop\covidoutput.txt', 'w', encoding='utf-8') as f:
    for tweet in tweetlist:
        f.write('%s\n' % tweet)

print(polarity)
print(f"Number of positive tweets: {positive}")
print(f"Number of negative tweets: {negative}")
print(f"Number of neutral tweets: {neutral}")
