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
    #submission = reddit.submission(id='hikrpa')
    haiku = [None] * 3
    # Creates array visited submissions
    with open('visited_submissions.txt', 'a+') as f:
        visited = f.read().splitlines()
    
    # Iterates through 10 newest submissions
    for submission in subreddit.new(limit=10):
        print("\t" + submission.title + "\n")
        if submission.id in visited:
            continue
        visited.append(submission.id)
        # Opens all the comments
        submission.comments.replace_more(limit=None)
        # Iterates through checking comments and turning them into haikus if they follow the format
        for comment in submission.comments.list():
            commentSyllables = check_syllables(comment.body)
            if (commentSyllables == 5):
                if (not haiku[0]):
                    haiku[0] = comment.body
                else:
                    haiku[2] = comment.body
            
            if (commentSyllables == 7):
                haiku[1] = comment.body
            
            if haiku[0] and haiku[1] and haiku[2]:
                comment.reply(haiku[0] + "\n\n" + haiku[1] + "\n\n" + haiku[2])
                for line in haiku:
                    line = None
    
    # Writes the new visited submissions into a file
    with open('visited_submissions.txt', 'a') as f:
        for item in visited:
            f.write("%s\n" % item)

def check_syllables(comment):
    # Makes comments suitable to pass as key to CMU dictionary e.g. I write, erase, rewrite = [i, write, erase, rewrite]
    cleanCopy = regex.sub(' ', comment)
    cleanCopy = cleanCopy.lower().split()

    syllables = 0
    # Goes through each counting up the syllables
    for word in cleanCopy:
        pronouncedWord = syllableDict.get(word)
        # Skips the word if it's not in the dictonary (update this later so it learns new words)
        if (pronouncedWord == None or syllables > 7):
            return 0
        for phoneme in pronouncedWord[0]:
            syllables += 1 if any(map(str.isdigit, phoneme)) else 0
    return syllables


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

if __name__ == "__main__":
    main()