import praw
import re
import os
import csv
from nltk.corpus import cmudict

syllableDict = cmudict.dict()
regex = re.compile('[^a-zA-Z ]')


def main():
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('test')  # pythonforengineers
    submission = reddit.submission(id='giptxi')

    for comment in submission.comments.list():
        print(comment.body)
        print(check_syllables(comment.body))


    """     for submission in subreddit.stream.submissions():
        print("\t" + submission.title)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            check_syllables(comment.body)
            print(comment.body)  """


def process_comment(comment, depth=0):
    """Generate comment bodies and depths."""
    yield comment.body, depth
    for reply in comment.replies:
        yield from process_comment(reply, depth + 1)


def get_post_comments(post, more_limit=32):
    """Get a list of (body, depth) pairs for the comments in the post."""
    comments = []
    post.comments.replace_more(limit=more_limit)
    for top_level in post.comments:
        comments.extend(process_comment(top_level))
    return comments


def check_syllables(comment):
    # Makes comments suitable to pass as key to CMU dictionary e.g. I write, erase, rewrite = [i, write, erase, rewrite]
    cleanCopy = regex.sub(' ', comment)
    cleanCopy = cleanCopy.lower().split()

    print(cleanCopy)
    syllables = 0
    # Goes through each counting up the syllables
    for word in cleanCopy:
        pronouncedWord = syllableDict.get(word)
        # Skips the word if it's not in the dictonary (update this later so it learns new words)
        if (pronouncedWord == None):
            break
        for phoneme in pronouncedWord[0]:
            syllables += 1 if any(map(str.isdigit, phoneme)) else 0

    return syllables

def create_haiku(comment):
    return 0

if __name__ == "__main__":
    main()
