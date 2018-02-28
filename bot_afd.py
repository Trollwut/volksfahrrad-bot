# A reddit bot that posts a love letter if a thread is about the German party AfD
# Created by Trollwut (/u/Trollw00t)

import praw
import config
import time
import os

# define which subreddit(s) should be crawled
# combine more than one with a plus (e.g. `sub1+sub2`)
subreddits = "test"
# limit of maximum new post being crawled
crawl_limit = 20
# waiting time between two runs
sleep_between_runs = 60 * 10
# wait after comment
sleep_after_comment = 60 * 10
# name of save file
save_file = 'replied_to.txt'

# ripped from https://www.reddit.com/r/de/comments/80f5wv/afdgemeinder%C3%A4te_bieten_geld_f%C3%BCr_mandat_die/duvcgh2/
answer = "Diese Partei ist ein Organ der Niedertracht. Es ist falsch, sie zu wählen. Jemand, der zu dieser Partei beiträgt, ist gesellschaftlich absolut inakzeptabel. Es wäre verfehlt, zu einem ihrer Politiker freundlich oder auch nur höflich zu sein. Man muss so unfreundlich zu ihnen sein, wie es das Gesetz gerade noch zulässt. Es sind schlechte Menschen, die Falsches tun."

def bot_login():
    print('Logging in as ' + config.username + '...')
    r = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "Trollwut's AfD bot")
    print('Logged in!')

    return r

def run_bot(r, submissions_replied_to):
    print('Crawling /r/' + subreddits + ' for new posts...')

    for submission in r.subreddit(subreddits).new(limit=crawl_limit):
        print('Next submission...')
        if "AfD" in submission.title:
            print('Found a post about Volksfahrräder » ' + submission.title)

            # Check if we already answered this post
            # Check all top-level comments if we have ourself as an author
            bot_answered = False
            if submission.id in submissions_replied_to:
                print('    Submission ID already has an answer.')
                continue

            else:
                for top_level_comment in submission.comments:
                    if top_level_comment.author == r.user.me():
                        bot_answered = True

                if bot_answered == True:
                    print('    ... but we already answered to this post.')
                    submissions_replied_to.append(submission.id)
                    # save new submission id to our save file
                    with open(save_file, "a") as f:
                        f.write(submission.id + "\n")

                if bot_answered == False:
                    print('    Ooh, that\'s new! Let me write an answer...')
                    submission.reply(answer)

    # new line for aesthetics
    print()


def get_saved_submissions():
    # get all saved submission IDs out of our save file
    if not os.path.isfile(save_file):
        replied_to = []
    else:
        with open(save_file, "r") as f:
            replied_to = f.read().split("\n")
    return replied_to


# Let's login to our bot
r = bot_login()

# runtime variable to which posts we already replied to (and already have crawled)
submissions_replied_to = get_saved_submissions()

#while True:
run_bot(r, submissions_replied_to)
    #time.sleep(sleep_between_runs)
