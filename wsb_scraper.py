import praw
import pandas as pd
import os
import datetime
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# set up Reddit API
reddit = praw.Reddit(client_id='o5HoS-P9uefXsQ', client_secret='9rBM2ILgyRne7tiu3xJjPrZqIXJvRA', user_agent='dantenvmt')
wsb = reddit.subreddit('wallstreetbets')

# common WSB terminology and associated sentiments
wsb_words = {
    'tendies': 2.0,
    'bull': 2.0,
    'bear': -2.0,
    'puts': -2.0,
    'calls': 2.0,
    'moon': 2.0,
    'btfd': 2.0,
    'going tits up': -2.0,
}

def get_sentiment(df_col, words=wsb_words):

    # initializes VADER
    vader = SentimentIntensityAnalyzer()

    # updates VADER's lexicon to include WSB terminology
    vader.lexicon.update(wsb_words)

    # analyzes sentiment of dataframe column input
    scores = df_col.apply(vader.polarity_scores).tolist()
    return pd.DataFrame(scores)

def get_date(submission):
    
    # gets submission datetime
    try:
        time = submission.created
    except: 
        time = submission
    return datetime.date.fromtimestamp(time)

def scrape_for(symbol, limit=10, after='120d', subreddit='wallstreetbets'):
    result = []
    url_for_comment = 'https://api.pushshift.io/reddit/search/comment/?q={0}&subreddit={1}&after={2}&size={3}&sort_type=score'.format(symbol, subreddit, after, limit)
    comments = requests.get(url_for_comment).json()['data']

    url_for_submission = 'https://api.pushshift.io/reddit/search/submission/?q={0}&subreddit={1}&after={2}&size={3}&sort_type=score'.format(symbol, subreddit, after, limit)
    submissions = requests.get(url_for_submission).json()['data']

    for comment in comments:
        result.append((comment['body'], get_date(comment['created_utc'])))

    for submission in submissions:
        date = get_date(submission['created_utc'])
        try:
            result.append((submission['title'] + submission['selftext'], date))
        except:
            result.append((submission['title'], date))
        sub = reddit.submission(id=submission['id'])
        sub.comments.replace_more(limit=0)
        for top_level_comment in sub.comments:
            result.append((top_level_comment.body, date))

    # creates a dataframe from API results
    df = pd.DataFrame(result, columns=['Text', 'Date'])

    # updates dataframe to include sentiments
    scored_df = df.join(get_sentiment(df['Text']), rsuffix='_right')

    return scored_df

