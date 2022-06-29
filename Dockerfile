# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

#ADD ENV VARIABLES
ENV TWEEPY_CONSUMER_KEY='<your-key>'
ENV TWEEPY_CONSUMER_SECRET='<your-key>'
ENV TWEEPY_BEARER_TOKEN='<your-key>'
ENV TWEEPY_ACCESS_KEY='<your-key>'
ENV TWEEPY_ACCESS_SECRET='<your-key>'
ENV SPOTIPY_REDIRECT_URI='http://localhost:8080'
ENV SPOTIPY_CLIENT_ID='<your-key>'
ENV SPOTIPY_CLIENT_SECRET='<your-key>'
ENV SPOTIPY_BOT_USER='<your-key>'

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "bot.py"]
