import tweepy
from dotenv import load_dotenv
import os
import random
import time
import schedule
from datetime import datetime
import pytz
from flask import Flask
import threading

# Initialize Flask App
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set up Twitter API v2 credentials
client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

# Predefined facts
facts = [
    "Rosicrucianism emerged in the early 17th century through three manifestos...",
    "The Rosy Cross symbolizes both spiritual unfolding (the rose) and the sacrifice of physical existence (the cross)...",
    # Add the rest of your facts here
]

# Define the task to post a random fact
def post_fact():
    fact = random.choice(facts)
    try:
        client.create_tweet(text=fact)
        print(f"Tweeted: {fact}")
    except Exception as e:
        print(f"Error posting fact: {e}")

# Schedule the task to run every hour
schedule.every().hour.at(":00").do(post_fact)

# Function to run the scheduled tasks in the background
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Flask route to check if the app is running
@app.route('/')
def home():
    return "Rosicrucian Twitter Bot is running!"

# Start the Flask app and schedule tasks
if __name__ == '__main__':
    # Start the schedule in a separate thread
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.daemon = True
    schedule_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
