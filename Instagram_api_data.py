import instaloader
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

L = instaloader.Instaloader()
""" username = "jim_desai"
password = "lifeyoga"
try:
    L.login(username, password)  # Attempt initial login
except instaloader.TwoFactorAuthRequiredException:
    two_factor_code = input("Enter 2FA code: ")
    L.two_factor_login(two_factor_code) """
artist_name = 'emiwaybantai'
artist = artist_name
profile = instaloader.Profile.from_username(L.context, artist)
posts = profile.get_posts()
hashtags = {}
sentiments = []
artist_mentions = {}
for post in posts:
    caption = post.caption
    # Extract hashtags
    hashtags.update({hashtag:hashtags.get(hashtag, 0) + 1 for hashtag in post.caption_hashtags})
    # Analyze sentiment
    if caption is not None:
        sentiment = SentimentIntensityAnalyzer().polarity_scores(caption)["compound"]
        sentiments.append(sentiment)
        if artist in caption:
            artist_mentions[artist] = artist_mentions.get(artist, 0) + 1

artist_counts = sum(artist_mentions.values())
hashtag_counts = sum(hashtags.values())
average_sentiment = sum(sentiments) / len(sentiments)
artist_fan_data = pd.DataFrame({'artist_counts':artist_counts,'hashtag_counts':hashtag_counts,'sentiment_score':average_sentiment}, index = [artist_name])
print(artist_fan_data)

""" import pandas as pd
import instaloader
from nltk.sentiment import SentimentIntensityAnalyzer
import csv

def instaauth(username,password):
        L = instaloader.Instaloader()
        try:
            L.login(username, password)  # Attempt initial login
        except instaloader.TwoFactorAuthRequiredException:
            two_factor_code = input("Enter 2FA code: ")
            L.two_factor_login(two_factor_code)
        return L

def fan_engagement_data(i,j,L,artist_instdata):
        for row in artist_instdata.iloc[i:j,:].itertuples():
            artist_fan_data = pd.DataFrame()
            artist_name = row.Artist
            artist_username = row.Username
            profile = instaloader.Profile.from_username(L.context, artist_username)
            posts = profile.get_posts()
            hashtags = {}
            sentiments = []
            artist_mentions = {}
            for post in posts:
                caption = post.caption
                # Extract hashtags
                hashtags.update({hashtag:hashtags.get(hashtag, 0) + 1 for hashtag in post.caption_hashtags})
                #Analyze sentiment
                if caption is not None:
                    sentiment = SentimentIntensityAnalyzer().polarity_scores(caption)["compound"]
                    sentiments.append(sentiment)
                    if artist_name in caption:
                        artist_mentions[artist_name] = artist_mentions.get(artist_name, 0) + 1
            artist_counts = sum(artist_mentions.values())
            hashtag_counts = sum(hashtags.values())
            average_sentiment = sum(sentiments) / len(sentiments)
            artist_fan_data._append(pd.DataFrame({'artist_counts':artist_counts,'hashtag_counts':hashtag_counts,'sentiment_score':average_sentiment}, index = [artist_name]))
        return artist_fan_data

def artist_instdata(csv_file):
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader) 
        data = list(csv_reader)
        instdata = pd.DataFrame()
        for row in data:
            artist_name = row[1]
            artist_username = row[2]
            instdata = instdata._append({'Artist':artist_name,'Username':artist_username},ignore_index=True)
    return instdata

username = "jim_desai"
password = "lifeyoga"
L = instaauth(username,password)
instdata = artist_instdata('Artists data.csv')
artist_engagement_data = fan_engagement_data(0,5,L,instdata)
print(artist_engagement_data) """