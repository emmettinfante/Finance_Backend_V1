import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Dropbox token (store in .env for Render)
load_dotenv()
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
LUNCHMONEY_TOKEN = os.getenv("LUNCHMONEY_TOKEN")

def upload_to_dropbox(local_file_path, dropbox_dest_path):
    with open(local_file_path, "rb") as f:
        headers = {
            "Authorization": f"Bearer {DROPBOX_TOKEN}",
            "Dropbox-API-Arg": f'{{"path": "{dropbox_dest_path}", "mode": "overwrite"}}',
            "Content-Type": "application/octet-stream"
        }
        response = requests.post("https://content.dropboxapi.com/2/files/upload", headers=headers, data=f)
    if response.status_code == 200:
        print(f"✅ Uploaded {dropbox_dest_path} to Dropbox.")
    else:
        print(f"❌ Failed to upload {dropbox_dest_path}: {response.text}")

def transactions():
    url = "https://api.lunchmoney.app/v1/transactions"
    headers = {"Authorization": f"Bearer {LUNCHMONEY_TOKEN}"}
    params = {
        "start_date": "2000-01-01",
        "end_date": datetime.today().strftime('%Y-%m-%d'),
        "limit": 500,
        "offset": 0
    }

    all_transactions = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            txns = data.get('transactions', [])
            if not txns:
                break
            all_transactions.extend(txns)
            params['offset'] += len(txns)
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            break

    df = pd.DataFrame(all_transactions)

    # Save CSV locally
    csv_path = "plaid_transactions.csv"
    txt_path = "plaid_assets.txt"
    with open(txt_path, "w") as file:
        file.write('transactions downloaded successfully\n')
        file.write(datetime.today().strftime('%Y-%m-%d %H:%M'))

    # Upload both to Dropbox
    upload_to_dropbox(csv_path, "/plaid/plaid_transactions.csv")
    upload_to_dropbox(txt_path, "/plaid/plaid_assets.txt")

    return df
