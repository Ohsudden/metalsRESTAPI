import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
from datetime import timedelta, datetime
import pandas as pd
import firebase_admin
import os
import json
import requests
import sys



load_dotenv()

if not firebase_admin._apps:
    #cred = credentials.Certificate("vyshnevetskyi-data-engineering-firebase-adminsdk-836jz-b41fb4f91d.json")
    cred_dict = json.loads(os.environ['FIREBASE_SERVICE_ACCOUNT_CREDENTIAL'])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://vyshnevetskyi-data-engineering-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    
def get_metal_data_from_firebase():
    ref = db.reference('/')
    metal_data = ref.get()
    
    print("Raw data from Firebase:", metal_data)  
    
    if metal_data:
        df_metal = pd.DataFrame(metal_data)
        print("DataFrame shape:", df_metal.shape)  
        print("DataFrame columns:", df_metal.columns)  
        df_metal['Date'] = pd.to_datetime(df_metal['Date']).dt.date
        return df_metal
    else:
        print("No metal data found in Firebase.")
        return pd.DataFrame()

metal_df = get_metal_data_from_firebase()
print("Metal DataFrame:")
print(metal_df.head())

def save_data(date, metal):
    date = pd.to_datetime(date).date()
    if metal in ['Gold', 'Palladium', 'Platinum']:
        df_new = metal_df[['Date', f'{metal} AM Fix', f'{metal} PM Fix']]
        df_new = df_new.loc[(metal_df['Date'] == date)]
    elif metal == 'Silver':
        df_new = metal_df[['Date', f'{metal} Fix']]
        df_new = df_new.loc[(metal_df['Date'] == date)]
    elif metal in ['Iridium', 'Rhodium', 'Ruthenium']:
        df_new = metal_df[['Date', f'{metal}']]
        df_new = df_new.loc[(metal_df['Date'] == date)]

    if not df_new.empty:
        json_file_path = f"./path/to/my_dir/raw/{metal}/metal_data_{date}.json"
        
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        
        df_new.to_json(json_file_path, orient='records', date_format='iso')
        
        print(f"Data saved to {json_file_path}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        date, metals = args
        save_data(date, metals)
    else:
        print("Usage: python script.py <date> <metal>")