import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get your token
token = os.getenv('lunchmoney_token')

# Set API endpoint for balances
url = "https://api.lunchmoney.app/v1/balances"

# Set headers
headers = {
    "Authorization": f"Bearer {token}"
}

# Make request
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    balances = data.get('balances', [])

    if not balances:
        print("No balances found.")
        exit()

    # Convert to DataFrame
    df = pd.DataFrame(balances)

    # 🔥 Filter to Chase Broker account
    # (print unique account names if unsure!)
    print(df['account_name'].unique())

    # Adjust this string to match exactly
    chase_broker_balances = df[df['account_name'] == 'Chase Broker']

    # Save to CSV
    output_path = '/Users/m1max/Downloads/chase_broker_balances.csv'
    chase_broker_balances.to_csv(output_path, index=False)

    print(f"✅ Downloaded {len(chase_broker_balances)} balances to {output_path}")
    print(chase_broker_balances.head())

elif response.status_code == 404:
    print("Error 404: Endpoint not found.")
else:
    print(f"Error {response.status_code}: {response.text}")