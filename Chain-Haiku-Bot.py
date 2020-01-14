import praw
import re
import os
from nltk.corpus import cmudict

def main():
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('test') # pythonforengineers

    for submission in subreddit.new(limit=10):
        print("\t" + submission.title)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print("\t\t", comment.body)

def check_haiku():
    return 0

if __name__ == "__main__":
    main()