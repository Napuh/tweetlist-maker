# tweetlist-maker
Tweepy bot to generate spotify playlists based on user's lasts tweets.

# Config

To configure this bot we need to set the following enviromental variables:

```
export TWEEPY_CONSUMER_KEY='<your-key>'
export TWEEPY_CONSUMER_SECRET='<your-key>'
export TWEEPY_BEARER_TOKEN='<your-key>'
export TWEEPY_ACCESS_KEY='<your-key>'
export TWEEPY_ACCESS_SECRET='<your-key>'
export SPOTIPY_REDIRECT_URI='http://localhost:8080'
export SPOTIPY_CLIENT_ID='<your-key>'
export SPOTIPY_CLIENT_SECRET='<your-key>'
export SPOTIPY_BOT_USER='<your-key>'
```

To configure them in the Dockerfile, you just need to fill them with your values.

Make sure the twitter app setting enable tweet writing.

# Usage
## Simple run

Place all files in the same folder. Install requirements with 
```bash
pip3 install -r requirements.txt
```
Run bot.py with
```bash
python3 bot.py
```

It will prompt you with a browser window to authorize the app. 

After that, it will generate a .cache file in the same folder which will be needed to run the bot without authorizing again.

## Docker

To run this on docker, we need to run the bot with the simple method, in order to generate a .cache file.

Then, we can create an image using the Dockerfile, adjusting the enviromental variables to the correct values.

Once the correct keys are configured, we can create the image with 
```bash
docker build -t tweetlist-maker .
```

Then, we run the image created with
```bash
docker run tweetlist-maker:latest
```