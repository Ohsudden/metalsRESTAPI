from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta, datetime
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import os
import json
import requests

load_dotenv()

app = Flask(__name__)
# Apply CORS to the entire Flask app
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello():
    return 'Main page'

def run_flask():
    app.run(host='0.0.0.0', port=8081)

if __name__ == "__main__":
    run_flask()
