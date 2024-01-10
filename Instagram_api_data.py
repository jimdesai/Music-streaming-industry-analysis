import instaloader
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

L = instaloader.Instaloader()
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
