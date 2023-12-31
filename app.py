from flask import Flask, render_template, request, jsonify
import requests
from requests_oauthlib import OAuth1
from web3 import Web3
import os
from dotenv import load_dotenv

app = Flask(__name__)

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
    



YOUR_TOKEN_ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]


##------------Wallet 
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/567987522f034d2ab9a21522cb3ed808'))

@app.route('/verify_token', methods=['POST'])
def verify_token():
    address = request.form.get('address')
    token_contract_address = '0x0a45f13B4934493755E9Cd3C3F4B086f2B2C8600'
    token_contract = w3.eth.contract(address=token_contract_address, abi=YOUR_TOKEN_ABI)
    balance = token_contract.functions.balanceOf(address).call()
    if balance > 0:
        return jsonify(status="success")
    else:
        return jsonify(status="error", message="No token found for this address")




if __name__ == '__main__':
    app.run(debug=True)