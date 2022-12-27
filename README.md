# Reddit BadwordBot
Automatically ban users who say a certain word, unconditionally

## Purpose
The following python bot built via Praw will automatically ban user who say a word on a blacklist of words.

## Requirements
Install requirements:
```apt-get install python3
pip3 install praw
```

Required config.json file:
```json
{
    "subreddit": "subreddit",
    "client_id": "REDDIT_APPLICATION_CLIENT_ID",
    "client_secret": "REDDIT_APPLICATION_CLIENT_SECRET",
    "username": "REDDIT_BOT_ACCOUNT_USERNAME",
    "password": "REDDIT_BOT_ACCOUNT_PASSWORD",
    "ban_message": "You've been banned for saying: <word>", 
    "quotes": false 
}
```

\<word\> is a template for the detected word in the ban_message

Set "quotes" to true if you want to include quote in message to check (Markdown: "> quote")

Run with:
```python3 bot.py```
