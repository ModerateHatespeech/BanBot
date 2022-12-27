"""
Toxicity Content Bot Script by ModerateHatespeech.com
@description Scans subreddit(s) for content that is considered toxic and reports the comment to moderators
@version 1.0.0
@last_updated 2/13/2022
"""

import praw
import requests
import json
import traceback
import logging
import re

logging.basicConfig(filename='report.log', format='%(asctime)s - %(message)s', level=logging.INFO) # action log

def load_config():
  """ Load configuration file """
  with open("config.json", "r") as f:
    config = json.load(f)
    missing = ["client_id", "client_secret", "subreddit", "api_token","username", "password","threshold"] - config.keys()
    if len(missing) > 0:
      raise KeyError("Missing keys in config.json {0}".format(str(missing)))
    return config

def login(config):
  """ Login to Reddit """
  reddit = praw.Reddit(
      user_agent = "BadwordBot (by u/toxicitymodbot)",
      client_id = config['client_id'],
      client_secret = config['client_secret'],
      password = config['password'],
      username = config['username']
  )
  return reddit

def get_reg_exp():
  with open("words.txt", "r") as f:
    words = f.read().splitlines()
    # turn into something like this:
    # (?:^| )(?:<each word from word separated by a |)(?: |$|\.|!|\?|,)
    # (?:^| )(?:word1|word2|word3)(?: |$|\.|!|\?|,)
    expression = r"(?i)(?:^| |\"|')(?:" + "|".join(words) + ")(?: |$|\.|!|\?|,|'|\")"
    return expression

def detect_word(text, regex):
  """ Call API and return response list with boolean & confidence score """
  if not config['quotes']:
    text = re.sub(r'>[^\n]+', "", text) # strip out quotes
  
  # Processing rules here. 
  
  # end of processing rules
  # if text matches regex return True
  regex =  re.compile(regex)
  matches = regex.search(text)
  if matches:
    return [True, matches]
  
  return [False]

def ban_user(username, data):
  """ Ban user from subreddit """
  reddit.subreddit(config['subreddit']).banned.add(username, 
                                                   ban_reason="Banned for saying '{0}'".format(data[0]), 
                                                   note=data[1], 
                                                   ban_message=config['ban_message'].replace("<word>", data[0]))

if __name__ == "__main__":
  config = load_config()
  reddit = login(config)
  regex = get_reg_exp()

  subreddit = reddit.subreddit(config['subreddit'])

  for comment in subreddit.stream.comments():
    try:
      result = detect_word(comment.body, regex)
      if result[0]:
        logging.info('Comment ({0}) had bad word. Banning user {1}.'.format(comment.permalink, comment.author))
        ban_user(comment.author.name, [result[1].group(), comment.permalink])
    except:
      logging.warning(traceback.format_exc())
      traceback.print_exc()
