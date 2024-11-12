from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import subprocess

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def main_page():
    return 'Main page'

@app.route('/firebase')
def firebase_page():
    return 'FirebasePage'


@app.route('/firebase/result', methods=['GET'])
def get():
    try:
        file_path2 = "request.json"
        with open(file_path2, 'r') as file:
            data = json.load(file)
            date = data.get('date')
            feature = data.get('feature')

        file_path = f'./path/to/my_dir/raw/{feature}/metal_data_{date}.json'
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            return jsonify(data)
        
        else:
            result = subprocess.run(['python3', 'job.py', date, feature], capture_output=True, text=True)

            if result.returncode == 0:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                return jsonify(data)
            else:
                return jsonify({'error': 'Failed to generate data', 'status': 'failed', 'details': result.stderr}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}', 'status': 'failed'}), 500

def run_flask():
    app.run(host='0.0.0.0', port=8081)

if __name__ == "__main__":
    run_flask()