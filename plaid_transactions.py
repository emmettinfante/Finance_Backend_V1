import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
LUNCHMONEY_TOKEN = os.getenv("LUNCHMONEY_TOKEN")

def upload_to_dropbox(local_file_path, dropbox_dest_path):
    try:
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
            print(f"❌ Dropbox upload failed: {response.status_code} — {response.text}")
    except Exception as e:
        print(f"❌ Dropbox upload error: {e}")

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
        
        if response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            break

        data = response.json()
        txns = data.get('transactions', [])

        if not txns:
            print("✅ No more transactions to fetch.")
            break

        all_transactions.extend(txns)
        params['offset'] += len(txns)

    df = pd.DataFrame(all_transactions)
    csv_path = "plaid_transactions.csv"
    txt_path = "plaid_assets.txt"

    if not df.empty:
        # Save CSV locally
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} transactions to {csv_path}")

        # Save log TXT
        with open(txt_path, "w") as file:
            file.write('transactions downloaded successfully\n')
            file.write(datetime.today().strftime('%Y-%m-%d %H:%M'))

        # Upload both files to Dropbox
        upload_to_dropbox(csv_path, "/plaid/plaid_transactions.csv")
        upload_to_dropbox(txt_path, "/plaid/plaid_assets.txt")
    else:
        print("❌ No data fetched. Skipping file save and upload.")

    return df
