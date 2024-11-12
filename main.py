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

@app.route('/')
def hello():
    return 'Main page'

@app.route('/firebase/')
def hello():
    return 'FirebasePage'

@app.route('/firebase/<date,Gold>', methods=['POST'])
def update_quest_status(user_id):
    if request.method == 'POST':
        data = request.json
        idofTask = data.get('idofTask')  # Get idofTask from the request data
        quest_status = True
        db.update_user_quest_status(user_id, idofTask, quest_status)
        return jsonify({'success': True})
    else:
        return None

def run_flask():
    app.run(host='0.0.0.0', port=8081)

if __name__ == "__main__":
    run_flask()
