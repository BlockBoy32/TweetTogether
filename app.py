from flask import Flask, render_template, request, jsonify
import requests
from requests_oauthlib import OAuth1

app = Flask(__name__)

import os
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")




auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
BASE_URL = "https://api.twitter.com/2"

@app.route('/')
def index():
    return render_template('index.html')



    ##------------Posting 
@app.route('/post_tweet', methods=['POST'])
def post_tweet():
    tweet_text = request.form.get('tweet')
    response = requests.post(
        f"{BASE_URL}/tweets",
        headers={"Content-Type": "application/json"},
        json={"text": tweet_text},
        auth=auth
    )
    data = response.json()
    # Print the response for debugging
    print("POST /tweets Response:", data)
    
    if response.status_code == 201:
        return jsonify(status="success", tweet_id=data["data"]["id"], tweet_text=tweet_text)
    else:
        error_message = "Unknown error"
        if "errors" in data and len(data["errors"]) > 0:
            error_message = data["errors"][0].get("message", "Unknown error")
        return jsonify(status="error", message=error_message)
    


    ##------------FEED
@app.route('/get_recent_tweets')
def get_recent_tweets():
    response = requests.get(
        "https://api.twitter.com/1.1/statuses/user_timeline.json?count=10",
        auth=auth
    )
    data = response.json()
    if response.status_code == 200:
        tweets = [{"id": tweet["id_str"], "text": tweet["text"]} for tweet in data]
        return jsonify(tweets)
    else:
        return jsonify([])  # Return an empty list in case of an error





if __name__ == '__main__':
    app.run(debug=True)